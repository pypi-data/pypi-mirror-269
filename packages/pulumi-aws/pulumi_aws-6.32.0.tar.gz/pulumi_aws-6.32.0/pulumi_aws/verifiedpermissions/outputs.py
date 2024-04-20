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
    'PolicyStoreValidationSettings',
    'SchemaDefinition',
    'GetPolicyStoreValidationSettingResult',
]

@pulumi.output_type
class PolicyStoreValidationSettings(dict):
    def __init__(__self__, *,
                 mode: str):
        """
        :param str mode: The mode for the validation settings. Valid values: `OFF`, `STRICT`.
               
               The following arguments are optional:
        """
        pulumi.set(__self__, "mode", mode)

    @property
    @pulumi.getter
    def mode(self) -> str:
        """
        The mode for the validation settings. Valid values: `OFF`, `STRICT`.

        The following arguments are optional:
        """
        return pulumi.get(self, "mode")


@pulumi.output_type
class SchemaDefinition(dict):
    def __init__(__self__, *,
                 value: str):
        """
        :param str value: A JSON string representation of the schema.
        """
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        A JSON string representation of the schema.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class GetPolicyStoreValidationSettingResult(dict):
    def __init__(__self__, *,
                 mode: str):
        pulumi.set(__self__, "mode", mode)

    @property
    @pulumi.getter
    def mode(self) -> str:
        return pulumi.get(self, "mode")


