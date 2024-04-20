# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetEventIntegrationResult',
    'AwaitableGetEventIntegrationResult',
    'get_event_integration',
    'get_event_integration_output',
]

@pulumi.output_type
class GetEventIntegrationResult:
    """
    A collection of values returned by getEventIntegration.
    """
    def __init__(__self__, arn=None, description=None, event_filters=None, eventbridge_bus=None, id=None, name=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if event_filters and not isinstance(event_filters, list):
            raise TypeError("Expected argument 'event_filters' to be a list")
        pulumi.set(__self__, "event_filters", event_filters)
        if eventbridge_bus and not isinstance(eventbridge_bus, str):
            raise TypeError("Expected argument 'eventbridge_bus' to be a str")
        pulumi.set(__self__, "eventbridge_bus", eventbridge_bus)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The ARN of the AppIntegrations Event Integration.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of the Event Integration.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="eventFilters")
    def event_filters(self) -> Sequence['outputs.GetEventIntegrationEventFilterResult']:
        """
        A block that defines the configuration information for the event filter. The Event Filter block is documented below.
        """
        return pulumi.get(self, "event_filters")

    @property
    @pulumi.getter(name="eventbridgeBus")
    def eventbridge_bus(self) -> str:
        """
        The EventBridge bus.
        """
        return pulumi.get(self, "eventbridge_bus")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Metadata that you can assign to help organize the report plans you create.
        """
        return pulumi.get(self, "tags")


class AwaitableGetEventIntegrationResult(GetEventIntegrationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEventIntegrationResult(
            arn=self.arn,
            description=self.description,
            event_filters=self.event_filters,
            eventbridge_bus=self.eventbridge_bus,
            id=self.id,
            name=self.name,
            tags=self.tags)


def get_event_integration(name: Optional[str] = None,
                          tags: Optional[Mapping[str, str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEventIntegrationResult:
    """
    Use this data source to get information on an existing AppIntegrations Event Integration.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.appintegrations.get_event_integration(name="example")
    ```
    <!--End PulumiCodeChooser -->


    :param str name: The AppIntegrations Event Integration name.
    :param Mapping[str, str] tags: Metadata that you can assign to help organize the report plans you create.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:appintegrations/getEventIntegration:getEventIntegration', __args__, opts=opts, typ=GetEventIntegrationResult).value

    return AwaitableGetEventIntegrationResult(
        arn=pulumi.get(__ret__, 'arn'),
        description=pulumi.get(__ret__, 'description'),
        event_filters=pulumi.get(__ret__, 'event_filters'),
        eventbridge_bus=pulumi.get(__ret__, 'eventbridge_bus'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_event_integration)
def get_event_integration_output(name: Optional[pulumi.Input[str]] = None,
                                 tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEventIntegrationResult]:
    """
    Use this data source to get information on an existing AppIntegrations Event Integration.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.appintegrations.get_event_integration(name="example")
    ```
    <!--End PulumiCodeChooser -->


    :param str name: The AppIntegrations Event Integration name.
    :param Mapping[str, str] tags: Metadata that you can assign to help organize the report plans you create.
    """
    ...
