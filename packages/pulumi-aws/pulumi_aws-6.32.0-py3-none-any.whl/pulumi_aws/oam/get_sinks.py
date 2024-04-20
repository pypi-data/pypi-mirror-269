# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetSinksResult',
    'AwaitableGetSinksResult',
    'get_sinks',
    'get_sinks_output',
]

@pulumi.output_type
class GetSinksResult:
    """
    A collection of values returned by getSinks.
    """
    def __init__(__self__, arns=None, id=None):
        if arns and not isinstance(arns, list):
            raise TypeError("Expected argument 'arns' to be a list")
        pulumi.set(__self__, "arns", arns)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def arns(self) -> Sequence[str]:
        """
        Set of ARN of the Sinks.
        """
        return pulumi.get(self, "arns")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetSinksResult(GetSinksResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSinksResult(
            arns=self.arns,
            id=self.id)


def get_sinks(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSinksResult:
    """
    Data source for managing an AWS CloudWatch Observability Access Manager Sinks.

    ## Example Usage

    ### Basic Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.oam.get_sinks()
    ```
    <!--End PulumiCodeChooser -->
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:oam/getSinks:getSinks', __args__, opts=opts, typ=GetSinksResult).value

    return AwaitableGetSinksResult(
        arns=pulumi.get(__ret__, 'arns'),
        id=pulumi.get(__ret__, 'id'))


@_utilities.lift_output_func(get_sinks)
def get_sinks_output(opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSinksResult]:
    """
    Data source for managing an AWS CloudWatch Observability Access Manager Sinks.

    ## Example Usage

    ### Basic Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.oam.get_sinks()
    ```
    <!--End PulumiCodeChooser -->
    """
    ...
