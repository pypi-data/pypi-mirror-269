from __future__ import annotations

import typing
from datetime import datetime

from everai.utils.datetime import format_datetime
from everai.utils.show_mixin import ShowMixin, TableField
from generated.schedulers import Appsv1Worker


class Worker(ShowMixin):
    worker_id: str
    device_id: str
    status: str
    created_at: datetime
    deleted_at: typing.Optional[datetime]

    table_fields: typing.List[TableField] = [
        TableField('worker_id', "ID"),
        TableField('status'),
        TableField('created_at', formatter=lambda dt: format_datetime(dt)),
        TableField('deleted_at', formatter=lambda dt: format_datetime(dt) if dt else ''),
    ]

    wide_table_extra_fields: typing.List[TableField] = [
        TableField('device_id', "DEVICE"),
    ]

    def __init__(self, worker_id: str, device_id: str, status: str,
                 created_at: datetime, deleted_at: typing.Optional[datetime] = None):
        self.worker_id = worker_id
        self.device_id = device_id
        self.status = status
        self.created_at = created_at
        self.deleted_at = deleted_at
        ...

    @staticmethod
    def from_proto(worker: Appsv1Worker) -> Worker:
        return Worker(
            worker_id=worker.id,
            device_id=worker.device_id,
            status=worker.status,
            created_at=worker.created_at,
            deleted_at=worker.deleted_at,
        )

    def to_proto(self) -> Appsv1Worker:
        return Appsv1Worker(
            id=self.worker_id,
            device_id=self.device_id,
            status=self.status,
            created_at=self.created_at,
            deleted_at=self.deleted_at,
        )

    def to_dict(self):
        return {
            'id': self.worker_id,
            'device': self.device_id,
            'status': self.status,
            'created_at': self.created_at,
            'deleted_at': self.deleted_at,
        }
