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

__all__ = ['ConfigurationSetArgs', 'ConfigurationSet']

@pulumi.input_type
class ConfigurationSetArgs:
    def __init__(__self__, *,
                 configuration_set_name: pulumi.Input[str],
                 delivery_options: Optional[pulumi.Input['ConfigurationSetDeliveryOptionsArgs']] = None,
                 reputation_options: Optional[pulumi.Input['ConfigurationSetReputationOptionsArgs']] = None,
                 sending_options: Optional[pulumi.Input['ConfigurationSetSendingOptionsArgs']] = None,
                 suppression_options: Optional[pulumi.Input['ConfigurationSetSuppressionOptionsArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tracking_options: Optional[pulumi.Input['ConfigurationSetTrackingOptionsArgs']] = None,
                 vdm_options: Optional[pulumi.Input['ConfigurationSetVdmOptionsArgs']] = None):
        """
        The set of arguments for constructing a ConfigurationSet resource.
        :param pulumi.Input[str] configuration_set_name: The name of the configuration set.
        :param pulumi.Input['ConfigurationSetDeliveryOptionsArgs'] delivery_options: An object that defines the dedicated IP pool that is used to send emails that you send using the configuration set.
        :param pulumi.Input['ConfigurationSetReputationOptionsArgs'] reputation_options: An object that defines whether or not Amazon SES collects reputation metrics for the emails that you send that use the configuration set.
        :param pulumi.Input['ConfigurationSetSendingOptionsArgs'] sending_options: An object that defines whether or not Amazon SES can send email that you send using the configuration set.
        :param pulumi.Input['ConfigurationSetSuppressionOptionsArgs'] suppression_options: An object that contains information about the suppression list preferences for your account.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the service. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input['ConfigurationSetTrackingOptionsArgs'] tracking_options: An object that defines the open and click tracking options for emails that you send using the configuration set.
        :param pulumi.Input['ConfigurationSetVdmOptionsArgs'] vdm_options: An object that defines the VDM settings that apply to emails that you send using the configuration set.
        """
        pulumi.set(__self__, "configuration_set_name", configuration_set_name)
        if delivery_options is not None:
            pulumi.set(__self__, "delivery_options", delivery_options)
        if reputation_options is not None:
            pulumi.set(__self__, "reputation_options", reputation_options)
        if sending_options is not None:
            pulumi.set(__self__, "sending_options", sending_options)
        if suppression_options is not None:
            pulumi.set(__self__, "suppression_options", suppression_options)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tracking_options is not None:
            pulumi.set(__self__, "tracking_options", tracking_options)
        if vdm_options is not None:
            pulumi.set(__self__, "vdm_options", vdm_options)

    @property
    @pulumi.getter(name="configurationSetName")
    def configuration_set_name(self) -> pulumi.Input[str]:
        """
        The name of the configuration set.
        """
        return pulumi.get(self, "configuration_set_name")

    @configuration_set_name.setter
    def configuration_set_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "configuration_set_name", value)

    @property
    @pulumi.getter(name="deliveryOptions")
    def delivery_options(self) -> Optional[pulumi.Input['ConfigurationSetDeliveryOptionsArgs']]:
        """
        An object that defines the dedicated IP pool that is used to send emails that you send using the configuration set.
        """
        return pulumi.get(self, "delivery_options")

    @delivery_options.setter
    def delivery_options(self, value: Optional[pulumi.Input['ConfigurationSetDeliveryOptionsArgs']]):
        pulumi.set(self, "delivery_options", value)

    @property
    @pulumi.getter(name="reputationOptions")
    def reputation_options(self) -> Optional[pulumi.Input['ConfigurationSetReputationOptionsArgs']]:
        """
        An object that defines whether or not Amazon SES collects reputation metrics for the emails that you send that use the configuration set.
        """
        return pulumi.get(self, "reputation_options")

    @reputation_options.setter
    def reputation_options(self, value: Optional[pulumi.Input['ConfigurationSetReputationOptionsArgs']]):
        pulumi.set(self, "reputation_options", value)

    @property
    @pulumi.getter(name="sendingOptions")
    def sending_options(self) -> Optional[pulumi.Input['ConfigurationSetSendingOptionsArgs']]:
        """
        An object that defines whether or not Amazon SES can send email that you send using the configuration set.
        """
        return pulumi.get(self, "sending_options")

    @sending_options.setter
    def sending_options(self, value: Optional[pulumi.Input['ConfigurationSetSendingOptionsArgs']]):
        pulumi.set(self, "sending_options", value)

    @property
    @pulumi.getter(name="suppressionOptions")
    def suppression_options(self) -> Optional[pulumi.Input['ConfigurationSetSuppressionOptionsArgs']]:
        """
        An object that contains information about the suppression list preferences for your account.
        """
        return pulumi.get(self, "suppression_options")

    @suppression_options.setter
    def suppression_options(self, value: Optional[pulumi.Input['ConfigurationSetSuppressionOptionsArgs']]):
        pulumi.set(self, "suppression_options", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the service. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="trackingOptions")
    def tracking_options(self) -> Optional[pulumi.Input['ConfigurationSetTrackingOptionsArgs']]:
        """
        An object that defines the open and click tracking options for emails that you send using the configuration set.
        """
        return pulumi.get(self, "tracking_options")

    @tracking_options.setter
    def tracking_options(self, value: Optional[pulumi.Input['ConfigurationSetTrackingOptionsArgs']]):
        pulumi.set(self, "tracking_options", value)

    @property
    @pulumi.getter(name="vdmOptions")
    def vdm_options(self) -> Optional[pulumi.Input['ConfigurationSetVdmOptionsArgs']]:
        """
        An object that defines the VDM settings that apply to emails that you send using the configuration set.
        """
        return pulumi.get(self, "vdm_options")

    @vdm_options.setter
    def vdm_options(self, value: Optional[pulumi.Input['ConfigurationSetVdmOptionsArgs']]):
        pulumi.set(self, "vdm_options", value)


@pulumi.input_type
class _ConfigurationSetState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 configuration_set_name: Optional[pulumi.Input[str]] = None,
                 delivery_options: Optional[pulumi.Input['ConfigurationSetDeliveryOptionsArgs']] = None,
                 reputation_options: Optional[pulumi.Input['ConfigurationSetReputationOptionsArgs']] = None,
                 sending_options: Optional[pulumi.Input['ConfigurationSetSendingOptionsArgs']] = None,
                 suppression_options: Optional[pulumi.Input['ConfigurationSetSuppressionOptionsArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tracking_options: Optional[pulumi.Input['ConfigurationSetTrackingOptionsArgs']] = None,
                 vdm_options: Optional[pulumi.Input['ConfigurationSetVdmOptionsArgs']] = None):
        """
        Input properties used for looking up and filtering ConfigurationSet resources.
        :param pulumi.Input[str] arn: ARN of the Configuration Set.
        :param pulumi.Input[str] configuration_set_name: The name of the configuration set.
        :param pulumi.Input['ConfigurationSetDeliveryOptionsArgs'] delivery_options: An object that defines the dedicated IP pool that is used to send emails that you send using the configuration set.
        :param pulumi.Input['ConfigurationSetReputationOptionsArgs'] reputation_options: An object that defines whether or not Amazon SES collects reputation metrics for the emails that you send that use the configuration set.
        :param pulumi.Input['ConfigurationSetSendingOptionsArgs'] sending_options: An object that defines whether or not Amazon SES can send email that you send using the configuration set.
        :param pulumi.Input['ConfigurationSetSuppressionOptionsArgs'] suppression_options: An object that contains information about the suppression list preferences for your account.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the service. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input['ConfigurationSetTrackingOptionsArgs'] tracking_options: An object that defines the open and click tracking options for emails that you send using the configuration set.
        :param pulumi.Input['ConfigurationSetVdmOptionsArgs'] vdm_options: An object that defines the VDM settings that apply to emails that you send using the configuration set.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if configuration_set_name is not None:
            pulumi.set(__self__, "configuration_set_name", configuration_set_name)
        if delivery_options is not None:
            pulumi.set(__self__, "delivery_options", delivery_options)
        if reputation_options is not None:
            pulumi.set(__self__, "reputation_options", reputation_options)
        if sending_options is not None:
            pulumi.set(__self__, "sending_options", sending_options)
        if suppression_options is not None:
            pulumi.set(__self__, "suppression_options", suppression_options)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if tracking_options is not None:
            pulumi.set(__self__, "tracking_options", tracking_options)
        if vdm_options is not None:
            pulumi.set(__self__, "vdm_options", vdm_options)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the Configuration Set.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="configurationSetName")
    def configuration_set_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the configuration set.
        """
        return pulumi.get(self, "configuration_set_name")

    @configuration_set_name.setter
    def configuration_set_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "configuration_set_name", value)

    @property
    @pulumi.getter(name="deliveryOptions")
    def delivery_options(self) -> Optional[pulumi.Input['ConfigurationSetDeliveryOptionsArgs']]:
        """
        An object that defines the dedicated IP pool that is used to send emails that you send using the configuration set.
        """
        return pulumi.get(self, "delivery_options")

    @delivery_options.setter
    def delivery_options(self, value: Optional[pulumi.Input['ConfigurationSetDeliveryOptionsArgs']]):
        pulumi.set(self, "delivery_options", value)

    @property
    @pulumi.getter(name="reputationOptions")
    def reputation_options(self) -> Optional[pulumi.Input['ConfigurationSetReputationOptionsArgs']]:
        """
        An object that defines whether or not Amazon SES collects reputation metrics for the emails that you send that use the configuration set.
        """
        return pulumi.get(self, "reputation_options")

    @reputation_options.setter
    def reputation_options(self, value: Optional[pulumi.Input['ConfigurationSetReputationOptionsArgs']]):
        pulumi.set(self, "reputation_options", value)

    @property
    @pulumi.getter(name="sendingOptions")
    def sending_options(self) -> Optional[pulumi.Input['ConfigurationSetSendingOptionsArgs']]:
        """
        An object that defines whether or not Amazon SES can send email that you send using the configuration set.
        """
        return pulumi.get(self, "sending_options")

    @sending_options.setter
    def sending_options(self, value: Optional[pulumi.Input['ConfigurationSetSendingOptionsArgs']]):
        pulumi.set(self, "sending_options", value)

    @property
    @pulumi.getter(name="suppressionOptions")
    def suppression_options(self) -> Optional[pulumi.Input['ConfigurationSetSuppressionOptionsArgs']]:
        """
        An object that contains information about the suppression list preferences for your account.
        """
        return pulumi.get(self, "suppression_options")

    @suppression_options.setter
    def suppression_options(self, value: Optional[pulumi.Input['ConfigurationSetSuppressionOptionsArgs']]):
        pulumi.set(self, "suppression_options", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the service. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter(name="trackingOptions")
    def tracking_options(self) -> Optional[pulumi.Input['ConfigurationSetTrackingOptionsArgs']]:
        """
        An object that defines the open and click tracking options for emails that you send using the configuration set.
        """
        return pulumi.get(self, "tracking_options")

    @tracking_options.setter
    def tracking_options(self, value: Optional[pulumi.Input['ConfigurationSetTrackingOptionsArgs']]):
        pulumi.set(self, "tracking_options", value)

    @property
    @pulumi.getter(name="vdmOptions")
    def vdm_options(self) -> Optional[pulumi.Input['ConfigurationSetVdmOptionsArgs']]:
        """
        An object that defines the VDM settings that apply to emails that you send using the configuration set.
        """
        return pulumi.get(self, "vdm_options")

    @vdm_options.setter
    def vdm_options(self, value: Optional[pulumi.Input['ConfigurationSetVdmOptionsArgs']]):
        pulumi.set(self, "vdm_options", value)


class ConfigurationSet(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration_set_name: Optional[pulumi.Input[str]] = None,
                 delivery_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetDeliveryOptionsArgs']]] = None,
                 reputation_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetReputationOptionsArgs']]] = None,
                 sending_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetSendingOptionsArgs']]] = None,
                 suppression_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetSuppressionOptionsArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tracking_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetTrackingOptionsArgs']]] = None,
                 vdm_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetVdmOptionsArgs']]] = None,
                 __props__=None):
        """
        Resource for managing an AWS SESv2 (Simple Email V2) Configuration Set.

        ## Example Usage

        ### Basic Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sesv2.ConfigurationSet("example",
            configuration_set_name="example",
            delivery_options=aws.sesv2.ConfigurationSetDeliveryOptionsArgs(
                tls_policy="REQUIRE",
            ),
            reputation_options=aws.sesv2.ConfigurationSetReputationOptionsArgs(
                reputation_metrics_enabled=False,
            ),
            sending_options=aws.sesv2.ConfigurationSetSendingOptionsArgs(
                sending_enabled=True,
            ),
            suppression_options=aws.sesv2.ConfigurationSetSuppressionOptionsArgs(
                suppressed_reasons=[
                    "BOUNCE",
                    "COMPLAINT",
                ],
            ),
            tracking_options=aws.sesv2.ConfigurationSetTrackingOptionsArgs(
                custom_redirect_domain="example.com",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import SESv2 (Simple Email V2) Configuration Set using the `configuration_set_name`. For example:

        ```sh
        $ pulumi import aws:sesv2/configurationSet:ConfigurationSet example example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] configuration_set_name: The name of the configuration set.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetDeliveryOptionsArgs']] delivery_options: An object that defines the dedicated IP pool that is used to send emails that you send using the configuration set.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetReputationOptionsArgs']] reputation_options: An object that defines whether or not Amazon SES collects reputation metrics for the emails that you send that use the configuration set.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetSendingOptionsArgs']] sending_options: An object that defines whether or not Amazon SES can send email that you send using the configuration set.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetSuppressionOptionsArgs']] suppression_options: An object that contains information about the suppression list preferences for your account.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the service. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetTrackingOptionsArgs']] tracking_options: An object that defines the open and click tracking options for emails that you send using the configuration set.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetVdmOptionsArgs']] vdm_options: An object that defines the VDM settings that apply to emails that you send using the configuration set.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConfigurationSetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS SESv2 (Simple Email V2) Configuration Set.

        ## Example Usage

        ### Basic Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sesv2.ConfigurationSet("example",
            configuration_set_name="example",
            delivery_options=aws.sesv2.ConfigurationSetDeliveryOptionsArgs(
                tls_policy="REQUIRE",
            ),
            reputation_options=aws.sesv2.ConfigurationSetReputationOptionsArgs(
                reputation_metrics_enabled=False,
            ),
            sending_options=aws.sesv2.ConfigurationSetSendingOptionsArgs(
                sending_enabled=True,
            ),
            suppression_options=aws.sesv2.ConfigurationSetSuppressionOptionsArgs(
                suppressed_reasons=[
                    "BOUNCE",
                    "COMPLAINT",
                ],
            ),
            tracking_options=aws.sesv2.ConfigurationSetTrackingOptionsArgs(
                custom_redirect_domain="example.com",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import SESv2 (Simple Email V2) Configuration Set using the `configuration_set_name`. For example:

        ```sh
        $ pulumi import aws:sesv2/configurationSet:ConfigurationSet example example
        ```

        :param str resource_name: The name of the resource.
        :param ConfigurationSetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConfigurationSetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration_set_name: Optional[pulumi.Input[str]] = None,
                 delivery_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetDeliveryOptionsArgs']]] = None,
                 reputation_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetReputationOptionsArgs']]] = None,
                 sending_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetSendingOptionsArgs']]] = None,
                 suppression_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetSuppressionOptionsArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tracking_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetTrackingOptionsArgs']]] = None,
                 vdm_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetVdmOptionsArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConfigurationSetArgs.__new__(ConfigurationSetArgs)

            if configuration_set_name is None and not opts.urn:
                raise TypeError("Missing required property 'configuration_set_name'")
            __props__.__dict__["configuration_set_name"] = configuration_set_name
            __props__.__dict__["delivery_options"] = delivery_options
            __props__.__dict__["reputation_options"] = reputation_options
            __props__.__dict__["sending_options"] = sending_options
            __props__.__dict__["suppression_options"] = suppression_options
            __props__.__dict__["tags"] = tags
            __props__.__dict__["tracking_options"] = tracking_options
            __props__.__dict__["vdm_options"] = vdm_options
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(ConfigurationSet, __self__).__init__(
            'aws:sesv2/configurationSet:ConfigurationSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            configuration_set_name: Optional[pulumi.Input[str]] = None,
            delivery_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetDeliveryOptionsArgs']]] = None,
            reputation_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetReputationOptionsArgs']]] = None,
            sending_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetSendingOptionsArgs']]] = None,
            suppression_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetSuppressionOptionsArgs']]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tracking_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetTrackingOptionsArgs']]] = None,
            vdm_options: Optional[pulumi.Input[pulumi.InputType['ConfigurationSetVdmOptionsArgs']]] = None) -> 'ConfigurationSet':
        """
        Get an existing ConfigurationSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN of the Configuration Set.
        :param pulumi.Input[str] configuration_set_name: The name of the configuration set.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetDeliveryOptionsArgs']] delivery_options: An object that defines the dedicated IP pool that is used to send emails that you send using the configuration set.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetReputationOptionsArgs']] reputation_options: An object that defines whether or not Amazon SES collects reputation metrics for the emails that you send that use the configuration set.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetSendingOptionsArgs']] sending_options: An object that defines whether or not Amazon SES can send email that you send using the configuration set.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetSuppressionOptionsArgs']] suppression_options: An object that contains information about the suppression list preferences for your account.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the service. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetTrackingOptionsArgs']] tracking_options: An object that defines the open and click tracking options for emails that you send using the configuration set.
        :param pulumi.Input[pulumi.InputType['ConfigurationSetVdmOptionsArgs']] vdm_options: An object that defines the VDM settings that apply to emails that you send using the configuration set.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ConfigurationSetState.__new__(_ConfigurationSetState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["configuration_set_name"] = configuration_set_name
        __props__.__dict__["delivery_options"] = delivery_options
        __props__.__dict__["reputation_options"] = reputation_options
        __props__.__dict__["sending_options"] = sending_options
        __props__.__dict__["suppression_options"] = suppression_options
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["tracking_options"] = tracking_options
        __props__.__dict__["vdm_options"] = vdm_options
        return ConfigurationSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the Configuration Set.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="configurationSetName")
    def configuration_set_name(self) -> pulumi.Output[str]:
        """
        The name of the configuration set.
        """
        return pulumi.get(self, "configuration_set_name")

    @property
    @pulumi.getter(name="deliveryOptions")
    def delivery_options(self) -> pulumi.Output[Optional['outputs.ConfigurationSetDeliveryOptions']]:
        """
        An object that defines the dedicated IP pool that is used to send emails that you send using the configuration set.
        """
        return pulumi.get(self, "delivery_options")

    @property
    @pulumi.getter(name="reputationOptions")
    def reputation_options(self) -> pulumi.Output['outputs.ConfigurationSetReputationOptions']:
        """
        An object that defines whether or not Amazon SES collects reputation metrics for the emails that you send that use the configuration set.
        """
        return pulumi.get(self, "reputation_options")

    @property
    @pulumi.getter(name="sendingOptions")
    def sending_options(self) -> pulumi.Output['outputs.ConfigurationSetSendingOptions']:
        """
        An object that defines whether or not Amazon SES can send email that you send using the configuration set.
        """
        return pulumi.get(self, "sending_options")

    @property
    @pulumi.getter(name="suppressionOptions")
    def suppression_options(self) -> pulumi.Output[Optional['outputs.ConfigurationSetSuppressionOptions']]:
        """
        An object that contains information about the suppression list preferences for your account.
        """
        return pulumi.get(self, "suppression_options")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the service. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter(name="trackingOptions")
    def tracking_options(self) -> pulumi.Output[Optional['outputs.ConfigurationSetTrackingOptions']]:
        """
        An object that defines the open and click tracking options for emails that you send using the configuration set.
        """
        return pulumi.get(self, "tracking_options")

    @property
    @pulumi.getter(name="vdmOptions")
    def vdm_options(self) -> pulumi.Output[Optional['outputs.ConfigurationSetVdmOptions']]:
        """
        An object that defines the VDM settings that apply to emails that you send using the configuration set.
        """
        return pulumi.get(self, "vdm_options")

