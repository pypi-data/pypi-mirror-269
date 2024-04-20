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
    'GetOrganizationalUnitDescendantAccountsResult',
    'AwaitableGetOrganizationalUnitDescendantAccountsResult',
    'get_organizational_unit_descendant_accounts',
    'get_organizational_unit_descendant_accounts_output',
]

@pulumi.output_type
class GetOrganizationalUnitDescendantAccountsResult:
    """
    A collection of values returned by getOrganizationalUnitDescendantAccounts.
    """
    def __init__(__self__, accounts=None, id=None, parent_id=None):
        if accounts and not isinstance(accounts, list):
            raise TypeError("Expected argument 'accounts' to be a list")
        pulumi.set(__self__, "accounts", accounts)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if parent_id and not isinstance(parent_id, str):
            raise TypeError("Expected argument 'parent_id' to be a str")
        pulumi.set(__self__, "parent_id", parent_id)

    @property
    @pulumi.getter
    def accounts(self) -> Sequence['outputs.GetOrganizationalUnitDescendantAccountsAccountResult']:
        """
        List of child accounts, which have the following attributes:
        """
        return pulumi.get(self, "accounts")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="parentId")
    def parent_id(self) -> str:
        return pulumi.get(self, "parent_id")


class AwaitableGetOrganizationalUnitDescendantAccountsResult(GetOrganizationalUnitDescendantAccountsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOrganizationalUnitDescendantAccountsResult(
            accounts=self.accounts,
            id=self.id,
            parent_id=self.parent_id)


def get_organizational_unit_descendant_accounts(parent_id: Optional[str] = None,
                                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOrganizationalUnitDescendantAccountsResult:
    """
    Get all direct child accounts under a parent organizational unit. This provides all children.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    org = aws.organizations.get_organization()
    accounts = aws.organizations.get_organizational_unit_descendant_accounts(parent_id=org.roots[0].id)
    ```
    <!--End PulumiCodeChooser -->


    :param str parent_id: The parent ID of the accounts.
    """
    __args__ = dict()
    __args__['parentId'] = parent_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:organizations/getOrganizationalUnitDescendantAccounts:getOrganizationalUnitDescendantAccounts', __args__, opts=opts, typ=GetOrganizationalUnitDescendantAccountsResult).value

    return AwaitableGetOrganizationalUnitDescendantAccountsResult(
        accounts=pulumi.get(__ret__, 'accounts'),
        id=pulumi.get(__ret__, 'id'),
        parent_id=pulumi.get(__ret__, 'parent_id'))


@_utilities.lift_output_func(get_organizational_unit_descendant_accounts)
def get_organizational_unit_descendant_accounts_output(parent_id: Optional[pulumi.Input[str]] = None,
                                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOrganizationalUnitDescendantAccountsResult]:
    """
    Get all direct child accounts under a parent organizational unit. This provides all children.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    org = aws.organizations.get_organization()
    accounts = aws.organizations.get_organizational_unit_descendant_accounts(parent_id=org.roots[0].id)
    ```
    <!--End PulumiCodeChooser -->


    :param str parent_id: The parent ID of the accounts.
    """
    ...
