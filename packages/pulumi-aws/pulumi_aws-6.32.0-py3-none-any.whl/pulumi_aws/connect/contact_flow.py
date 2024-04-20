# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ContactFlowArgs', 'ContactFlow']

@pulumi.input_type
class ContactFlowArgs:
    def __init__(__self__, *,
                 instance_id: pulumi.Input[str],
                 content: Optional[pulumi.Input[str]] = None,
                 content_hash: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 filename: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ContactFlow resource.
        :param pulumi.Input[str] instance_id: Specifies the identifier of the hosting Amazon Connect Instance.
        :param pulumi.Input[str] content: Specifies the content of the Contact Flow, provided as a JSON string, written in Amazon Connect Contact Flow Language. If defined, the `filename` argument cannot be used.
        :param pulumi.Input[str] content_hash: Used to trigger updates. Must be set to a base64-encoded SHA256 hash of the Contact Flow source specified with `filename`.
        :param pulumi.Input[str] description: Specifies the description of the Contact Flow.
        :param pulumi.Input[str] filename: The path to the Contact Flow source within the local filesystem. Conflicts with `content`.
        :param pulumi.Input[str] name: Specifies the name of the Contact Flow.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags to apply to the Contact Flow. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] type: Specifies the type of the Contact Flow. Defaults to `CONTACT_FLOW`. Allowed Values are: `CONTACT_FLOW`, `CUSTOMER_QUEUE`, `CUSTOMER_HOLD`, `CUSTOMER_WHISPER`, `AGENT_HOLD`, `AGENT_WHISPER`, `OUTBOUND_WHISPER`, `AGENT_TRANSFER`, `QUEUE_TRANSFER`.
        """
        pulumi.set(__self__, "instance_id", instance_id)
        if content is not None:
            pulumi.set(__self__, "content", content)
        if content_hash is not None:
            pulumi.set(__self__, "content_hash", content_hash)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if filename is not None:
            pulumi.set(__self__, "filename", filename)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        """
        Specifies the identifier of the hosting Amazon Connect Instance.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter
    def content(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the content of the Contact Flow, provided as a JSON string, written in Amazon Connect Contact Flow Language. If defined, the `filename` argument cannot be used.
        """
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter(name="contentHash")
    def content_hash(self) -> Optional[pulumi.Input[str]]:
        """
        Used to trigger updates. Must be set to a base64-encoded SHA256 hash of the Contact Flow source specified with `filename`.
        """
        return pulumi.get(self, "content_hash")

    @content_hash.setter
    def content_hash(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_hash", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the description of the Contact Flow.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def filename(self) -> Optional[pulumi.Input[str]]:
        """
        The path to the Contact Flow source within the local filesystem. Conflicts with `content`.
        """
        return pulumi.get(self, "filename")

    @filename.setter
    def filename(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "filename", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Contact Flow.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Tags to apply to the Contact Flow. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the type of the Contact Flow. Defaults to `CONTACT_FLOW`. Allowed Values are: `CONTACT_FLOW`, `CUSTOMER_QUEUE`, `CUSTOMER_HOLD`, `CUSTOMER_WHISPER`, `AGENT_HOLD`, `AGENT_WHISPER`, `OUTBOUND_WHISPER`, `AGENT_TRANSFER`, `QUEUE_TRANSFER`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class _ContactFlowState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 contact_flow_id: Optional[pulumi.Input[str]] = None,
                 content: Optional[pulumi.Input[str]] = None,
                 content_hash: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 filename: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ContactFlow resources.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the Contact Flow.
        :param pulumi.Input[str] contact_flow_id: The identifier of the Contact Flow.
        :param pulumi.Input[str] content: Specifies the content of the Contact Flow, provided as a JSON string, written in Amazon Connect Contact Flow Language. If defined, the `filename` argument cannot be used.
        :param pulumi.Input[str] content_hash: Used to trigger updates. Must be set to a base64-encoded SHA256 hash of the Contact Flow source specified with `filename`.
        :param pulumi.Input[str] description: Specifies the description of the Contact Flow.
        :param pulumi.Input[str] filename: The path to the Contact Flow source within the local filesystem. Conflicts with `content`.
        :param pulumi.Input[str] instance_id: Specifies the identifier of the hosting Amazon Connect Instance.
        :param pulumi.Input[str] name: Specifies the name of the Contact Flow.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags to apply to the Contact Flow. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] type: Specifies the type of the Contact Flow. Defaults to `CONTACT_FLOW`. Allowed Values are: `CONTACT_FLOW`, `CUSTOMER_QUEUE`, `CUSTOMER_HOLD`, `CUSTOMER_WHISPER`, `AGENT_HOLD`, `AGENT_WHISPER`, `OUTBOUND_WHISPER`, `AGENT_TRANSFER`, `QUEUE_TRANSFER`.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if contact_flow_id is not None:
            pulumi.set(__self__, "contact_flow_id", contact_flow_id)
        if content is not None:
            pulumi.set(__self__, "content", content)
        if content_hash is not None:
            pulumi.set(__self__, "content_hash", content_hash)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if filename is not None:
            pulumi.set(__self__, "filename", filename)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the Contact Flow.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="contactFlowId")
    def contact_flow_id(self) -> Optional[pulumi.Input[str]]:
        """
        The identifier of the Contact Flow.
        """
        return pulumi.get(self, "contact_flow_id")

    @contact_flow_id.setter
    def contact_flow_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "contact_flow_id", value)

    @property
    @pulumi.getter
    def content(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the content of the Contact Flow, provided as a JSON string, written in Amazon Connect Contact Flow Language. If defined, the `filename` argument cannot be used.
        """
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter(name="contentHash")
    def content_hash(self) -> Optional[pulumi.Input[str]]:
        """
        Used to trigger updates. Must be set to a base64-encoded SHA256 hash of the Contact Flow source specified with `filename`.
        """
        return pulumi.get(self, "content_hash")

    @content_hash.setter
    def content_hash(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_hash", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the description of the Contact Flow.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def filename(self) -> Optional[pulumi.Input[str]]:
        """
        The path to the Contact Flow source within the local filesystem. Conflicts with `content`.
        """
        return pulumi.get(self, "filename")

    @filename.setter
    def filename(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "filename", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the identifier of the hosting Amazon Connect Instance.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Contact Flow.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Tags to apply to the Contact Flow. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the type of the Contact Flow. Defaults to `CONTACT_FLOW`. Allowed Values are: `CONTACT_FLOW`, `CUSTOMER_QUEUE`, `CUSTOMER_HOLD`, `CUSTOMER_WHISPER`, `AGENT_HOLD`, `AGENT_WHISPER`, `OUTBOUND_WHISPER`, `AGENT_TRANSFER`, `QUEUE_TRANSFER`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class ContactFlow(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 content: Optional[pulumi.Input[str]] = None,
                 content_hash: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 filename: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an Amazon Connect Contact Flow resource. For more information see
        [Amazon Connect: Getting Started](https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-get-started.html)

        This resource embeds or references Contact Flows specified in Amazon Connect Contact Flow Language. For more information see
        [Amazon Connect Flow language](https://docs.aws.amazon.com/connect/latest/adminguide/flow-language.html)

        !> **WARN:** Contact Flows exported from the Console [Contact Flow import/export](https://docs.aws.amazon.com/connect/latest/adminguide/contact-flow-import-export.html) are not in the Amazon Connect Contact Flow Language and can not be used with this resource. Instead, the recommendation is to use the AWS CLI [`describe-contact-flow`](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/connect/describe-contact-flow.html).
        See example below which uses `jq` to extract the `Content` attribute and saves it to a local file.

        ## Example Usage

        ### Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        test = aws.connect.ContactFlow("test",
            instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
            name="Test",
            description="Test Contact Flow Description",
            type="CONTACT_FLOW",
            content=json.dumps({
                "Version": "2019-10-30",
                "StartAction": "12345678-1234-1234-1234-123456789012",
                "Actions": [
                    {
                        "Identifier": "12345678-1234-1234-1234-123456789012",
                        "Type": "MessageParticipant",
                        "Transitions": {
                            "NextAction": "abcdef-abcd-abcd-abcd-abcdefghijkl",
                            "Errors": [],
                            "Conditions": [],
                        },
                        "Parameters": {
                            "Text": "Thanks for calling the sample flow!",
                        },
                    },
                    {
                        "Identifier": "abcdef-abcd-abcd-abcd-abcdefghijkl",
                        "Type": "DisconnectParticipant",
                        "Transitions": {},
                        "Parameters": {},
                    },
                ],
            }),
            tags={
                "Name": "Test Contact Flow",
                "Application": "Example",
                "Method": "Create",
            })
        ```
        <!--End PulumiCodeChooser -->

        ### With External Content

        Use the AWS CLI to extract Contact Flow Content:

        Use the generated file as input:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_std as std

        test = aws.connect.ContactFlow("test",
            instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
            name="Test",
            description="Test Contact Flow Description",
            type="CONTACT_FLOW",
            filename="contact_flow.json",
            content_hash=std.filebase64sha256(input="contact_flow.json").result,
            tags={
                "Name": "Test Contact Flow",
                "Application": "Example",
                "Method": "Create",
            })
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Amazon Connect Contact Flows using the `instance_id` and `contact_flow_id` separated by a colon (`:`). For example:

        ```sh
        $ pulumi import aws:connect/contactFlow:ContactFlow example f1288a1f-6193-445a-b47e-af739b2:c1d4e5f6-1b3c-1b3c-1b3c-c1d4e5f6c1d4e5
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] content: Specifies the content of the Contact Flow, provided as a JSON string, written in Amazon Connect Contact Flow Language. If defined, the `filename` argument cannot be used.
        :param pulumi.Input[str] content_hash: Used to trigger updates. Must be set to a base64-encoded SHA256 hash of the Contact Flow source specified with `filename`.
        :param pulumi.Input[str] description: Specifies the description of the Contact Flow.
        :param pulumi.Input[str] filename: The path to the Contact Flow source within the local filesystem. Conflicts with `content`.
        :param pulumi.Input[str] instance_id: Specifies the identifier of the hosting Amazon Connect Instance.
        :param pulumi.Input[str] name: Specifies the name of the Contact Flow.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags to apply to the Contact Flow. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] type: Specifies the type of the Contact Flow. Defaults to `CONTACT_FLOW`. Allowed Values are: `CONTACT_FLOW`, `CUSTOMER_QUEUE`, `CUSTOMER_HOLD`, `CUSTOMER_WHISPER`, `AGENT_HOLD`, `AGENT_WHISPER`, `OUTBOUND_WHISPER`, `AGENT_TRANSFER`, `QUEUE_TRANSFER`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ContactFlowArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Amazon Connect Contact Flow resource. For more information see
        [Amazon Connect: Getting Started](https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-get-started.html)

        This resource embeds or references Contact Flows specified in Amazon Connect Contact Flow Language. For more information see
        [Amazon Connect Flow language](https://docs.aws.amazon.com/connect/latest/adminguide/flow-language.html)

        !> **WARN:** Contact Flows exported from the Console [Contact Flow import/export](https://docs.aws.amazon.com/connect/latest/adminguide/contact-flow-import-export.html) are not in the Amazon Connect Contact Flow Language and can not be used with this resource. Instead, the recommendation is to use the AWS CLI [`describe-contact-flow`](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/connect/describe-contact-flow.html).
        See example below which uses `jq` to extract the `Content` attribute and saves it to a local file.

        ## Example Usage

        ### Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        test = aws.connect.ContactFlow("test",
            instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
            name="Test",
            description="Test Contact Flow Description",
            type="CONTACT_FLOW",
            content=json.dumps({
                "Version": "2019-10-30",
                "StartAction": "12345678-1234-1234-1234-123456789012",
                "Actions": [
                    {
                        "Identifier": "12345678-1234-1234-1234-123456789012",
                        "Type": "MessageParticipant",
                        "Transitions": {
                            "NextAction": "abcdef-abcd-abcd-abcd-abcdefghijkl",
                            "Errors": [],
                            "Conditions": [],
                        },
                        "Parameters": {
                            "Text": "Thanks for calling the sample flow!",
                        },
                    },
                    {
                        "Identifier": "abcdef-abcd-abcd-abcd-abcdefghijkl",
                        "Type": "DisconnectParticipant",
                        "Transitions": {},
                        "Parameters": {},
                    },
                ],
            }),
            tags={
                "Name": "Test Contact Flow",
                "Application": "Example",
                "Method": "Create",
            })
        ```
        <!--End PulumiCodeChooser -->

        ### With External Content

        Use the AWS CLI to extract Contact Flow Content:

        Use the generated file as input:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_std as std

        test = aws.connect.ContactFlow("test",
            instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
            name="Test",
            description="Test Contact Flow Description",
            type="CONTACT_FLOW",
            filename="contact_flow.json",
            content_hash=std.filebase64sha256(input="contact_flow.json").result,
            tags={
                "Name": "Test Contact Flow",
                "Application": "Example",
                "Method": "Create",
            })
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Amazon Connect Contact Flows using the `instance_id` and `contact_flow_id` separated by a colon (`:`). For example:

        ```sh
        $ pulumi import aws:connect/contactFlow:ContactFlow example f1288a1f-6193-445a-b47e-af739b2:c1d4e5f6-1b3c-1b3c-1b3c-c1d4e5f6c1d4e5
        ```

        :param str resource_name: The name of the resource.
        :param ContactFlowArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ContactFlowArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 content: Optional[pulumi.Input[str]] = None,
                 content_hash: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 filename: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ContactFlowArgs.__new__(ContactFlowArgs)

            __props__.__dict__["content"] = content
            __props__.__dict__["content_hash"] = content_hash
            __props__.__dict__["description"] = description
            __props__.__dict__["filename"] = filename
            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["type"] = type
            __props__.__dict__["arn"] = None
            __props__.__dict__["contact_flow_id"] = None
            __props__.__dict__["tags_all"] = None
        super(ContactFlow, __self__).__init__(
            'aws:connect/contactFlow:ContactFlow',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            contact_flow_id: Optional[pulumi.Input[str]] = None,
            content: Optional[pulumi.Input[str]] = None,
            content_hash: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            filename: Optional[pulumi.Input[str]] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'ContactFlow':
        """
        Get an existing ContactFlow resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the Contact Flow.
        :param pulumi.Input[str] contact_flow_id: The identifier of the Contact Flow.
        :param pulumi.Input[str] content: Specifies the content of the Contact Flow, provided as a JSON string, written in Amazon Connect Contact Flow Language. If defined, the `filename` argument cannot be used.
        :param pulumi.Input[str] content_hash: Used to trigger updates. Must be set to a base64-encoded SHA256 hash of the Contact Flow source specified with `filename`.
        :param pulumi.Input[str] description: Specifies the description of the Contact Flow.
        :param pulumi.Input[str] filename: The path to the Contact Flow source within the local filesystem. Conflicts with `content`.
        :param pulumi.Input[str] instance_id: Specifies the identifier of the hosting Amazon Connect Instance.
        :param pulumi.Input[str] name: Specifies the name of the Contact Flow.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags to apply to the Contact Flow. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] type: Specifies the type of the Contact Flow. Defaults to `CONTACT_FLOW`. Allowed Values are: `CONTACT_FLOW`, `CUSTOMER_QUEUE`, `CUSTOMER_HOLD`, `CUSTOMER_WHISPER`, `AGENT_HOLD`, `AGENT_WHISPER`, `OUTBOUND_WHISPER`, `AGENT_TRANSFER`, `QUEUE_TRANSFER`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ContactFlowState.__new__(_ContactFlowState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["contact_flow_id"] = contact_flow_id
        __props__.__dict__["content"] = content
        __props__.__dict__["content_hash"] = content_hash
        __props__.__dict__["description"] = description
        __props__.__dict__["filename"] = filename
        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["name"] = name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["type"] = type
        return ContactFlow(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the Contact Flow.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="contactFlowId")
    def contact_flow_id(self) -> pulumi.Output[str]:
        """
        The identifier of the Contact Flow.
        """
        return pulumi.get(self, "contact_flow_id")

    @property
    @pulumi.getter
    def content(self) -> pulumi.Output[str]:
        """
        Specifies the content of the Contact Flow, provided as a JSON string, written in Amazon Connect Contact Flow Language. If defined, the `filename` argument cannot be used.
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter(name="contentHash")
    def content_hash(self) -> pulumi.Output[Optional[str]]:
        """
        Used to trigger updates. Must be set to a base64-encoded SHA256 hash of the Contact Flow source specified with `filename`.
        """
        return pulumi.get(self, "content_hash")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the description of the Contact Flow.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def filename(self) -> pulumi.Output[Optional[str]]:
        """
        The path to the Contact Flow source within the local filesystem. Conflicts with `content`.
        """
        return pulumi.get(self, "filename")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        Specifies the identifier of the hosting Amazon Connect Instance.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Contact Flow.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Tags to apply to the Contact Flow. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the type of the Contact Flow. Defaults to `CONTACT_FLOW`. Allowed Values are: `CONTACT_FLOW`, `CUSTOMER_QUEUE`, `CUSTOMER_HOLD`, `CUSTOMER_WHISPER`, `AGENT_HOLD`, `AGENT_WHISPER`, `OUTBOUND_WHISPER`, `AGENT_TRANSFER`, `QUEUE_TRANSFER`.
        """
        return pulumi.get(self, "type")

