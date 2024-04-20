# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AgreementArgs', 'Agreement']

@pulumi.input_type
class AgreementArgs:
    def __init__(__self__, *,
                 access_role: pulumi.Input[str],
                 base_directory: pulumi.Input[str],
                 local_profile_id: pulumi.Input[str],
                 partner_profile_id: pulumi.Input[str],
                 server_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Agreement resource.
        :param pulumi.Input[str] access_role: The IAM Role which provides read and write access to the parent directory of the file location mentioned in the StartFileTransfer request.
        :param pulumi.Input[str] base_directory: The landing directory for the files transferred by using the AS2 protocol.
        :param pulumi.Input[str] local_profile_id: The unique identifier for the AS2 local profile.
        :param pulumi.Input[str] partner_profile_id: The unique identifier for the AS2 partner profile.
        :param pulumi.Input[str] server_id: The unique server identifier for the server instance. This is the specific server the agreement uses.
        :param pulumi.Input[str] description: The Optional description of the transdfer.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "access_role", access_role)
        pulumi.set(__self__, "base_directory", base_directory)
        pulumi.set(__self__, "local_profile_id", local_profile_id)
        pulumi.set(__self__, "partner_profile_id", partner_profile_id)
        pulumi.set(__self__, "server_id", server_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="accessRole")
    def access_role(self) -> pulumi.Input[str]:
        """
        The IAM Role which provides read and write access to the parent directory of the file location mentioned in the StartFileTransfer request.
        """
        return pulumi.get(self, "access_role")

    @access_role.setter
    def access_role(self, value: pulumi.Input[str]):
        pulumi.set(self, "access_role", value)

    @property
    @pulumi.getter(name="baseDirectory")
    def base_directory(self) -> pulumi.Input[str]:
        """
        The landing directory for the files transferred by using the AS2 protocol.
        """
        return pulumi.get(self, "base_directory")

    @base_directory.setter
    def base_directory(self, value: pulumi.Input[str]):
        pulumi.set(self, "base_directory", value)

    @property
    @pulumi.getter(name="localProfileId")
    def local_profile_id(self) -> pulumi.Input[str]:
        """
        The unique identifier for the AS2 local profile.
        """
        return pulumi.get(self, "local_profile_id")

    @local_profile_id.setter
    def local_profile_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "local_profile_id", value)

    @property
    @pulumi.getter(name="partnerProfileId")
    def partner_profile_id(self) -> pulumi.Input[str]:
        """
        The unique identifier for the AS2 partner profile.
        """
        return pulumi.get(self, "partner_profile_id")

    @partner_profile_id.setter
    def partner_profile_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "partner_profile_id", value)

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> pulumi.Input[str]:
        """
        The unique server identifier for the server instance. This is the specific server the agreement uses.
        """
        return pulumi.get(self, "server_id")

    @server_id.setter
    def server_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The Optional description of the transdfer.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _AgreementState:
    def __init__(__self__, *,
                 access_role: Optional[pulumi.Input[str]] = None,
                 agreement_id: Optional[pulumi.Input[str]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 base_directory: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 local_profile_id: Optional[pulumi.Input[str]] = None,
                 partner_profile_id: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Agreement resources.
        :param pulumi.Input[str] access_role: The IAM Role which provides read and write access to the parent directory of the file location mentioned in the StartFileTransfer request.
        :param pulumi.Input[str] agreement_id: The unique identifier for the AS2 agreement.
        :param pulumi.Input[str] arn: The ARN of the agreement.
        :param pulumi.Input[str] base_directory: The landing directory for the files transferred by using the AS2 protocol.
        :param pulumi.Input[str] description: The Optional description of the transdfer.
        :param pulumi.Input[str] local_profile_id: The unique identifier for the AS2 local profile.
        :param pulumi.Input[str] partner_profile_id: The unique identifier for the AS2 partner profile.
        :param pulumi.Input[str] server_id: The unique server identifier for the server instance. This is the specific server the agreement uses.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        if access_role is not None:
            pulumi.set(__self__, "access_role", access_role)
        if agreement_id is not None:
            pulumi.set(__self__, "agreement_id", agreement_id)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if base_directory is not None:
            pulumi.set(__self__, "base_directory", base_directory)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if local_profile_id is not None:
            pulumi.set(__self__, "local_profile_id", local_profile_id)
        if partner_profile_id is not None:
            pulumi.set(__self__, "partner_profile_id", partner_profile_id)
        if server_id is not None:
            pulumi.set(__self__, "server_id", server_id)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter(name="accessRole")
    def access_role(self) -> Optional[pulumi.Input[str]]:
        """
        The IAM Role which provides read and write access to the parent directory of the file location mentioned in the StartFileTransfer request.
        """
        return pulumi.get(self, "access_role")

    @access_role.setter
    def access_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_role", value)

    @property
    @pulumi.getter(name="agreementId")
    def agreement_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique identifier for the AS2 agreement.
        """
        return pulumi.get(self, "agreement_id")

    @agreement_id.setter
    def agreement_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "agreement_id", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the agreement.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="baseDirectory")
    def base_directory(self) -> Optional[pulumi.Input[str]]:
        """
        The landing directory for the files transferred by using the AS2 protocol.
        """
        return pulumi.get(self, "base_directory")

    @base_directory.setter
    def base_directory(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "base_directory", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The Optional description of the transdfer.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="localProfileId")
    def local_profile_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique identifier for the AS2 local profile.
        """
        return pulumi.get(self, "local_profile_id")

    @local_profile_id.setter
    def local_profile_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "local_profile_id", value)

    @property
    @pulumi.getter(name="partnerProfileId")
    def partner_profile_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique identifier for the AS2 partner profile.
        """
        return pulumi.get(self, "partner_profile_id")

    @partner_profile_id.setter
    def partner_profile_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "partner_profile_id", value)

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique server identifier for the server instance. This is the specific server the agreement uses.
        """
        return pulumi.get(self, "server_id")

    @server_id.setter
    def server_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_id", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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


class Agreement(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_role: Optional[pulumi.Input[str]] = None,
                 base_directory: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 local_profile_id: Optional[pulumi.Input[str]] = None,
                 partner_profile_id: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a AWS Transfer AS2 Agreement resource.

        ## Example Usage

        ### Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.transfer.Agreement("example",
            access_role=test["arn"],
            base_directory="/DOC-EXAMPLE-BUCKET/home/mydirectory",
            description="example",
            local_profile_id=local["profileId"],
            partner_profile_id=partner["profileId"],
            server_id=test_aws_transfer_server["id"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Transfer AS2 Agreement using the `server_id/agreement_id`. For example:

        ```sh
        $ pulumi import aws:transfer/agreement:Agreement example s-4221a88afd5f4362a/a-4221a88afd5f4362a
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_role: The IAM Role which provides read and write access to the parent directory of the file location mentioned in the StartFileTransfer request.
        :param pulumi.Input[str] base_directory: The landing directory for the files transferred by using the AS2 protocol.
        :param pulumi.Input[str] description: The Optional description of the transdfer.
        :param pulumi.Input[str] local_profile_id: The unique identifier for the AS2 local profile.
        :param pulumi.Input[str] partner_profile_id: The unique identifier for the AS2 partner profile.
        :param pulumi.Input[str] server_id: The unique server identifier for the server instance. This is the specific server the agreement uses.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AgreementArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a AWS Transfer AS2 Agreement resource.

        ## Example Usage

        ### Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.transfer.Agreement("example",
            access_role=test["arn"],
            base_directory="/DOC-EXAMPLE-BUCKET/home/mydirectory",
            description="example",
            local_profile_id=local["profileId"],
            partner_profile_id=partner["profileId"],
            server_id=test_aws_transfer_server["id"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Transfer AS2 Agreement using the `server_id/agreement_id`. For example:

        ```sh
        $ pulumi import aws:transfer/agreement:Agreement example s-4221a88afd5f4362a/a-4221a88afd5f4362a
        ```

        :param str resource_name: The name of the resource.
        :param AgreementArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AgreementArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_role: Optional[pulumi.Input[str]] = None,
                 base_directory: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 local_profile_id: Optional[pulumi.Input[str]] = None,
                 partner_profile_id: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AgreementArgs.__new__(AgreementArgs)

            if access_role is None and not opts.urn:
                raise TypeError("Missing required property 'access_role'")
            __props__.__dict__["access_role"] = access_role
            if base_directory is None and not opts.urn:
                raise TypeError("Missing required property 'base_directory'")
            __props__.__dict__["base_directory"] = base_directory
            __props__.__dict__["description"] = description
            if local_profile_id is None and not opts.urn:
                raise TypeError("Missing required property 'local_profile_id'")
            __props__.__dict__["local_profile_id"] = local_profile_id
            if partner_profile_id is None and not opts.urn:
                raise TypeError("Missing required property 'partner_profile_id'")
            __props__.__dict__["partner_profile_id"] = partner_profile_id
            if server_id is None and not opts.urn:
                raise TypeError("Missing required property 'server_id'")
            __props__.__dict__["server_id"] = server_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["agreement_id"] = None
            __props__.__dict__["arn"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["tags_all"] = None
        super(Agreement, __self__).__init__(
            'aws:transfer/agreement:Agreement',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_role: Optional[pulumi.Input[str]] = None,
            agreement_id: Optional[pulumi.Input[str]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            base_directory: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            local_profile_id: Optional[pulumi.Input[str]] = None,
            partner_profile_id: Optional[pulumi.Input[str]] = None,
            server_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Agreement':
        """
        Get an existing Agreement resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_role: The IAM Role which provides read and write access to the parent directory of the file location mentioned in the StartFileTransfer request.
        :param pulumi.Input[str] agreement_id: The unique identifier for the AS2 agreement.
        :param pulumi.Input[str] arn: The ARN of the agreement.
        :param pulumi.Input[str] base_directory: The landing directory for the files transferred by using the AS2 protocol.
        :param pulumi.Input[str] description: The Optional description of the transdfer.
        :param pulumi.Input[str] local_profile_id: The unique identifier for the AS2 local profile.
        :param pulumi.Input[str] partner_profile_id: The unique identifier for the AS2 partner profile.
        :param pulumi.Input[str] server_id: The unique server identifier for the server instance. This is the specific server the agreement uses.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AgreementState.__new__(_AgreementState)

        __props__.__dict__["access_role"] = access_role
        __props__.__dict__["agreement_id"] = agreement_id
        __props__.__dict__["arn"] = arn
        __props__.__dict__["base_directory"] = base_directory
        __props__.__dict__["description"] = description
        __props__.__dict__["local_profile_id"] = local_profile_id
        __props__.__dict__["partner_profile_id"] = partner_profile_id
        __props__.__dict__["server_id"] = server_id
        __props__.__dict__["status"] = status
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return Agreement(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessRole")
    def access_role(self) -> pulumi.Output[str]:
        """
        The IAM Role which provides read and write access to the parent directory of the file location mentioned in the StartFileTransfer request.
        """
        return pulumi.get(self, "access_role")

    @property
    @pulumi.getter(name="agreementId")
    def agreement_id(self) -> pulumi.Output[str]:
        """
        The unique identifier for the AS2 agreement.
        """
        return pulumi.get(self, "agreement_id")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the agreement.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="baseDirectory")
    def base_directory(self) -> pulumi.Output[str]:
        """
        The landing directory for the files transferred by using the AS2 protocol.
        """
        return pulumi.get(self, "base_directory")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The Optional description of the transdfer.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="localProfileId")
    def local_profile_id(self) -> pulumi.Output[str]:
        """
        The unique identifier for the AS2 local profile.
        """
        return pulumi.get(self, "local_profile_id")

    @property
    @pulumi.getter(name="partnerProfileId")
    def partner_profile_id(self) -> pulumi.Output[str]:
        """
        The unique identifier for the AS2 partner profile.
        """
        return pulumi.get(self, "partner_profile_id")

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> pulumi.Output[str]:
        """
        The unique server identifier for the server instance. This is the specific server the agreement uses.
        """
        return pulumi.get(self, "server_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

