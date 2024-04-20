# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ServiceSettingArgs', 'ServiceSetting']

@pulumi.input_type
class ServiceSettingArgs:
    def __init__(__self__, *,
                 setting_id: pulumi.Input[str],
                 setting_value: pulumi.Input[str]):
        """
        The set of arguments for constructing a ServiceSetting resource.
        :param pulumi.Input[str] setting_id: ID of the service setting.
        :param pulumi.Input[str] setting_value: Value of the service setting.
        """
        pulumi.set(__self__, "setting_id", setting_id)
        pulumi.set(__self__, "setting_value", setting_value)

    @property
    @pulumi.getter(name="settingId")
    def setting_id(self) -> pulumi.Input[str]:
        """
        ID of the service setting.
        """
        return pulumi.get(self, "setting_id")

    @setting_id.setter
    def setting_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "setting_id", value)

    @property
    @pulumi.getter(name="settingValue")
    def setting_value(self) -> pulumi.Input[str]:
        """
        Value of the service setting.
        """
        return pulumi.get(self, "setting_value")

    @setting_value.setter
    def setting_value(self, value: pulumi.Input[str]):
        pulumi.set(self, "setting_value", value)


@pulumi.input_type
class _ServiceSettingState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 setting_id: Optional[pulumi.Input[str]] = None,
                 setting_value: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ServiceSetting resources.
        :param pulumi.Input[str] arn: ARN of the service setting.
        :param pulumi.Input[str] setting_id: ID of the service setting.
        :param pulumi.Input[str] setting_value: Value of the service setting.
        :param pulumi.Input[str] status: Status of the service setting. Value can be `Default`, `Customized` or `PendingUpdate`.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if setting_id is not None:
            pulumi.set(__self__, "setting_id", setting_id)
        if setting_value is not None:
            pulumi.set(__self__, "setting_value", setting_value)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the service setting.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="settingId")
    def setting_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the service setting.
        """
        return pulumi.get(self, "setting_id")

    @setting_id.setter
    def setting_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "setting_id", value)

    @property
    @pulumi.getter(name="settingValue")
    def setting_value(self) -> Optional[pulumi.Input[str]]:
        """
        Value of the service setting.
        """
        return pulumi.get(self, "setting_value")

    @setting_value.setter
    def setting_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "setting_value", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Status of the service setting. Value can be `Default`, `Customized` or `PendingUpdate`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class ServiceSetting(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 setting_id: Optional[pulumi.Input[str]] = None,
                 setting_value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        This setting defines how a user interacts with or uses a service or a feature of a service.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        test_setting = aws.ssm.ServiceSetting("test_setting",
            setting_id="arn:aws:ssm:us-east-1:123456789012:servicesetting/ssm/parameter-store/high-throughput-enabled",
            setting_value="true")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import AWS SSM Service Setting using the `setting_id`. For example:

        ```sh
        $ pulumi import aws:ssm/serviceSetting:ServiceSetting example arn:aws:ssm:us-east-1:123456789012:servicesetting/ssm/parameter-store/high-throughput-enabled
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] setting_id: ID of the service setting.
        :param pulumi.Input[str] setting_value: Value of the service setting.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServiceSettingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This setting defines how a user interacts with or uses a service or a feature of a service.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        test_setting = aws.ssm.ServiceSetting("test_setting",
            setting_id="arn:aws:ssm:us-east-1:123456789012:servicesetting/ssm/parameter-store/high-throughput-enabled",
            setting_value="true")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import AWS SSM Service Setting using the `setting_id`. For example:

        ```sh
        $ pulumi import aws:ssm/serviceSetting:ServiceSetting example arn:aws:ssm:us-east-1:123456789012:servicesetting/ssm/parameter-store/high-throughput-enabled
        ```

        :param str resource_name: The name of the resource.
        :param ServiceSettingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceSettingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 setting_id: Optional[pulumi.Input[str]] = None,
                 setting_value: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServiceSettingArgs.__new__(ServiceSettingArgs)

            if setting_id is None and not opts.urn:
                raise TypeError("Missing required property 'setting_id'")
            __props__.__dict__["setting_id"] = setting_id
            if setting_value is None and not opts.urn:
                raise TypeError("Missing required property 'setting_value'")
            __props__.__dict__["setting_value"] = setting_value
            __props__.__dict__["arn"] = None
            __props__.__dict__["status"] = None
        super(ServiceSetting, __self__).__init__(
            'aws:ssm/serviceSetting:ServiceSetting',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            setting_id: Optional[pulumi.Input[str]] = None,
            setting_value: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'ServiceSetting':
        """
        Get an existing ServiceSetting resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN of the service setting.
        :param pulumi.Input[str] setting_id: ID of the service setting.
        :param pulumi.Input[str] setting_value: Value of the service setting.
        :param pulumi.Input[str] status: Status of the service setting. Value can be `Default`, `Customized` or `PendingUpdate`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServiceSettingState.__new__(_ServiceSettingState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["setting_id"] = setting_id
        __props__.__dict__["setting_value"] = setting_value
        __props__.__dict__["status"] = status
        return ServiceSetting(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the service setting.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="settingId")
    def setting_id(self) -> pulumi.Output[str]:
        """
        ID of the service setting.
        """
        return pulumi.get(self, "setting_id")

    @property
    @pulumi.getter(name="settingValue")
    def setting_value(self) -> pulumi.Output[str]:
        """
        Value of the service setting.
        """
        return pulumi.get(self, "setting_value")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Status of the service setting. Value can be `Default`, `Customized` or `PendingUpdate`.
        """
        return pulumi.get(self, "status")

