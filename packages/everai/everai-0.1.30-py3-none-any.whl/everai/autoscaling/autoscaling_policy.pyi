from everai.autoscaling.factors import Factors
from everai.autoscaling.action import DecideResult

class AutoScalingPolicy:
    def decide(self, factors: Factors) -> DecideResult: ...
