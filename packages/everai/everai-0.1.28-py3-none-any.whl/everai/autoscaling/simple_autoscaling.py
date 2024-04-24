import datetime
import typing
from everai.autoscaling.action import Action, ScaleUpAction, ScaleDownAction
from everai.autoscaling.autoscaling_policy import AutoScalingPolicy
from everai.autoscaling.factors import Factors, QueueReason, WorkerStatus


class SimpleAutoScalingPolicy(AutoScalingPolicy):
    # The minimum number of worker, even all of those are idle
    min_workers: int
    # The maximum number of worker, even there are some request in queue
    max_workers: int
    # The max_queue_size let scheduler know it's time to scale up
    max_queue_size: int
    # The quantity of each scale up
    scale_up_step: int
    # The max_idle_time in seconds let scheduler witch worker should be scale down
    max_idle_time: int

    def __init__(self,
                 min_workers: int,
                 max_workers: int,
                 max_queue_size: int,
                 max_idle_time: int,
                 scale_up_step: int = 1):
        assert 0 <= min_workers <= max_workers
        assert max_queue_size > 0
        assert max_idle_time > 0
        assert scale_up_step > 0

        self.min_workers = min_workers
        self.max_workers = max_workers
        self.max_queue_size = max_queue_size
        self.max_idle_time = max_idle_time
        self.scale_up_step = scale_up_step

    def should_scale_up(self, factors: Factors) -> bool:
        busy_count = 0
        for req in factors.queue.requests:
            if req.queue_reason == QueueReason.QueueDueBusy:
                busy_count += 1
        return busy_count > self.max_queue_size

    def decide(self, factors: Factors) -> typing.List[Action]:
        now = int(datetime.datetime.now().timestamp())
        # scale up to min_workers
        if len(factors.workers) < self.min_workers:
            return [ScaleUpAction(count=self.min_workers - len(factors.workers))]

        # ensure after scale down, satisfied the max_workers
        max_scale_up_count = self.max_workers - len(factors.workers)
        scale_up_count = 0
        if self.should_scale_up(factors):
            scale_up_count = min(max_scale_up_count, self.scale_up_step)

        if scale_up_count > 0:
            return [ScaleUpAction(count=scale_up_count)]

        # check if scale down is necessary
        scale_down_actions = []
        factors.workers.sort(key=lambda x: x.started_at, reverse=True)
        for worker in factors.workers:
            if (worker.number_of_sessions == 0 and worker.status == WorkerStatus.Free and
                    now - worker.last_service_time >= self.max_idle_time):
                scale_down_actions.append(ScaleDownAction(worker_id=worker.worker_id))

        # ensure after scale down, satisfied the min_workers
        max_scale_down_count = len(factors.workers) - self.min_workers
        scale_down_count = min(max_scale_down_count, len(scale_down_actions))
        return scale_down_actions[:scale_down_count]
