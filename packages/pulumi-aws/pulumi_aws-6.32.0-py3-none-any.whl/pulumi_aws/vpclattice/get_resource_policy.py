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
    'GetResourcePolicyResult',
    'AwaitableGetResourcePolicyResult',
    'get_resource_policy',
    'get_resource_policy_output',
]

@pulumi.output_type
class GetResourcePolicyResult:
    """
    A collection of values returned by getResourcePolicy.
    """
    def __init__(__self__, id=None, policy=None, resource_arn=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if policy and not isinstance(policy, str):
            raise TypeError("Expected argument 'policy' to be a str")
        pulumi.set(__self__, "policy", policy)
        if resource_arn and not isinstance(resource_arn, str):
            raise TypeError("Expected argument 'resource_arn' to be a str")
        pulumi.set(__self__, "resource_arn", resource_arn)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def policy(self) -> str:
        """
        JSON-encoded string representation of the applied resource policy.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> str:
        return pulumi.get(self, "resource_arn")


class AwaitableGetResourcePolicyResult(GetResourcePolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResourcePolicyResult(
            id=self.id,
            policy=self.policy,
            resource_arn=self.resource_arn)


def get_resource_policy(resource_arn: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResourcePolicyResult:
    """
    Data source for managing an AWS VPC Lattice Resource Policy.

    ## Example Usage

    ### Basic Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.vpclattice.get_resource_policy(resource_arn=example_aws_vpclattice_service_network["arn"])
    ```
    <!--End PulumiCodeChooser -->


    :param str resource_arn: Resource ARN of the resource for which a policy is retrieved.
    """
    __args__ = dict()
    __args__['resourceArn'] = resource_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:vpclattice/getResourcePolicy:getResourcePolicy', __args__, opts=opts, typ=GetResourcePolicyResult).value

    return AwaitableGetResourcePolicyResult(
        id=pulumi.get(__ret__, 'id'),
        policy=pulumi.get(__ret__, 'policy'),
        resource_arn=pulumi.get(__ret__, 'resource_arn'))


@_utilities.lift_output_func(get_resource_policy)
def get_resource_policy_output(resource_arn: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetResourcePolicyResult]:
    """
    Data source for managing an AWS VPC Lattice Resource Policy.

    ## Example Usage

    ### Basic Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.vpclattice.get_resource_policy(resource_arn=example_aws_vpclattice_service_network["arn"])
    ```
    <!--End PulumiCodeChooser -->


    :param str resource_arn: Resource ARN of the resource for which a policy is retrieved.
    """
    ...
