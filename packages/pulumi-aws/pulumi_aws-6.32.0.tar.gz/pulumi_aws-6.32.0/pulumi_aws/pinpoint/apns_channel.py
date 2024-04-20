# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ApnsChannelArgs', 'ApnsChannel']

@pulumi.input_type
class ApnsChannelArgs:
    def __init__(__self__, *,
                 application_id: pulumi.Input[str],
                 bundle_id: Optional[pulumi.Input[str]] = None,
                 certificate: Optional[pulumi.Input[str]] = None,
                 default_authentication_method: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 private_key: Optional[pulumi.Input[str]] = None,
                 team_id: Optional[pulumi.Input[str]] = None,
                 token_key: Optional[pulumi.Input[str]] = None,
                 token_key_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ApnsChannel resource.
        :param pulumi.Input[str] application_id: The application ID.
        :param pulumi.Input[str] bundle_id: The ID assigned to your iOS app. To find this value, choose Certificates, IDs & Profiles, choose App IDs in the Identifiers section, and choose your app.
        :param pulumi.Input[str] certificate: The pem encoded TLS Certificate from Apple.
        :param pulumi.Input[str] default_authentication_method: The default authentication method used for APNs.
               __NOTE__: Amazon Pinpoint uses this default for every APNs push notification that you send using the console.
               You can override the default when you send a message programmatically using the Amazon Pinpoint API, the AWS CLI, or an AWS SDK.
               If your default authentication type fails, Amazon Pinpoint doesn't attempt to use the other authentication type.
               
               One of the following sets of credentials is also required.
               
               If you choose to use __Certificate credentials__ you will have to provide:
        :param pulumi.Input[bool] enabled: Whether the channel is enabled or disabled. Defaults to `true`.
        :param pulumi.Input[str] private_key: The Certificate Private Key file (ie. `.key` file).
               
               If you choose to use __Key credentials__ you will have to provide:
        :param pulumi.Input[str] team_id: The ID assigned to your Apple developer account team. This value is provided on the Membership page.
        :param pulumi.Input[str] token_key: The `.p8` file that you download from your Apple developer account when you create an authentication key.
        :param pulumi.Input[str] token_key_id: The ID assigned to your signing key. To find this value, choose Certificates, IDs & Profiles, and choose your key in the Keys section.
        """
        pulumi.set(__self__, "application_id", application_id)
        if bundle_id is not None:
            pulumi.set(__self__, "bundle_id", bundle_id)
        if certificate is not None:
            pulumi.set(__self__, "certificate", certificate)
        if default_authentication_method is not None:
            pulumi.set(__self__, "default_authentication_method", default_authentication_method)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if private_key is not None:
            pulumi.set(__self__, "private_key", private_key)
        if team_id is not None:
            pulumi.set(__self__, "team_id", team_id)
        if token_key is not None:
            pulumi.set(__self__, "token_key", token_key)
        if token_key_id is not None:
            pulumi.set(__self__, "token_key_id", token_key_id)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> pulumi.Input[str]:
        """
        The application ID.
        """
        return pulumi.get(self, "application_id")

    @application_id.setter
    def application_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "application_id", value)

    @property
    @pulumi.getter(name="bundleId")
    def bundle_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID assigned to your iOS app. To find this value, choose Certificates, IDs & Profiles, choose App IDs in the Identifiers section, and choose your app.
        """
        return pulumi.get(self, "bundle_id")

    @bundle_id.setter
    def bundle_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bundle_id", value)

    @property
    @pulumi.getter
    def certificate(self) -> Optional[pulumi.Input[str]]:
        """
        The pem encoded TLS Certificate from Apple.
        """
        return pulumi.get(self, "certificate")

    @certificate.setter
    def certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate", value)

    @property
    @pulumi.getter(name="defaultAuthenticationMethod")
    def default_authentication_method(self) -> Optional[pulumi.Input[str]]:
        """
        The default authentication method used for APNs.
        __NOTE__: Amazon Pinpoint uses this default for every APNs push notification that you send using the console.
        You can override the default when you send a message programmatically using the Amazon Pinpoint API, the AWS CLI, or an AWS SDK.
        If your default authentication type fails, Amazon Pinpoint doesn't attempt to use the other authentication type.

        One of the following sets of credentials is also required.

        If you choose to use __Certificate credentials__ you will have to provide:
        """
        return pulumi.get(self, "default_authentication_method")

    @default_authentication_method.setter
    def default_authentication_method(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_authentication_method", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the channel is enabled or disabled. Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="privateKey")
    def private_key(self) -> Optional[pulumi.Input[str]]:
        """
        The Certificate Private Key file (ie. `.key` file).

        If you choose to use __Key credentials__ you will have to provide:
        """
        return pulumi.get(self, "private_key")

    @private_key.setter
    def private_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_key", value)

    @property
    @pulumi.getter(name="teamId")
    def team_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID assigned to your Apple developer account team. This value is provided on the Membership page.
        """
        return pulumi.get(self, "team_id")

    @team_id.setter
    def team_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "team_id", value)

    @property
    @pulumi.getter(name="tokenKey")
    def token_key(self) -> Optional[pulumi.Input[str]]:
        """
        The `.p8` file that you download from your Apple developer account when you create an authentication key.
        """
        return pulumi.get(self, "token_key")

    @token_key.setter
    def token_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token_key", value)

    @property
    @pulumi.getter(name="tokenKeyId")
    def token_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID assigned to your signing key. To find this value, choose Certificates, IDs & Profiles, and choose your key in the Keys section.
        """
        return pulumi.get(self, "token_key_id")

    @token_key_id.setter
    def token_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token_key_id", value)


@pulumi.input_type
class _ApnsChannelState:
    def __init__(__self__, *,
                 application_id: Optional[pulumi.Input[str]] = None,
                 bundle_id: Optional[pulumi.Input[str]] = None,
                 certificate: Optional[pulumi.Input[str]] = None,
                 default_authentication_method: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 private_key: Optional[pulumi.Input[str]] = None,
                 team_id: Optional[pulumi.Input[str]] = None,
                 token_key: Optional[pulumi.Input[str]] = None,
                 token_key_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ApnsChannel resources.
        :param pulumi.Input[str] application_id: The application ID.
        :param pulumi.Input[str] bundle_id: The ID assigned to your iOS app. To find this value, choose Certificates, IDs & Profiles, choose App IDs in the Identifiers section, and choose your app.
        :param pulumi.Input[str] certificate: The pem encoded TLS Certificate from Apple.
        :param pulumi.Input[str] default_authentication_method: The default authentication method used for APNs.
               __NOTE__: Amazon Pinpoint uses this default for every APNs push notification that you send using the console.
               You can override the default when you send a message programmatically using the Amazon Pinpoint API, the AWS CLI, or an AWS SDK.
               If your default authentication type fails, Amazon Pinpoint doesn't attempt to use the other authentication type.
               
               One of the following sets of credentials is also required.
               
               If you choose to use __Certificate credentials__ you will have to provide:
        :param pulumi.Input[bool] enabled: Whether the channel is enabled or disabled. Defaults to `true`.
        :param pulumi.Input[str] private_key: The Certificate Private Key file (ie. `.key` file).
               
               If you choose to use __Key credentials__ you will have to provide:
        :param pulumi.Input[str] team_id: The ID assigned to your Apple developer account team. This value is provided on the Membership page.
        :param pulumi.Input[str] token_key: The `.p8` file that you download from your Apple developer account when you create an authentication key.
        :param pulumi.Input[str] token_key_id: The ID assigned to your signing key. To find this value, choose Certificates, IDs & Profiles, and choose your key in the Keys section.
        """
        if application_id is not None:
            pulumi.set(__self__, "application_id", application_id)
        if bundle_id is not None:
            pulumi.set(__self__, "bundle_id", bundle_id)
        if certificate is not None:
            pulumi.set(__self__, "certificate", certificate)
        if default_authentication_method is not None:
            pulumi.set(__self__, "default_authentication_method", default_authentication_method)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if private_key is not None:
            pulumi.set(__self__, "private_key", private_key)
        if team_id is not None:
            pulumi.set(__self__, "team_id", team_id)
        if token_key is not None:
            pulumi.set(__self__, "token_key", token_key)
        if token_key_id is not None:
            pulumi.set(__self__, "token_key_id", token_key_id)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> Optional[pulumi.Input[str]]:
        """
        The application ID.
        """
        return pulumi.get(self, "application_id")

    @application_id.setter
    def application_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "application_id", value)

    @property
    @pulumi.getter(name="bundleId")
    def bundle_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID assigned to your iOS app. To find this value, choose Certificates, IDs & Profiles, choose App IDs in the Identifiers section, and choose your app.
        """
        return pulumi.get(self, "bundle_id")

    @bundle_id.setter
    def bundle_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bundle_id", value)

    @property
    @pulumi.getter
    def certificate(self) -> Optional[pulumi.Input[str]]:
        """
        The pem encoded TLS Certificate from Apple.
        """
        return pulumi.get(self, "certificate")

    @certificate.setter
    def certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate", value)

    @property
    @pulumi.getter(name="defaultAuthenticationMethod")
    def default_authentication_method(self) -> Optional[pulumi.Input[str]]:
        """
        The default authentication method used for APNs.
        __NOTE__: Amazon Pinpoint uses this default for every APNs push notification that you send using the console.
        You can override the default when you send a message programmatically using the Amazon Pinpoint API, the AWS CLI, or an AWS SDK.
        If your default authentication type fails, Amazon Pinpoint doesn't attempt to use the other authentication type.

        One of the following sets of credentials is also required.

        If you choose to use __Certificate credentials__ you will have to provide:
        """
        return pulumi.get(self, "default_authentication_method")

    @default_authentication_method.setter
    def default_authentication_method(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_authentication_method", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the channel is enabled or disabled. Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="privateKey")
    def private_key(self) -> Optional[pulumi.Input[str]]:
        """
        The Certificate Private Key file (ie. `.key` file).

        If you choose to use __Key credentials__ you will have to provide:
        """
        return pulumi.get(self, "private_key")

    @private_key.setter
    def private_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_key", value)

    @property
    @pulumi.getter(name="teamId")
    def team_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID assigned to your Apple developer account team. This value is provided on the Membership page.
        """
        return pulumi.get(self, "team_id")

    @team_id.setter
    def team_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "team_id", value)

    @property
    @pulumi.getter(name="tokenKey")
    def token_key(self) -> Optional[pulumi.Input[str]]:
        """
        The `.p8` file that you download from your Apple developer account when you create an authentication key.
        """
        return pulumi.get(self, "token_key")

    @token_key.setter
    def token_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token_key", value)

    @property
    @pulumi.getter(name="tokenKeyId")
    def token_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID assigned to your signing key. To find this value, choose Certificates, IDs & Profiles, and choose your key in the Keys section.
        """
        return pulumi.get(self, "token_key_id")

    @token_key_id.setter
    def token_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "token_key_id", value)


class ApnsChannel(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_id: Optional[pulumi.Input[str]] = None,
                 bundle_id: Optional[pulumi.Input[str]] = None,
                 certificate: Optional[pulumi.Input[str]] = None,
                 default_authentication_method: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 private_key: Optional[pulumi.Input[str]] = None,
                 team_id: Optional[pulumi.Input[str]] = None,
                 token_key: Optional[pulumi.Input[str]] = None,
                 token_key_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Pinpoint APNs Channel resource.

        > **Note:** All arguments, including certificates and tokens, will be stored in the raw state as plain-text.
        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_std as std

        app = aws.pinpoint.App("app")
        apns = aws.pinpoint.ApnsChannel("apns",
            application_id=app.application_id,
            certificate=std.file(input="./certificate.pem").result,
            private_key=std.file(input="./private_key.key").result)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Pinpoint APNs Channel using the `application-id`. For example:

        ```sh
        $ pulumi import aws:pinpoint/apnsChannel:ApnsChannel apns application-id
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_id: The application ID.
        :param pulumi.Input[str] bundle_id: The ID assigned to your iOS app. To find this value, choose Certificates, IDs & Profiles, choose App IDs in the Identifiers section, and choose your app.
        :param pulumi.Input[str] certificate: The pem encoded TLS Certificate from Apple.
        :param pulumi.Input[str] default_authentication_method: The default authentication method used for APNs.
               __NOTE__: Amazon Pinpoint uses this default for every APNs push notification that you send using the console.
               You can override the default when you send a message programmatically using the Amazon Pinpoint API, the AWS CLI, or an AWS SDK.
               If your default authentication type fails, Amazon Pinpoint doesn't attempt to use the other authentication type.
               
               One of the following sets of credentials is also required.
               
               If you choose to use __Certificate credentials__ you will have to provide:
        :param pulumi.Input[bool] enabled: Whether the channel is enabled or disabled. Defaults to `true`.
        :param pulumi.Input[str] private_key: The Certificate Private Key file (ie. `.key` file).
               
               If you choose to use __Key credentials__ you will have to provide:
        :param pulumi.Input[str] team_id: The ID assigned to your Apple developer account team. This value is provided on the Membership page.
        :param pulumi.Input[str] token_key: The `.p8` file that you download from your Apple developer account when you create an authentication key.
        :param pulumi.Input[str] token_key_id: The ID assigned to your signing key. To find this value, choose Certificates, IDs & Profiles, and choose your key in the Keys section.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApnsChannelArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Pinpoint APNs Channel resource.

        > **Note:** All arguments, including certificates and tokens, will be stored in the raw state as plain-text.
        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_std as std

        app = aws.pinpoint.App("app")
        apns = aws.pinpoint.ApnsChannel("apns",
            application_id=app.application_id,
            certificate=std.file(input="./certificate.pem").result,
            private_key=std.file(input="./private_key.key").result)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Pinpoint APNs Channel using the `application-id`. For example:

        ```sh
        $ pulumi import aws:pinpoint/apnsChannel:ApnsChannel apns application-id
        ```

        :param str resource_name: The name of the resource.
        :param ApnsChannelArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApnsChannelArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_id: Optional[pulumi.Input[str]] = None,
                 bundle_id: Optional[pulumi.Input[str]] = None,
                 certificate: Optional[pulumi.Input[str]] = None,
                 default_authentication_method: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 private_key: Optional[pulumi.Input[str]] = None,
                 team_id: Optional[pulumi.Input[str]] = None,
                 token_key: Optional[pulumi.Input[str]] = None,
                 token_key_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApnsChannelArgs.__new__(ApnsChannelArgs)

            if application_id is None and not opts.urn:
                raise TypeError("Missing required property 'application_id'")
            __props__.__dict__["application_id"] = application_id
            __props__.__dict__["bundle_id"] = None if bundle_id is None else pulumi.Output.secret(bundle_id)
            __props__.__dict__["certificate"] = None if certificate is None else pulumi.Output.secret(certificate)
            __props__.__dict__["default_authentication_method"] = default_authentication_method
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["private_key"] = None if private_key is None else pulumi.Output.secret(private_key)
            __props__.__dict__["team_id"] = None if team_id is None else pulumi.Output.secret(team_id)
            __props__.__dict__["token_key"] = None if token_key is None else pulumi.Output.secret(token_key)
            __props__.__dict__["token_key_id"] = None if token_key_id is None else pulumi.Output.secret(token_key_id)
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["bundleId", "certificate", "privateKey", "teamId", "tokenKey", "tokenKeyId"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(ApnsChannel, __self__).__init__(
            'aws:pinpoint/apnsChannel:ApnsChannel',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            application_id: Optional[pulumi.Input[str]] = None,
            bundle_id: Optional[pulumi.Input[str]] = None,
            certificate: Optional[pulumi.Input[str]] = None,
            default_authentication_method: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            private_key: Optional[pulumi.Input[str]] = None,
            team_id: Optional[pulumi.Input[str]] = None,
            token_key: Optional[pulumi.Input[str]] = None,
            token_key_id: Optional[pulumi.Input[str]] = None) -> 'ApnsChannel':
        """
        Get an existing ApnsChannel resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_id: The application ID.
        :param pulumi.Input[str] bundle_id: The ID assigned to your iOS app. To find this value, choose Certificates, IDs & Profiles, choose App IDs in the Identifiers section, and choose your app.
        :param pulumi.Input[str] certificate: The pem encoded TLS Certificate from Apple.
        :param pulumi.Input[str] default_authentication_method: The default authentication method used for APNs.
               __NOTE__: Amazon Pinpoint uses this default for every APNs push notification that you send using the console.
               You can override the default when you send a message programmatically using the Amazon Pinpoint API, the AWS CLI, or an AWS SDK.
               If your default authentication type fails, Amazon Pinpoint doesn't attempt to use the other authentication type.
               
               One of the following sets of credentials is also required.
               
               If you choose to use __Certificate credentials__ you will have to provide:
        :param pulumi.Input[bool] enabled: Whether the channel is enabled or disabled. Defaults to `true`.
        :param pulumi.Input[str] private_key: The Certificate Private Key file (ie. `.key` file).
               
               If you choose to use __Key credentials__ you will have to provide:
        :param pulumi.Input[str] team_id: The ID assigned to your Apple developer account team. This value is provided on the Membership page.
        :param pulumi.Input[str] token_key: The `.p8` file that you download from your Apple developer account when you create an authentication key.
        :param pulumi.Input[str] token_key_id: The ID assigned to your signing key. To find this value, choose Certificates, IDs & Profiles, and choose your key in the Keys section.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ApnsChannelState.__new__(_ApnsChannelState)

        __props__.__dict__["application_id"] = application_id
        __props__.__dict__["bundle_id"] = bundle_id
        __props__.__dict__["certificate"] = certificate
        __props__.__dict__["default_authentication_method"] = default_authentication_method
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["private_key"] = private_key
        __props__.__dict__["team_id"] = team_id
        __props__.__dict__["token_key"] = token_key
        __props__.__dict__["token_key_id"] = token_key_id
        return ApnsChannel(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> pulumi.Output[str]:
        """
        The application ID.
        """
        return pulumi.get(self, "application_id")

    @property
    @pulumi.getter(name="bundleId")
    def bundle_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID assigned to your iOS app. To find this value, choose Certificates, IDs & Profiles, choose App IDs in the Identifiers section, and choose your app.
        """
        return pulumi.get(self, "bundle_id")

    @property
    @pulumi.getter
    def certificate(self) -> pulumi.Output[Optional[str]]:
        """
        The pem encoded TLS Certificate from Apple.
        """
        return pulumi.get(self, "certificate")

    @property
    @pulumi.getter(name="defaultAuthenticationMethod")
    def default_authentication_method(self) -> pulumi.Output[Optional[str]]:
        """
        The default authentication method used for APNs.
        __NOTE__: Amazon Pinpoint uses this default for every APNs push notification that you send using the console.
        You can override the default when you send a message programmatically using the Amazon Pinpoint API, the AWS CLI, or an AWS SDK.
        If your default authentication type fails, Amazon Pinpoint doesn't attempt to use the other authentication type.

        One of the following sets of credentials is also required.

        If you choose to use __Certificate credentials__ you will have to provide:
        """
        return pulumi.get(self, "default_authentication_method")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether the channel is enabled or disabled. Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="privateKey")
    def private_key(self) -> pulumi.Output[Optional[str]]:
        """
        The Certificate Private Key file (ie. `.key` file).

        If you choose to use __Key credentials__ you will have to provide:
        """
        return pulumi.get(self, "private_key")

    @property
    @pulumi.getter(name="teamId")
    def team_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID assigned to your Apple developer account team. This value is provided on the Membership page.
        """
        return pulumi.get(self, "team_id")

    @property
    @pulumi.getter(name="tokenKey")
    def token_key(self) -> pulumi.Output[Optional[str]]:
        """
        The `.p8` file that you download from your Apple developer account when you create an authentication key.
        """
        return pulumi.get(self, "token_key")

    @property
    @pulumi.getter(name="tokenKeyId")
    def token_key_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID assigned to your signing key. To find this value, choose Certificates, IDs & Profiles, and choose your key in the Keys section.
        """
        return pulumi.get(self, "token_key_id")

