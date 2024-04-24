import typing

import deprecation

from everai.api.api import ValueFromSecret
from everai.app import VolumeRequest
from everai.app.app import App
from everai.app.app_runtime import AppRuntime
from everai.app.autocaling_handler import register_autoscaling_handler
from everai.constants import EVERAI_FORCE_PULL_VOLUME
from everai.image import Image, BasicAuth
from everai.resource_requests.resource_requests import ResourceRequests
from everai.runner import must_find_target
from everai.api import API
from everai.secret import Secret, SecretManager, Placeholder
from everai.volume import Volume, VolumeManager
from everai.autoscaling import AutoScalingPolicy
from gevent.pywsgi import WSGIServer
import gevent.signal
import signal
import threading

from flask import Flask, Blueprint, Response

from everai.worker.worker import Worker
from generated.schedulers import (
    ApiException,
    V1SetupVolume,
    V1ResourceClaim,
)
from generated.volumes.exceptions import NotFoundException as VolumeNotFoundException

autoscaling_warning = """
You are deploying an app without autoscaling_policy, 
that will cause the app to run only one worker and always one worker,
if you want to setup an autoscaling_policy for this app after deploy,
you cloud run command everai app upgrade <your app name> --autoscaling-policy,
or setup in your dashboard, www.evermachine.com
"""


class AppManager:
    def __init__(self):
        self.api = API()
        self.secret_manager = SecretManager()
        self.volume_manager = VolumeManager()
        self._running = False

    def create(self, app_name: str, app_route_name: typing.Optional[str] = None) -> App:
        resp = self.api.create_app(name=app_name, route_name=app_route_name)
        return App.from_proto(resp)

    def pause(self, app_name: str):
        self.api.pause_app(name=app_name)

    def prepare_secrets(self, app: App, runtime: AppRuntime):
        prepared_secrets: typing.Dict[str, Secret] = {}
        for name in app.secret_requests:
            secret = self.secret_manager.get(name=name)
            prepared_secrets[secret.name] = secret
        runtime.secrets = prepared_secrets
        # app.prepared_secrets = prepared_secrets

    def prepare_volumes(self, app: App, runtime: AppRuntime):
        prepared_volumes: typing.Dict[str, Volume] = {}
        for req in app.volume_requests:
            try:
                volume = self.volume_manager.get(req.name)
                prepared_volumes[volume.name] = volume
            except VolumeNotFoundException as e:
                if req.create_if_not_exists:
                    volume = self.volume_manager.create_volume(name=req.name)
                elif req.optional:
                    continue
                else:
                    raise e

            volume.set_path(self.volume_manager.volume_path(volume.id))
            prepared_volumes[volume.name] = volume

            if EVERAI_FORCE_PULL_VOLUME:
                self.volume_manager.pull(volume.name)
        # app.prepared_volumes = prepared_volumes
        runtime.volumes = prepared_volumes

    def everai_handler(self, flask_app: Flask):
        everai_blueprint = Blueprint('everai', __name__, url_prefix='/-everai-')

        @everai_blueprint.route('/healthy', methods=['GET'])
        def healthy():
            status = 200 if self._running else 503
            message = 'Running' if self._running else 'Preparing'
            return Response(message, status=status, mimetype='text/plain')

        flask_app.register_blueprint(everai_blueprint)

    def run_autoscaling(self, app: typing.Optional[App] = None, *args, **kwargs):
        app = app or must_find_target(target_type=App)
        assert app.autoscaling_policy is not None

        flask_app = Flask(app.name)
        register_autoscaling_handler(flask_app, app.autoscaling_policy)
        AppManager.start_http_server(flask_app=flask_app, *args, **kwargs)

    @staticmethod
    def start_http_server(flask_app: Flask, cb: typing.Optional[typing.Callable[[], None]] = None, *args,
                          **kwargs):

        port = kwargs.pop('port', 8866)
        listen = kwargs.pop('listen', '0.0.0.0')

        http_server = WSGIServer((listen, port), flask_app)

        def graceful_stop(*args, **kwargs):
            print(f'Got stop signal, worker do final clear')
            if http_server.started:
                http_server.stop()
            if cb is not None:
                cb()

        gevent.signal.signal(signal.SIGTERM, graceful_stop)
        gevent.signal.signal(signal.SIGINT, graceful_stop)

        http_server.serve_forever()
        # flask_app.run(host=listen, port=port, debug=False)

    def run(self, app: typing.Optional[App] = None, *args, **kwargs):
        app = app or must_find_target(target_type=App)
        # start prepare thread
        prepare_thread = threading.Thread(target=self.prepare,
                                          args=(app,),
                                          kwargs=dict(
                                              is_prepare_mode=False,
                                          ))
        prepare_thread.start()

        flask_app = Flask(app.name)
        self.everai_handler(flask_app)
        app.service.create_handler(flask_app)

        AppManager.start_http_server(flask_app=flask_app, cb=app.do_clear, *args, **kwargs)

    def prepare(self, app: typing.Optional[App] = None,
                is_prepare_mode: bool = True,
                *args, **kwargs):
        app = app or must_find_target(target_type=App)
        runtime = AppRuntime()
        self.prepare_secrets(app, runtime)
        self.prepare_volumes(app, runtime)
        runtime.volume_manager = self.volume_manager
        runtime.secret_manager = self.secret_manager
        runtime.is_prepare_mode = is_prepare_mode
        app.runtime = runtime

        app.do_prepare()
        print('prepare finished')
        if len(app.service.routes) > 0 and not is_prepare_mode:
            self._running = True

    def delete(self, app_name: str) -> None:
        self.api.delete_app(app_name)

    def list(self) -> typing.List[App]:
        return [App.from_proto(app) for app in self.api.list_apps()]

    def get(self, app_name: str) -> App:
        v1app = self.api.get_app(app_name)
        return App.from_proto(v1app)

    def setup_image(self, app_name: str, image: Image):
        username = None
        password = None
        if image.auth is not None:
            assert isinstance(image.auth, BasicAuth)
            assert isinstance(image.auth.username, Placeholder)
            assert isinstance(image.auth.password, Placeholder)
            username = ValueFromSecret(secret_name=image.auth.username.secret_name,
                                       key=image.auth.username.secret_key)
            password = ValueFromSecret(secret_name=image.auth.password.secret_name,
                                       key=image.auth.password.secret_key)

        self.api.setup_image(app_name, repository=image.repository, tag=image.tag, digest=image.digest,
                             username=username, password=password)

    def setup_volume_requests(self, app_name: str, volume_requests: typing.List[VolumeRequest]):
        self.api.setup_volume_requests(app_name, [
            V1SetupVolume(volume_name=x.name, optional=x.optional,
                          create_if_not_exists=x.create_if_not_exists) for x in volume_requests])

    def setup_secret_requests(self, app_name: str, secret_requests: typing.List[str]):
        self.api.setup_secret_requests(app_name, secret_requests)

    def setup_resource_requests(self, app_name: str, resource_requests: ResourceRequests):
        self.api.setup_resource_requests(app_name, V1ResourceClaim(
            cpu_num=resource_requests.cpu_num,
            gpu_num=resource_requests.gpu_num,
            memory_mb=resource_requests.memory_mb,
            region_constraints=resource_requests.region_constraints,
            cpu_constraints=resource_requests.cpu_constraints,
            gpu_constraints=resource_requests.gpu_constraints,
            cuda_constraints=resource_requests.cuda_version_constraints,
            driver_version_constraints=resource_requests.driver_version_constraints,
        ))

    @deprecation.deprecated(details='setup_autoscaling_policy is deprecated, don not use it again')
    def setup_autoscaling_policy(self, app_name: str, autoscaling_policy: typing.Optional[AutoScalingPolicy]):
        ...
        # maybe use restrictedpython is more make sense
        # if autoscaling_policy is None:
        #     self.api.setup_autoscaling_policy(app_name=app_name)
        # else:
        #     obj = jsonpickle.dumps(autoscaling_policy)
        #     print(obj)
        #     sourcefile = inspect.getsourcefile(autoscaling_policy.__class__)
        #     with open(sourcefile, 'r') as f:
        #         sourcecode = f.read()
        #
        #     print(sourcecode)
        #     bin = compile(sourcecode, os.path.basename(sourcefile), 'exec')
        #     print(bin)
        #
        #     raise RuntimeError(f"Autoscaling policy")
        #
        #     assert isinstance(autoscaling_policy, SimpleAutoScalingPolicy)
        #     self.api.setup_autoscaling_policy(app_name=app_name,
        #                                       min_workers=autoscaling_policy.min_workers,
        #                                       max_workers=autoscaling_policy.max_workers,
        #                                       max_queue_size=autoscaling_policy.max_queue_size,
        #                                       max_idle_time=autoscaling_policy.max_idle_time,
        #                                       )

    def deploy(self, app: typing.Optional[App]):
        app = app or must_find_target(target_type=App)

        try:
            self.api.get_app(app.name)
        except ApiException as e:
            if e.status == 404:
                self.api.create_app(app.name)
            else:
                raise e

        missed = []
        if app.resource_requests is None:
            missed.append("resource_requests")
        if app.image is None:
            missed.append("image")

        if len(missed) > 0:
            msg = ', '.join(missed)
            raise Exception(f'resource_requests, image is required, {msg} is missed')

        if app.autoscaling_policy is None:
            print(f"Warning: {autoscaling_warning}")

        self.setup_image(app.name, app.image)

        if app.volume_requests is not None and len(app.volume_requests) > 0:
            self.setup_volume_requests(app.name, app.volume_requests)

        if app.secret_requests is not None and len(app.secret_requests) > 0:
            self.setup_secret_requests(app.name, app.secret_requests)

        self.setup_resource_requests(app.name, app.resource_requests)

        self.setup_autoscaling_policy(app.name, app.autoscaling_policy)

    def list_worker(self, app_name: str) -> typing.List[Worker]:
        workers = self.api.list_worker(app_name=app_name)
        return [Worker.from_proto(worker) for worker in workers]
