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
    'CustomModelOutputDataConfigArgs',
    'CustomModelTimeoutsArgs',
    'CustomModelTrainingDataConfigArgs',
    'CustomModelTrainingMetricArgs',
    'CustomModelValidationDataConfigArgs',
    'CustomModelValidationDataConfigValidatorArgs',
    'CustomModelValidationMetricArgs',
    'CustomModelVpcConfigArgs',
    'ProvisionedModelThroughputTimeoutsArgs',
]

@pulumi.input_type
class CustomModelOutputDataConfigArgs:
    def __init__(__self__, *,
                 s3_uri: pulumi.Input[str]):
        """
        :param pulumi.Input[str] s3_uri: The S3 URI where the validation data is stored.
        """
        pulumi.set(__self__, "s3_uri", s3_uri)

    @property
    @pulumi.getter(name="s3Uri")
    def s3_uri(self) -> pulumi.Input[str]:
        """
        The S3 URI where the validation data is stored.
        """
        return pulumi.get(self, "s3_uri")

    @s3_uri.setter
    def s3_uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "s3_uri", value)


@pulumi.input_type
class CustomModelTimeoutsArgs:
    def __init__(__self__, *,
                 create: Optional[pulumi.Input[str]] = None,
                 delete: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] create: A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        :param pulumi.Input[str] delete: A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.
        """
        if create is not None:
            pulumi.set(__self__, "create", create)
        if delete is not None:
            pulumi.set(__self__, "delete", delete)

    @property
    @pulumi.getter
    def create(self) -> Optional[pulumi.Input[str]]:
        """
        A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        """
        return pulumi.get(self, "create")

    @create.setter
    def create(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create", value)

    @property
    @pulumi.getter
    def delete(self) -> Optional[pulumi.Input[str]]:
        """
        A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.
        """
        return pulumi.get(self, "delete")

    @delete.setter
    def delete(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "delete", value)


@pulumi.input_type
class CustomModelTrainingDataConfigArgs:
    def __init__(__self__, *,
                 s3_uri: pulumi.Input[str]):
        """
        :param pulumi.Input[str] s3_uri: The S3 URI where the validation data is stored.
        """
        pulumi.set(__self__, "s3_uri", s3_uri)

    @property
    @pulumi.getter(name="s3Uri")
    def s3_uri(self) -> pulumi.Input[str]:
        """
        The S3 URI where the validation data is stored.
        """
        return pulumi.get(self, "s3_uri")

    @s3_uri.setter
    def s3_uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "s3_uri", value)


@pulumi.input_type
class CustomModelTrainingMetricArgs:
    def __init__(__self__, *,
                 training_loss: pulumi.Input[float]):
        """
        :param pulumi.Input[float] training_loss: Loss metric associated with the customization job.
        """
        pulumi.set(__self__, "training_loss", training_loss)

    @property
    @pulumi.getter(name="trainingLoss")
    def training_loss(self) -> pulumi.Input[float]:
        """
        Loss metric associated with the customization job.
        """
        return pulumi.get(self, "training_loss")

    @training_loss.setter
    def training_loss(self, value: pulumi.Input[float]):
        pulumi.set(self, "training_loss", value)


@pulumi.input_type
class CustomModelValidationDataConfigArgs:
    def __init__(__self__, *,
                 validators: Optional[pulumi.Input[Sequence[pulumi.Input['CustomModelValidationDataConfigValidatorArgs']]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input['CustomModelValidationDataConfigValidatorArgs']]] validators: Information about the validators.
        """
        if validators is not None:
            pulumi.set(__self__, "validators", validators)

    @property
    @pulumi.getter
    def validators(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CustomModelValidationDataConfigValidatorArgs']]]]:
        """
        Information about the validators.
        """
        return pulumi.get(self, "validators")

    @validators.setter
    def validators(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CustomModelValidationDataConfigValidatorArgs']]]]):
        pulumi.set(self, "validators", value)


@pulumi.input_type
class CustomModelValidationDataConfigValidatorArgs:
    def __init__(__self__, *,
                 s3_uri: pulumi.Input[str]):
        """
        :param pulumi.Input[str] s3_uri: The S3 URI where the validation data is stored.
        """
        pulumi.set(__self__, "s3_uri", s3_uri)

    @property
    @pulumi.getter(name="s3Uri")
    def s3_uri(self) -> pulumi.Input[str]:
        """
        The S3 URI where the validation data is stored.
        """
        return pulumi.get(self, "s3_uri")

    @s3_uri.setter
    def s3_uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "s3_uri", value)


@pulumi.input_type
class CustomModelValidationMetricArgs:
    def __init__(__self__, *,
                 validation_loss: pulumi.Input[float]):
        """
        :param pulumi.Input[float] validation_loss: The validation loss associated with the validator.
        """
        pulumi.set(__self__, "validation_loss", validation_loss)

    @property
    @pulumi.getter(name="validationLoss")
    def validation_loss(self) -> pulumi.Input[float]:
        """
        The validation loss associated with the validator.
        """
        return pulumi.get(self, "validation_loss")

    @validation_loss.setter
    def validation_loss(self, value: pulumi.Input[float]):
        pulumi.set(self, "validation_loss", value)


@pulumi.input_type
class CustomModelVpcConfigArgs:
    def __init__(__self__, *,
                 security_group_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 subnet_ids: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_ids: VPC configuration security group IDs.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: VPC configuration subnets.
        """
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        pulumi.set(__self__, "subnet_ids", subnet_ids)

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        VPC configuration security group IDs.
        """
        return pulumi.get(self, "security_group_ids")

    @security_group_ids.setter
    def security_group_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "security_group_ids", value)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        VPC configuration subnets.
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "subnet_ids", value)


@pulumi.input_type
class ProvisionedModelThroughputTimeoutsArgs:
    def __init__(__self__, *,
                 create: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] create: A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        """
        if create is not None:
            pulumi.set(__self__, "create", create)

    @property
    @pulumi.getter
    def create(self) -> Optional[pulumi.Input[str]]:
        """
        A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        """
        return pulumi.get(self, "create")

    @create.setter
    def create(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create", value)


