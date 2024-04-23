from __future__ import annotations

import typing
from datetime import datetime

from generated.schedulers import Appsv1Worker


class Worker(object):
    worker_id: str
    device_id: str
    status: str
    created_at: datetime
    deleted_at: typing.Optional[datetime]

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
