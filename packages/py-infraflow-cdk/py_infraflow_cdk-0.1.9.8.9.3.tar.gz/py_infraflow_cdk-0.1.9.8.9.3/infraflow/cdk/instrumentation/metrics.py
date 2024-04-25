from datetime import timedelta
from typing import Union

from aws_cdk import Duration
from aws_cdk.aws_cloudwatch import Metric, Statistic as AwsStatistic

from infraflow.cdk.core.utils import to_duration

class Statistic:
    def __init__(self, metric: Metric, statistic: str):
        self._metric = metric.with_(statistic=statistic)

    def over(self, period: Union[int, timedelta, Duration]):
        return self._metric.with_(period=to_duration(period))

class InfraflowMetric:
    def __init__(self, metric: Metric):
        self.metric = metric

    @property
    def average(self) -> Statistic:
        return Statistic(self.metric, statistic="average")

    @property
    def max(self) -> Statistic:
        return Statistic(self.metric, statistic="max")

    @property
    def min(self) -> Statistic:
        return Statistic(self.metric, statistic="min")

    @property
    def sum(self) -> Statistic:
        return Statistic(self.metric, statistic="sum")

    # @property
    # def count_samples(self)  -> Statistic:
    #     return Statistic(self.metric, statistic="sum")
    #
    # @property
    # def trimmed_mean(self)  -> Statistic:
    #     return Statistic(self.metric, statistic="sum")
    #
    # @property
    # def percentage(self)  -> Statistic:
    #     return Statistic(self.metric, statistic="sum")
    #
    # @property
    # def percentage_rank(self)  -> Statistic:
    #     return Statistic(self.metric, statistic="sum")
    #
    # @property
    # def trimmed_count(self)  -> Statistic:
    #     return Statistic(self.metric, statistic="sum")
    #
    # @property
    # def trimmed_summ(self)  -> Statistic:
    #     return Statistic(self.metric, statistic="sum")