# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AccountArgs', 'Account']

@pulumi.input_type
class AccountArgs:
    def __init__(__self__, *,
                 auto_enable_controls: Optional[pulumi.Input[bool]] = None,
                 control_finding_generator: Optional[pulumi.Input[str]] = None,
                 enable_default_standards: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a Account resource.
        :param pulumi.Input[bool] auto_enable_controls: Whether to automatically enable new controls when they are added to standards that are enabled. By default, this is set to true, and new controls are enabled automatically. To not automatically enable new controls, set this to false.
        :param pulumi.Input[str] control_finding_generator: Updates whether the calling account has consolidated control findings turned on. If the value for this field is set to `SECURITY_CONTROL`, Security Hub generates a single finding for a control check even when the check applies to multiple enabled standards. If the value for this field is set to `STANDARD_CONTROL`, Security Hub generates separate findings for a control check when the check applies to multiple enabled standards. For accounts that are part of an organization, this value can only be updated in the administrator account.
        :param pulumi.Input[bool] enable_default_standards: Whether to enable the security standards that Security Hub has designated as automatically enabled including: ` AWS Foundational Security Best Practices v1.0.0` and `CIS AWS Foundations Benchmark v1.2.0`. Defaults to `true`.
        """
        if auto_enable_controls is not None:
            pulumi.set(__self__, "auto_enable_controls", auto_enable_controls)
        if control_finding_generator is not None:
            pulumi.set(__self__, "control_finding_generator", control_finding_generator)
        if enable_default_standards is not None:
            pulumi.set(__self__, "enable_default_standards", enable_default_standards)

    @property
    @pulumi.getter(name="autoEnableControls")
    def auto_enable_controls(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to automatically enable new controls when they are added to standards that are enabled. By default, this is set to true, and new controls are enabled automatically. To not automatically enable new controls, set this to false.
        """
        return pulumi.get(self, "auto_enable_controls")

    @auto_enable_controls.setter
    def auto_enable_controls(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_enable_controls", value)

    @property
    @pulumi.getter(name="controlFindingGenerator")
    def control_finding_generator(self) -> Optional[pulumi.Input[str]]:
        """
        Updates whether the calling account has consolidated control findings turned on. If the value for this field is set to `SECURITY_CONTROL`, Security Hub generates a single finding for a control check even when the check applies to multiple enabled standards. If the value for this field is set to `STANDARD_CONTROL`, Security Hub generates separate findings for a control check when the check applies to multiple enabled standards. For accounts that are part of an organization, this value can only be updated in the administrator account.
        """
        return pulumi.get(self, "control_finding_generator")

    @control_finding_generator.setter
    def control_finding_generator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "control_finding_generator", value)

    @property
    @pulumi.getter(name="enableDefaultStandards")
    def enable_default_standards(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to enable the security standards that Security Hub has designated as automatically enabled including: ` AWS Foundational Security Best Practices v1.0.0` and `CIS AWS Foundations Benchmark v1.2.0`. Defaults to `true`.
        """
        return pulumi.get(self, "enable_default_standards")

    @enable_default_standards.setter
    def enable_default_standards(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_default_standards", value)


@pulumi.input_type
class _AccountState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 auto_enable_controls: Optional[pulumi.Input[bool]] = None,
                 control_finding_generator: Optional[pulumi.Input[str]] = None,
                 enable_default_standards: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering Account resources.
        :param pulumi.Input[str] arn: ARN of the SecurityHub Hub created in the account.
        :param pulumi.Input[bool] auto_enable_controls: Whether to automatically enable new controls when they are added to standards that are enabled. By default, this is set to true, and new controls are enabled automatically. To not automatically enable new controls, set this to false.
        :param pulumi.Input[str] control_finding_generator: Updates whether the calling account has consolidated control findings turned on. If the value for this field is set to `SECURITY_CONTROL`, Security Hub generates a single finding for a control check even when the check applies to multiple enabled standards. If the value for this field is set to `STANDARD_CONTROL`, Security Hub generates separate findings for a control check when the check applies to multiple enabled standards. For accounts that are part of an organization, this value can only be updated in the administrator account.
        :param pulumi.Input[bool] enable_default_standards: Whether to enable the security standards that Security Hub has designated as automatically enabled including: ` AWS Foundational Security Best Practices v1.0.0` and `CIS AWS Foundations Benchmark v1.2.0`. Defaults to `true`.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if auto_enable_controls is not None:
            pulumi.set(__self__, "auto_enable_controls", auto_enable_controls)
        if control_finding_generator is not None:
            pulumi.set(__self__, "control_finding_generator", control_finding_generator)
        if enable_default_standards is not None:
            pulumi.set(__self__, "enable_default_standards", enable_default_standards)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the SecurityHub Hub created in the account.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="autoEnableControls")
    def auto_enable_controls(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to automatically enable new controls when they are added to standards that are enabled. By default, this is set to true, and new controls are enabled automatically. To not automatically enable new controls, set this to false.
        """
        return pulumi.get(self, "auto_enable_controls")

    @auto_enable_controls.setter
    def auto_enable_controls(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_enable_controls", value)

    @property
    @pulumi.getter(name="controlFindingGenerator")
    def control_finding_generator(self) -> Optional[pulumi.Input[str]]:
        """
        Updates whether the calling account has consolidated control findings turned on. If the value for this field is set to `SECURITY_CONTROL`, Security Hub generates a single finding for a control check even when the check applies to multiple enabled standards. If the value for this field is set to `STANDARD_CONTROL`, Security Hub generates separate findings for a control check when the check applies to multiple enabled standards. For accounts that are part of an organization, this value can only be updated in the administrator account.
        """
        return pulumi.get(self, "control_finding_generator")

    @control_finding_generator.setter
    def control_finding_generator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "control_finding_generator", value)

    @property
    @pulumi.getter(name="enableDefaultStandards")
    def enable_default_standards(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to enable the security standards that Security Hub has designated as automatically enabled including: ` AWS Foundational Security Best Practices v1.0.0` and `CIS AWS Foundations Benchmark v1.2.0`. Defaults to `true`.
        """
        return pulumi.get(self, "enable_default_standards")

    @enable_default_standards.setter
    def enable_default_standards(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_default_standards", value)


class Account(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_enable_controls: Optional[pulumi.Input[bool]] = None,
                 control_finding_generator: Optional[pulumi.Input[str]] = None,
                 enable_default_standards: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Enables Security Hub for this AWS account.

        > **NOTE:** Destroying this resource will disable Security Hub for this AWS account.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.securityhub.Account("example")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import an existing Security Hub enabled account using the AWS account ID. For example:

        ```sh
        $ pulumi import aws:securityhub/account:Account example 123456789012
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_enable_controls: Whether to automatically enable new controls when they are added to standards that are enabled. By default, this is set to true, and new controls are enabled automatically. To not automatically enable new controls, set this to false.
        :param pulumi.Input[str] control_finding_generator: Updates whether the calling account has consolidated control findings turned on. If the value for this field is set to `SECURITY_CONTROL`, Security Hub generates a single finding for a control check even when the check applies to multiple enabled standards. If the value for this field is set to `STANDARD_CONTROL`, Security Hub generates separate findings for a control check when the check applies to multiple enabled standards. For accounts that are part of an organization, this value can only be updated in the administrator account.
        :param pulumi.Input[bool] enable_default_standards: Whether to enable the security standards that Security Hub has designated as automatically enabled including: ` AWS Foundational Security Best Practices v1.0.0` and `CIS AWS Foundations Benchmark v1.2.0`. Defaults to `true`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[AccountArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Enables Security Hub for this AWS account.

        > **NOTE:** Destroying this resource will disable Security Hub for this AWS account.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.securityhub.Account("example")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import an existing Security Hub enabled account using the AWS account ID. For example:

        ```sh
        $ pulumi import aws:securityhub/account:Account example 123456789012
        ```

        :param str resource_name: The name of the resource.
        :param AccountArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccountArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_enable_controls: Optional[pulumi.Input[bool]] = None,
                 control_finding_generator: Optional[pulumi.Input[str]] = None,
                 enable_default_standards: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccountArgs.__new__(AccountArgs)

            __props__.__dict__["auto_enable_controls"] = auto_enable_controls
            __props__.__dict__["control_finding_generator"] = control_finding_generator
            __props__.__dict__["enable_default_standards"] = enable_default_standards
            __props__.__dict__["arn"] = None
        super(Account, __self__).__init__(
            'aws:securityhub/account:Account',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            auto_enable_controls: Optional[pulumi.Input[bool]] = None,
            control_finding_generator: Optional[pulumi.Input[str]] = None,
            enable_default_standards: Optional[pulumi.Input[bool]] = None) -> 'Account':
        """
        Get an existing Account resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN of the SecurityHub Hub created in the account.
        :param pulumi.Input[bool] auto_enable_controls: Whether to automatically enable new controls when they are added to standards that are enabled. By default, this is set to true, and new controls are enabled automatically. To not automatically enable new controls, set this to false.
        :param pulumi.Input[str] control_finding_generator: Updates whether the calling account has consolidated control findings turned on. If the value for this field is set to `SECURITY_CONTROL`, Security Hub generates a single finding for a control check even when the check applies to multiple enabled standards. If the value for this field is set to `STANDARD_CONTROL`, Security Hub generates separate findings for a control check when the check applies to multiple enabled standards. For accounts that are part of an organization, this value can only be updated in the administrator account.
        :param pulumi.Input[bool] enable_default_standards: Whether to enable the security standards that Security Hub has designated as automatically enabled including: ` AWS Foundational Security Best Practices v1.0.0` and `CIS AWS Foundations Benchmark v1.2.0`. Defaults to `true`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AccountState.__new__(_AccountState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["auto_enable_controls"] = auto_enable_controls
        __props__.__dict__["control_finding_generator"] = control_finding_generator
        __props__.__dict__["enable_default_standards"] = enable_default_standards
        return Account(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the SecurityHub Hub created in the account.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="autoEnableControls")
    def auto_enable_controls(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to automatically enable new controls when they are added to standards that are enabled. By default, this is set to true, and new controls are enabled automatically. To not automatically enable new controls, set this to false.
        """
        return pulumi.get(self, "auto_enable_controls")

    @property
    @pulumi.getter(name="controlFindingGenerator")
    def control_finding_generator(self) -> pulumi.Output[str]:
        """
        Updates whether the calling account has consolidated control findings turned on. If the value for this field is set to `SECURITY_CONTROL`, Security Hub generates a single finding for a control check even when the check applies to multiple enabled standards. If the value for this field is set to `STANDARD_CONTROL`, Security Hub generates separate findings for a control check when the check applies to multiple enabled standards. For accounts that are part of an organization, this value can only be updated in the administrator account.
        """
        return pulumi.get(self, "control_finding_generator")

    @property
    @pulumi.getter(name="enableDefaultStandards")
    def enable_default_standards(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to enable the security standards that Security Hub has designated as automatically enabled including: ` AWS Foundational Security Best Practices v1.0.0` and `CIS AWS Foundations Benchmark v1.2.0`. Defaults to `true`.
        """
        return pulumi.get(self, "enable_default_standards")

