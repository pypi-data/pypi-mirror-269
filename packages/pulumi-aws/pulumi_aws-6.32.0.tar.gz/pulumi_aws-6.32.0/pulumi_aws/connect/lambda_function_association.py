# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['LambdaFunctionAssociationArgs', 'LambdaFunctionAssociation']

@pulumi.input_type
class LambdaFunctionAssociationArgs:
    def __init__(__self__, *,
                 function_arn: pulumi.Input[str],
                 instance_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a LambdaFunctionAssociation resource.
        :param pulumi.Input[str] function_arn: Amazon Resource Name (ARN) of the Lambda Function, omitting any version or alias qualifier.
        :param pulumi.Input[str] instance_id: The identifier of the Amazon Connect instance. You can find the instanceId in the ARN of the instance.
        """
        pulumi.set(__self__, "function_arn", function_arn)
        pulumi.set(__self__, "instance_id", instance_id)

    @property
    @pulumi.getter(name="functionArn")
    def function_arn(self) -> pulumi.Input[str]:
        """
        Amazon Resource Name (ARN) of the Lambda Function, omitting any version or alias qualifier.
        """
        return pulumi.get(self, "function_arn")

    @function_arn.setter
    def function_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "function_arn", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        """
        The identifier of the Amazon Connect instance. You can find the instanceId in the ARN of the instance.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)


@pulumi.input_type
class _LambdaFunctionAssociationState:
    def __init__(__self__, *,
                 function_arn: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering LambdaFunctionAssociation resources.
        :param pulumi.Input[str] function_arn: Amazon Resource Name (ARN) of the Lambda Function, omitting any version or alias qualifier.
        :param pulumi.Input[str] instance_id: The identifier of the Amazon Connect instance. You can find the instanceId in the ARN of the instance.
        """
        if function_arn is not None:
            pulumi.set(__self__, "function_arn", function_arn)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)

    @property
    @pulumi.getter(name="functionArn")
    def function_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the Lambda Function, omitting any version or alias qualifier.
        """
        return pulumi.get(self, "function_arn")

    @function_arn.setter
    def function_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "function_arn", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The identifier of the Amazon Connect instance. You can find the instanceId in the ARN of the instance.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)


class LambdaFunctionAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 function_arn: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an Amazon Connect Lambda Function Association. For more information see
        [Amazon Connect: Getting Started](https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-get-started.html) and [Invoke AWS Lambda functions](https://docs.aws.amazon.com/connect/latest/adminguide/connect-lambda-functions.html).

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.connect.LambdaFunctionAssociation("example",
            function_arn=example_aws_lambda_function["arn"],
            instance_id=example_aws_connect_instance["id"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import `aws_connect_lambda_function_association` using the `instance_id` and `function_arn` separated by a comma (`,`). For example:

        ```sh
        $ pulumi import aws:connect/lambdaFunctionAssociation:LambdaFunctionAssociation example aaaaaaaa-bbbb-cccc-dddd-111111111111,arn:aws:lambda:us-west-2:123456789123:function:example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] function_arn: Amazon Resource Name (ARN) of the Lambda Function, omitting any version or alias qualifier.
        :param pulumi.Input[str] instance_id: The identifier of the Amazon Connect instance. You can find the instanceId in the ARN of the instance.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LambdaFunctionAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Amazon Connect Lambda Function Association. For more information see
        [Amazon Connect: Getting Started](https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-get-started.html) and [Invoke AWS Lambda functions](https://docs.aws.amazon.com/connect/latest/adminguide/connect-lambda-functions.html).

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.connect.LambdaFunctionAssociation("example",
            function_arn=example_aws_lambda_function["arn"],
            instance_id=example_aws_connect_instance["id"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import `aws_connect_lambda_function_association` using the `instance_id` and `function_arn` separated by a comma (`,`). For example:

        ```sh
        $ pulumi import aws:connect/lambdaFunctionAssociation:LambdaFunctionAssociation example aaaaaaaa-bbbb-cccc-dddd-111111111111,arn:aws:lambda:us-west-2:123456789123:function:example
        ```

        :param str resource_name: The name of the resource.
        :param LambdaFunctionAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LambdaFunctionAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 function_arn: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LambdaFunctionAssociationArgs.__new__(LambdaFunctionAssociationArgs)

            if function_arn is None and not opts.urn:
                raise TypeError("Missing required property 'function_arn'")
            __props__.__dict__["function_arn"] = function_arn
            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
        super(LambdaFunctionAssociation, __self__).__init__(
            'aws:connect/lambdaFunctionAssociation:LambdaFunctionAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            function_arn: Optional[pulumi.Input[str]] = None,
            instance_id: Optional[pulumi.Input[str]] = None) -> 'LambdaFunctionAssociation':
        """
        Get an existing LambdaFunctionAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] function_arn: Amazon Resource Name (ARN) of the Lambda Function, omitting any version or alias qualifier.
        :param pulumi.Input[str] instance_id: The identifier of the Amazon Connect instance. You can find the instanceId in the ARN of the instance.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LambdaFunctionAssociationState.__new__(_LambdaFunctionAssociationState)

        __props__.__dict__["function_arn"] = function_arn
        __props__.__dict__["instance_id"] = instance_id
        return LambdaFunctionAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="functionArn")
    def function_arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the Lambda Function, omitting any version or alias qualifier.
        """
        return pulumi.get(self, "function_arn")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        The identifier of the Amazon Connect instance. You can find the instanceId in the ARN of the instance.
        """
        return pulumi.get(self, "instance_id")

