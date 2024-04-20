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
    'GetAccountAliasResult',
    'AwaitableGetAccountAliasResult',
    'get_account_alias',
    'get_account_alias_output',
]

@pulumi.output_type
class GetAccountAliasResult:
    """
    A collection of values returned by getAccountAlias.
    """
    def __init__(__self__, account_alias=None, id=None):
        if account_alias and not isinstance(account_alias, str):
            raise TypeError("Expected argument 'account_alias' to be a str")
        pulumi.set(__self__, "account_alias", account_alias)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter(name="accountAlias")
    def account_alias(self) -> str:
        """
        Alias associated with the AWS account.
        """
        return pulumi.get(self, "account_alias")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetAccountAliasResult(GetAccountAliasResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccountAliasResult(
            account_alias=self.account_alias,
            id=self.id)


def get_account_alias(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAccountAliasResult:
    """
    The IAM Account Alias data source allows access to the account alias
    for the effective account in which this provider is working.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    current = aws.iam.get_account_alias()
    pulumi.export("accountId", current.account_alias)
    ```
    <!--End PulumiCodeChooser -->
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:iam/getAccountAlias:getAccountAlias', __args__, opts=opts, typ=GetAccountAliasResult).value

    return AwaitableGetAccountAliasResult(
        account_alias=pulumi.get(__ret__, 'account_alias'),
        id=pulumi.get(__ret__, 'id'))


@_utilities.lift_output_func(get_account_alias)
def get_account_alias_output(opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAccountAliasResult]:
    """
    The IAM Account Alias data source allows access to the account alias
    for the effective account in which this provider is working.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    current = aws.iam.get_account_alias()
    pulumi.export("accountId", current.account_alias)
    ```
    <!--End PulumiCodeChooser -->
    """
    ...
