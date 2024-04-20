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
    'GetMaintenanceWindowsResult',
    'AwaitableGetMaintenanceWindowsResult',
    'get_maintenance_windows',
    'get_maintenance_windows_output',
]

@pulumi.output_type
class GetMaintenanceWindowsResult:
    """
    A collection of values returned by getMaintenanceWindows.
    """
    def __init__(__self__, filters=None, id=None, ids=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetMaintenanceWindowsFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        """
        List of window IDs of the matched SSM maintenance windows.
        """
        return pulumi.get(self, "ids")


class AwaitableGetMaintenanceWindowsResult(GetMaintenanceWindowsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMaintenanceWindowsResult(
            filters=self.filters,
            id=self.id,
            ids=self.ids)


def get_maintenance_windows(filters: Optional[Sequence[pulumi.InputType['GetMaintenanceWindowsFilterArgs']]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMaintenanceWindowsResult:
    """
    Use this data source to get the window IDs of SSM maintenance windows.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ssm.get_maintenance_windows(filters=[aws.ssm.GetMaintenanceWindowsFilterArgs(
        name="Enabled",
        values=["true"],
    )])
    ```
    <!--End PulumiCodeChooser -->


    :param Sequence[pulumi.InputType['GetMaintenanceWindowsFilterArgs']] filters: Configuration block(s) for filtering. Detailed below.
    """
    __args__ = dict()
    __args__['filters'] = filters
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ssm/getMaintenanceWindows:getMaintenanceWindows', __args__, opts=opts, typ=GetMaintenanceWindowsResult).value

    return AwaitableGetMaintenanceWindowsResult(
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'))


@_utilities.lift_output_func(get_maintenance_windows)
def get_maintenance_windows_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetMaintenanceWindowsFilterArgs']]]]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMaintenanceWindowsResult]:
    """
    Use this data source to get the window IDs of SSM maintenance windows.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ssm.get_maintenance_windows(filters=[aws.ssm.GetMaintenanceWindowsFilterArgs(
        name="Enabled",
        values=["true"],
    )])
    ```
    <!--End PulumiCodeChooser -->


    :param Sequence[pulumi.InputType['GetMaintenanceWindowsFilterArgs']] filters: Configuration block(s) for filtering. Detailed below.
    """
    ...
