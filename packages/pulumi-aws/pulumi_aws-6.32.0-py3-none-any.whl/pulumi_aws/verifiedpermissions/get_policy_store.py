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
    'GetPolicyStoreResult',
    'AwaitableGetPolicyStoreResult',
    'get_policy_store',
    'get_policy_store_output',
]

@pulumi.output_type
class GetPolicyStoreResult:
    """
    A collection of values returned by getPolicyStore.
    """
    def __init__(__self__, arn=None, created_date=None, description=None, id=None, last_updated_date=None, validation_settings=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if created_date and not isinstance(created_date, str):
            raise TypeError("Expected argument 'created_date' to be a str")
        pulumi.set(__self__, "created_date", created_date)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_updated_date and not isinstance(last_updated_date, str):
            raise TypeError("Expected argument 'last_updated_date' to be a str")
        pulumi.set(__self__, "last_updated_date", last_updated_date)
        if validation_settings and not isinstance(validation_settings, list):
            raise TypeError("Expected argument 'validation_settings' to be a list")
        pulumi.set(__self__, "validation_settings", validation_settings)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The ARN of the Policy Store.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> str:
        """
        The date the Policy Store was created.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastUpdatedDate")
    def last_updated_date(self) -> str:
        """
        The date the Policy Store was last updated.
        """
        return pulumi.get(self, "last_updated_date")

    @property
    @pulumi.getter(name="validationSettings")
    def validation_settings(self) -> Sequence['outputs.GetPolicyStoreValidationSettingResult']:
        """
        Validation settings for the policy store.
        """
        return pulumi.get(self, "validation_settings")


class AwaitableGetPolicyStoreResult(GetPolicyStoreResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicyStoreResult(
            arn=self.arn,
            created_date=self.created_date,
            description=self.description,
            id=self.id,
            last_updated_date=self.last_updated_date,
            validation_settings=self.validation_settings)


def get_policy_store(id: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicyStoreResult:
    """
    Data source for managing an AWS Verified Permissions Policy Store.

    ## Example Usage

    ### Basic Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.verifiedpermissions.get_policy_store(id="example")
    ```
    <!--End PulumiCodeChooser -->


    :param str id: The ID of the Policy Store.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:verifiedpermissions/getPolicyStore:getPolicyStore', __args__, opts=opts, typ=GetPolicyStoreResult).value

    return AwaitableGetPolicyStoreResult(
        arn=pulumi.get(__ret__, 'arn'),
        created_date=pulumi.get(__ret__, 'created_date'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        last_updated_date=pulumi.get(__ret__, 'last_updated_date'),
        validation_settings=pulumi.get(__ret__, 'validation_settings'))


@_utilities.lift_output_func(get_policy_store)
def get_policy_store_output(id: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPolicyStoreResult]:
    """
    Data source for managing an AWS Verified Permissions Policy Store.

    ## Example Usage

    ### Basic Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.verifiedpermissions.get_policy_store(id="example")
    ```
    <!--End PulumiCodeChooser -->


    :param str id: The ID of the Policy Store.
    """
    ...
