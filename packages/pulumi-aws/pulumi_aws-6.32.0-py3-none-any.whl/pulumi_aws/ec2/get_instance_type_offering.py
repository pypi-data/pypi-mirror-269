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
from ._inputs import *

__all__ = [
    'GetInstanceTypeOfferingResult',
    'AwaitableGetInstanceTypeOfferingResult',
    'get_instance_type_offering',
    'get_instance_type_offering_output',
]

@pulumi.output_type
class GetInstanceTypeOfferingResult:
    """
    A collection of values returned by getInstanceTypeOffering.
    """
    def __init__(__self__, filters=None, id=None, instance_type=None, location_type=None, preferred_instance_types=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_type and not isinstance(instance_type, str):
            raise TypeError("Expected argument 'instance_type' to be a str")
        pulumi.set(__self__, "instance_type", instance_type)
        if location_type and not isinstance(location_type, str):
            raise TypeError("Expected argument 'location_type' to be a str")
        pulumi.set(__self__, "location_type", location_type)
        if preferred_instance_types and not isinstance(preferred_instance_types, list):
            raise TypeError("Expected argument 'preferred_instance_types' to be a list")
        pulumi.set(__self__, "preferred_instance_types", preferred_instance_types)

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetInstanceTypeOfferingFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="instanceType")
    def instance_type(self) -> str:
        """
        EC2 Instance Type.
        """
        return pulumi.get(self, "instance_type")

    @property
    @pulumi.getter(name="locationType")
    def location_type(self) -> Optional[str]:
        return pulumi.get(self, "location_type")

    @property
    @pulumi.getter(name="preferredInstanceTypes")
    def preferred_instance_types(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "preferred_instance_types")


class AwaitableGetInstanceTypeOfferingResult(GetInstanceTypeOfferingResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstanceTypeOfferingResult(
            filters=self.filters,
            id=self.id,
            instance_type=self.instance_type,
            location_type=self.location_type,
            preferred_instance_types=self.preferred_instance_types)


def get_instance_type_offering(filters: Optional[Sequence[pulumi.InputType['GetInstanceTypeOfferingFilterArgs']]] = None,
                               location_type: Optional[str] = None,
                               preferred_instance_types: Optional[Sequence[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstanceTypeOfferingResult:
    """
    Information about single EC2 Instance Type Offering.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_instance_type_offering(filters=[aws.ec2.GetInstanceTypeOfferingFilterArgs(
            name="instance-type",
            values=[
                "t2.micro",
                "t3.micro",
            ],
        )],
        preferred_instance_types=[
            "t3.micro",
            "t2.micro",
        ])
    ```
    <!--End PulumiCodeChooser -->


    :param Sequence[pulumi.InputType['GetInstanceTypeOfferingFilterArgs']] filters: One or more configuration blocks containing name-values filters. See the [EC2 API Reference](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstanceTypeOfferings.html) for supported filters. Detailed below.
    :param str location_type: Location type. Defaults to `region`. Valid values: `availability-zone`, `availability-zone-id`, and `region`.
    :param Sequence[str] preferred_instance_types: Ordered list of preferred EC2 Instance Types. The first match in this list will be returned. If no preferred matches are found and the original search returned more than one result, an error is returned.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['locationType'] = location_type
    __args__['preferredInstanceTypes'] = preferred_instance_types
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2/getInstanceTypeOffering:getInstanceTypeOffering', __args__, opts=opts, typ=GetInstanceTypeOfferingResult).value

    return AwaitableGetInstanceTypeOfferingResult(
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        instance_type=pulumi.get(__ret__, 'instance_type'),
        location_type=pulumi.get(__ret__, 'location_type'),
        preferred_instance_types=pulumi.get(__ret__, 'preferred_instance_types'))


@_utilities.lift_output_func(get_instance_type_offering)
def get_instance_type_offering_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetInstanceTypeOfferingFilterArgs']]]]] = None,
                                      location_type: Optional[pulumi.Input[Optional[str]]] = None,
                                      preferred_instance_types: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInstanceTypeOfferingResult]:
    """
    Information about single EC2 Instance Type Offering.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_instance_type_offering(filters=[aws.ec2.GetInstanceTypeOfferingFilterArgs(
            name="instance-type",
            values=[
                "t2.micro",
                "t3.micro",
            ],
        )],
        preferred_instance_types=[
            "t3.micro",
            "t2.micro",
        ])
    ```
    <!--End PulumiCodeChooser -->


    :param Sequence[pulumi.InputType['GetInstanceTypeOfferingFilterArgs']] filters: One or more configuration blocks containing name-values filters. See the [EC2 API Reference](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstanceTypeOfferings.html) for supported filters. Detailed below.
    :param str location_type: Location type. Defaults to `region`. Valid values: `availability-zone`, `availability-zone-id`, and `region`.
    :param Sequence[str] preferred_instance_types: Ordered list of preferred EC2 Instance Types. The first match in this list will be returned. If no preferred matches are found and the original search returned more than one result, an error is returned.
    """
    ...
