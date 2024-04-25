from __future__ import annotations

import datetime
import threading

from everai.utils.show_mixin import ShowMixin, TableField
from everai.autoscaling.autoscaling_policy import AutoScalingPolicy
from everai.image import Image
from everai.resource_requests.resource_requests import ResourceRequests
from everai.app.service import Service
from everai.app.volume_request import VolumeRequest
import typing

from generated.schedulers import V1App, V1AppStatus
from everai.app.app_runner import AppRunnerMixin
from everai.utils.datetime import format_datetime


class App(AppRunnerMixin, ShowMixin):
    _name: str
    _route_name: str
    _created_at: datetime.datetime
    _changed_at: datetime.datetime
    _status: V1AppStatus
    _image: Image

    table_fields: typing.List[TableField] = [
        TableField('name'),
        TableField('status'),
        TableField('created_at',
                   formatter=lambda dt: format_datetime(dt)),
        TableField('route_name'),
    ]
    wide_table_extra_fields: typing.List[TableField] = [
        TableField('changed_at',
                   formatter=lambda dt: format_datetime(dt)),
    ]

    def __init__(self,
                 name: str,
                 image: typing.Optional[Image] = None,
                 resource_requests: typing.Optional[ResourceRequests] = None,
                 autoscaling_policy: typing.Optional[AutoScalingPolicy] = None,
                 secret_requests: typing.Optional[typing.List[str]] = None,
                 configmap_requests: typing.Optional[typing.List[str]] = None,
                 volume_requests: typing.Optional[typing.List[VolumeRequest]] = None,
                 *args, **kwargs):
        self._name = name
        self._image = image
        self._resource_requests = resource_requests
        self._autoscaling_policy = autoscaling_policy
        self._volume_requests = volume_requests or []
        self._secret_requests = secret_requests or []
        self._configmap_requests = configmap_requests or []
        self.lock = threading.Lock()

        self._service = Service()
        self._prepare_funcs = []
        self._clear_funcs = []

    def __str__(self):
        return (f'App(name={self._name}, route_name={self._route_name}, '
                f'created_at={format_datetime(self._created_at, fmt="%Y-%m-%d %H:%M%z")}, '
                f'changed_at={format_datetime(self._changed_at, fmt="%Y-%m-%d %H:%M%z")}, '
                f'status={self._status}'
                f')')

    @property
    def name(self) -> str:
        return self._name

    @property
    def route_name(self) -> str:
        return self._route_name

    @route_name.setter
    def route_name(self, route_name: str):
        self._route_name = route_name

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @property
    def changed_at(self) -> datetime.datetime:
        return self._changed_at

    @property
    def status(self) -> V1AppStatus:
        return self._status

    @property
    def image(self) -> Image:
        return self._image

    @staticmethod
    def from_proto(v1app: V1App) -> App:
        app = App(name=v1app.name)
        app.route_name = v1app.route_path or v1app.name
        app._created_at = v1app.created_at
        app._changed_at = v1app.modified_at
        app._status = v1app.status
        return app

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'name': self._name,
            'status': self._status.value,
            'created_at': self._created_at,
            'changed_at': self._changed_at,
            'route_name': self._route_name,
        }
