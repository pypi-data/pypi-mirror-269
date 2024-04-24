from abc import ABC, abstractmethod
import typing
from everai.autoscaling.factors import Factors
from everai.autoscaling.action import DecideResult


class AutoScalingPolicy(ABC):
    @abstractmethod
    def decide(self, factors: Factors) -> DecideResult: ...
