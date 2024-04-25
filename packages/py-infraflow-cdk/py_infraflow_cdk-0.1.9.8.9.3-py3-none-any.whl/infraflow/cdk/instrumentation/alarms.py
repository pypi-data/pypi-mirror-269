import builtins
import typing

import jsii
from aws_cdk.aws_cloudwatch import Metric, ComparisonOperator
from constructs import Construct


class AlarmsBase:
    def __init__(self, name: str, resource: Construct, scope: Construct=None):
        self.scope = scope
        self.resource = resource
        self.name = name



    def create_alarm(
        self,
        metric: Metric,
        name: str,
        evaluation_periods: jsii.Number,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        comparison_operator: typing.Optional[ComparisonOperator] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluate_low_sample_count_percentile: typing.Optional[builtins.str] = None,
        treat_missing_data: typing.Optional["TreatMissingData"] = None
    ):
        return metric.create_alarm(
            id=f"{self.name}{name}",
            alarm_name=f"{self.name}{name}",
            scope=self.scope,
            threshold=threshold,
            alarm_description=alarm_description,
            evaluation_periods=evaluation_periods,
            comparison_operator=comparison_operator,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluate_low_sample_count_percentile=evaluate_low_sample_count_percentile,
            treat_missing_data=treat_missing_data
        )