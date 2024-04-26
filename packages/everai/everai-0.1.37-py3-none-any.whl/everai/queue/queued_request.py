from __future__ import annotations
from datetime import datetime
import typing

from everai.utils.datetime import format_datetime
from everai.utils.show_mixin import ShowMixin, TableField
from generated.schedulers import ListRequestQueuesResponseRequestQueue


class QueuedRequest(ShowMixin):
    queue_index: typing.Optional[int]
    create_at: typing.Optional[datetime]
    queue_reason: typing.Optional[str]

    table_fields: typing.List[TableField] = [
        TableField('queue_index'),
        TableField('create_at', formatter=lambda dt: format_datetime(dt)),
        TableField('queue_reason'),
    ]

    def __init__(self,
                 queue_index: typing.Optional[int],
                 create_at: typing.Optional[datetime],
                 queue_reason: typing.Optional[str]):
        self.queue_index = queue_index
        self.create_at = create_at
        self.queue_reason = queue_reason

    @staticmethod
    def from_proto(queue: ListRequestQueuesResponseRequestQueue) -> QueuedRequest:
        return QueuedRequest(
            queue_index=queue.index,
            create_at=queue.create_at,
            queue_reason=queue.reason,
        )
