import builtins
import typing
from datetime import timedelta
from typing import Union

import jsii
from aws_cdk import Duration
from aws_cdk.aws_cloudwatch import ComparisonOperator, TreatMissingData, GraphWidget, Metric
from aws_cdk.aws_sqs import Queue
from constructs import Construct

from infraflow.cdk.core.utils import to_duration
from infraflow.cdk.instrumentation.alarms import AlarmsBase
from infraflow.cdk.instrumentation.metrics import InfraflowMetric


class QueueMetrics:
    def __init__(self, queue: Queue, scope: Construct=None):
        self.queue = queue
        self.scope = queue.stack if scope is None else scope

    @property
    def sent(self) -> InfraflowMetric:
        return InfraflowMetric(self.queue.metric_number_of_messages_sent())

    @property
    def length(self) -> InfraflowMetric:
        return InfraflowMetric(self.queue.metric_approximate_number_of_messages_visible())

    @property
    def age_of_oldest(self):
        return InfraflowMetric(self.queue.metric_approximate_age_of_oldest_message())



class QueueAlarms(AlarmsBase):
    def __init__(self, queue: Queue, name: str = None, scope: Construct = None):
        super().__init__(name or queue.queue_name, queue, scope or queue.stack)
        self.queue = queue
        self.metrics = QueueMetrics(queue)

    def age_of_oldest_over_threshold(self, threshold: int, period: Union[int, timedelta, Duration], evaluation_periods: int):
        return self.create_alarm(
            self.metrics.age_of_oldest.average.over(period),
            name=f"AgeOfOldestOverThreshold",
            threshold=threshold,
            evaluation_periods=evaluation_periods,
            comparison_operator=ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treat_missing_data=TreatMissingData.NOT_BREACHING,
        )

    def length_over_threshold(self, threshold: int, period: Union[int, timedelta, Duration], evaluation_periods: int):
        return self.create_alarm(
            self.metrics.length.average.over(period),
            name=f"LengthOverThreshold",
            threshold=threshold,
            evaluation_periods=evaluation_periods,
            comparison_operator=ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treat_missing_data=TreatMissingData.NOT_BREACHING,
        )

    def sent_over_threshold(self, threshold: int, period: Union[int, timedelta, Duration], evaluation_periods: int):
        return self.create_alarm(
            metric=self.metrics.sent.average.over(period),
            name=f"SentOverThreshold",
            threshold=threshold,
            evaluation_periods=evaluation_periods,
            comparison_operator=ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            treat_missing_data=TreatMissingData.NOT_BREACHING,
        )



class QueueWidgets:
    def __init__(self, queue: Queue, scope: Construct=None):
        self.queue = queue
        self.metrics = QueueMetrics(queue)
        self.scope = queue.stack if scope is None else scope

    def age_max_widget(self, period: Union[int, timedelta, Duration], width: int, height: int):
        widget = GraphWidget(
            title=f"{self.queue.queue_name} - Age of Oldest Message",
            height=height,
            width=width,
        )
        widget.add_left_metric(self.metrics.age_of_oldest.max.over(period=period))
        return widget

    def length_max_widget(self, period: Union[int, timedelta, Duration], width: int, height: int):
        widget = GraphWidget(
            title=f"{self.queue.queue_name} - Length of Queue",
            height=height,
            width=width,
        )
        widget.add_left_metric(self.metrics.length.max.over(period=period))
        return widget

    def sent_sum_widget(self, period: Union[int, timedelta, Duration], width: int, height: int):
        widget = GraphWidget(
            title=f"{self.queue.queue_name} - Total Messages Sent",
            height=height,
            width=width,
        )
        widget.add_left_metric(self.metrics.sent.sum.over(period=period))
        return widget


class QueueInstrumentation:
    def __init__(self, queue: Queue, scope: Construct=None):
        self.scope = queue.stack if scope is None else scope
        self.metrics = QueueMetrics(queue, self.scope)
        self.queue = queue
        self.widgets = QueueWidgets(queue, self.scope)
        self.alarms = QueueAlarms(queue, self.scope)
