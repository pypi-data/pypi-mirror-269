import functools
import typing

from everai.app.volume_request import VolumeRequest
from everai.app.service import Service
from everai.autoscaling import AutoScalingPolicy
from everai.image import Image
from everai.resource_requests.resource_requests import ResourceRequests

AppSetupCallable = typing.Callable[[], None]
AppSetupMethod = typing.Callable[[AppSetupCallable], AppSetupCallable]


class _AppSetupFunction:
    def __init__(self, func: AppSetupCallable,
                 optional: bool = False,
                 ):
        self.func = func
        self.name = func.__name__
        self.optional = optional

    def __call__(self):
        return self.func()


def setup_params(func):
    @functools.wraps(func)
    def decorator(self, optional=False):
        return func(self, optional=optional)

    return decorator


class AppSetupMixin:
    _prepare_funcs: typing.List[_AppSetupFunction]
    _clear_funcs: typing.List[_AppSetupFunction]
    _image: Image

    _resource_requests: ResourceRequests
    _autoscaling_policy: AutoScalingPolicy
    _secret_requests: typing.Optional[typing.List[str]]
    _configmap_requests: typing.Optional[typing.List[str]]
    _volume_requests: typing.Optional[typing.List[VolumeRequest]]

    @property
    def prepare_funcs(self) -> typing.List[_AppSetupFunction]:
        return self._prepare_funcs

    @property
    def clear_funcs(self) -> typing.List[_AppSetupFunction]:
        return self._clear_funcs

    @setup_params
    def prepare(self, *args, **kwargs) -> AppSetupMethod:
        def decorator(func: AppSetupCallable) -> AppSetupCallable:
            self._prepare_funcs.append(_AppSetupFunction(func, *args, **kwargs))
            return func

        return decorator

    @setup_params
    def clear(self, *args, **kwargs) -> AppSetupMethod:
        def decorator(func: AppSetupCallable) -> AppSetupCallable:
            self._clear_funcs.append(_AppSetupFunction(func, *args, **kwargs))
            return func

        return decorator

    @property
    def secret_requests(self) -> typing.List[str]:
        return self._secret_requests or []

    @property
    def configmap_requests(self) -> typing.List[str]:
        return self._configmap_requests or []

    @property
    def volume_requests(self) -> typing.List[VolumeRequest]:
        return self._volume_requests or []

    @property
    def autoscaling_policy(self) -> AutoScalingPolicy:
        return self._autoscaling_policy

    @property
    def resource_requests(self) -> ResourceRequests:
        return self._resource_requests

