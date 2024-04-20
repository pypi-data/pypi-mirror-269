# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['QueuePolicyArgs', 'QueuePolicy']

@pulumi.input_type
class QueuePolicyArgs:
    def __init__(__self__, *,
                 policy: pulumi.Input[str],
                 queue_url: pulumi.Input[str]):
        """
        The set of arguments for constructing a QueuePolicy resource.
        :param pulumi.Input[str] policy: The JSON policy for the SQS queue.
        :param pulumi.Input[str] queue_url: The URL of the SQS Queue to which to attach the policy
        """
        pulumi.set(__self__, "policy", policy)
        pulumi.set(__self__, "queue_url", queue_url)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Input[str]:
        """
        The JSON policy for the SQS queue.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter(name="queueUrl")
    def queue_url(self) -> pulumi.Input[str]:
        """
        The URL of the SQS Queue to which to attach the policy
        """
        return pulumi.get(self, "queue_url")

    @queue_url.setter
    def queue_url(self, value: pulumi.Input[str]):
        pulumi.set(self, "queue_url", value)


@pulumi.input_type
class _QueuePolicyState:
    def __init__(__self__, *,
                 policy: Optional[pulumi.Input[str]] = None,
                 queue_url: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering QueuePolicy resources.
        :param pulumi.Input[str] policy: The JSON policy for the SQS queue.
        :param pulumi.Input[str] queue_url: The URL of the SQS Queue to which to attach the policy
        """
        if policy is not None:
            pulumi.set(__self__, "policy", policy)
        if queue_url is not None:
            pulumi.set(__self__, "queue_url", queue_url)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        The JSON policy for the SQS queue.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter(name="queueUrl")
    def queue_url(self) -> Optional[pulumi.Input[str]]:
        """
        The URL of the SQS Queue to which to attach the policy
        """
        return pulumi.get(self, "queue_url")

    @queue_url.setter
    def queue_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "queue_url", value)


class QueuePolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 queue_url: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Allows you to set a policy of an SQS Queue
        while referencing ARN of the queue within the policy.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        q = aws.sqs.Queue("q", name="examplequeue")
        test = q.arn.apply(lambda arn: aws.iam.get_policy_document_output(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            sid="First",
            effect="Allow",
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="*",
                identifiers=["*"],
            )],
            actions=["sqs:SendMessage"],
            resources=[arn],
            conditions=[aws.iam.GetPolicyDocumentStatementConditionArgs(
                test="ArnEquals",
                variable="aws:SourceArn",
                values=[example["arn"]],
            )],
        )]))
        test_queue_policy = aws.sqs.QueuePolicy("test",
            queue_url=q.id,
            policy=test.json)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import SQS Queue Policies using the queue URL. For example:

        ```sh
        $ pulumi import aws:sqs/queuePolicy:QueuePolicy test https://queue.amazonaws.com/0123456789012/myqueue
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy: The JSON policy for the SQS queue.
        :param pulumi.Input[str] queue_url: The URL of the SQS Queue to which to attach the policy
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: QueuePolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Allows you to set a policy of an SQS Queue
        while referencing ARN of the queue within the policy.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        q = aws.sqs.Queue("q", name="examplequeue")
        test = q.arn.apply(lambda arn: aws.iam.get_policy_document_output(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            sid="First",
            effect="Allow",
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="*",
                identifiers=["*"],
            )],
            actions=["sqs:SendMessage"],
            resources=[arn],
            conditions=[aws.iam.GetPolicyDocumentStatementConditionArgs(
                test="ArnEquals",
                variable="aws:SourceArn",
                values=[example["arn"]],
            )],
        )]))
        test_queue_policy = aws.sqs.QueuePolicy("test",
            queue_url=q.id,
            policy=test.json)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import SQS Queue Policies using the queue URL. For example:

        ```sh
        $ pulumi import aws:sqs/queuePolicy:QueuePolicy test https://queue.amazonaws.com/0123456789012/myqueue
        ```

        :param str resource_name: The name of the resource.
        :param QueuePolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(QueuePolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 queue_url: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = QueuePolicyArgs.__new__(QueuePolicyArgs)

            if policy is None and not opts.urn:
                raise TypeError("Missing required property 'policy'")
            __props__.__dict__["policy"] = policy
            if queue_url is None and not opts.urn:
                raise TypeError("Missing required property 'queue_url'")
            __props__.__dict__["queue_url"] = queue_url
        super(QueuePolicy, __self__).__init__(
            'aws:sqs/queuePolicy:QueuePolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            policy: Optional[pulumi.Input[str]] = None,
            queue_url: Optional[pulumi.Input[str]] = None) -> 'QueuePolicy':
        """
        Get an existing QueuePolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy: The JSON policy for the SQS queue.
        :param pulumi.Input[str] queue_url: The URL of the SQS Queue to which to attach the policy
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _QueuePolicyState.__new__(_QueuePolicyState)

        __props__.__dict__["policy"] = policy
        __props__.__dict__["queue_url"] = queue_url
        return QueuePolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[str]:
        """
        The JSON policy for the SQS queue.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter(name="queueUrl")
    def queue_url(self) -> pulumi.Output[str]:
        """
        The URL of the SQS Queue to which to attach the policy
        """
        return pulumi.get(self, "queue_url")

