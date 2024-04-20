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

__all__ = ['MultiRegionAccessPointArgs', 'MultiRegionAccessPoint']

@pulumi.input_type
class MultiRegionAccessPointArgs:
    def __init__(__self__, *,
                 details: pulumi.Input['MultiRegionAccessPointDetailsArgs'],
                 account_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a MultiRegionAccessPoint resource.
        :param pulumi.Input['MultiRegionAccessPointDetailsArgs'] details: A configuration block containing details about the Multi-Region Access Point. See Details Configuration Block below for more details
        :param pulumi.Input[str] account_id: The AWS account ID for the owner of the buckets for which you want to create a Multi-Region Access Point. Defaults to automatically determined account ID of the AWS provider.
        """
        pulumi.set(__self__, "details", details)
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)

    @property
    @pulumi.getter
    def details(self) -> pulumi.Input['MultiRegionAccessPointDetailsArgs']:
        """
        A configuration block containing details about the Multi-Region Access Point. See Details Configuration Block below for more details
        """
        return pulumi.get(self, "details")

    @details.setter
    def details(self, value: pulumi.Input['MultiRegionAccessPointDetailsArgs']):
        pulumi.set(self, "details", value)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The AWS account ID for the owner of the buckets for which you want to create a Multi-Region Access Point. Defaults to automatically determined account ID of the AWS provider.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_id", value)


@pulumi.input_type
class _MultiRegionAccessPointState:
    def __init__(__self__, *,
                 account_id: Optional[pulumi.Input[str]] = None,
                 alias: Optional[pulumi.Input[str]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 details: Optional[pulumi.Input['MultiRegionAccessPointDetailsArgs']] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering MultiRegionAccessPoint resources.
        :param pulumi.Input[str] account_id: The AWS account ID for the owner of the buckets for which you want to create a Multi-Region Access Point. Defaults to automatically determined account ID of the AWS provider.
        :param pulumi.Input[str] alias: The alias for the Multi-Region Access Point.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the Multi-Region Access Point.
        :param pulumi.Input['MultiRegionAccessPointDetailsArgs'] details: A configuration block containing details about the Multi-Region Access Point. See Details Configuration Block below for more details
        :param pulumi.Input[str] domain_name: The DNS domain name of the S3 Multi-Region Access Point in the format _`alias`_.accesspoint.s3-global.amazonaws.com. For more information, see the documentation on [Multi-Region Access Point Requests](https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiRegionAccessPointRequests.html).
        :param pulumi.Input[str] status: The current status of the Multi-Region Access Point. One of: `READY`, `INCONSISTENT_ACROSS_REGIONS`, `CREATING`, `PARTIALLY_CREATED`, `PARTIALLY_DELETED`, `DELETING`.
        """
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if alias is not None:
            pulumi.set(__self__, "alias", alias)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if details is not None:
            pulumi.set(__self__, "details", details)
        if domain_name is not None:
            pulumi.set(__self__, "domain_name", domain_name)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The AWS account ID for the owner of the buckets for which you want to create a Multi-Region Access Point. Defaults to automatically determined account ID of the AWS provider.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter
    def alias(self) -> Optional[pulumi.Input[str]]:
        """
        The alias for the Multi-Region Access Point.
        """
        return pulumi.get(self, "alias")

    @alias.setter
    def alias(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "alias", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the Multi-Region Access Point.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def details(self) -> Optional[pulumi.Input['MultiRegionAccessPointDetailsArgs']]:
        """
        A configuration block containing details about the Multi-Region Access Point. See Details Configuration Block below for more details
        """
        return pulumi.get(self, "details")

    @details.setter
    def details(self, value: Optional[pulumi.Input['MultiRegionAccessPointDetailsArgs']]):
        pulumi.set(self, "details", value)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        The DNS domain name of the S3 Multi-Region Access Point in the format _`alias`_.accesspoint.s3-global.amazonaws.com. For more information, see the documentation on [Multi-Region Access Point Requests](https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiRegionAccessPointRequests.html).
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The current status of the Multi-Region Access Point. One of: `READY`, `INCONSISTENT_ACROSS_REGIONS`, `CREATING`, `PARTIALLY_CREATED`, `PARTIALLY_DELETED`, `DELETING`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class MultiRegionAccessPoint(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 details: Optional[pulumi.Input[pulumi.InputType['MultiRegionAccessPointDetailsArgs']]] = None,
                 __props__=None):
        """
        Provides a resource to manage an S3 Multi-Region Access Point associated with specified buckets.

        > This resource cannot be used with S3 directory buckets.

        ## Example Usage

        ### Multiple AWS Buckets in Different Regions

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        foo_bucket = aws.s3.BucketV2("foo_bucket", bucket="example-bucket-foo")
        bar_bucket = aws.s3.BucketV2("bar_bucket", bucket="example-bucket-bar")
        example = aws.s3control.MultiRegionAccessPoint("example", details=aws.s3control.MultiRegionAccessPointDetailsArgs(
            name="example",
            regions=[
                aws.s3control.MultiRegionAccessPointDetailsRegionArgs(
                    bucket=foo_bucket.id,
                ),
                aws.s3control.MultiRegionAccessPointDetailsRegionArgs(
                    bucket=bar_bucket.id,
                ),
            ],
        ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Multi-Region Access Points using the `account_id` and `name` of the Multi-Region Access Point separated by a colon (`:`). For example:

        ```sh
        $ pulumi import aws:s3control/multiRegionAccessPoint:MultiRegionAccessPoint example 123456789012:example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: The AWS account ID for the owner of the buckets for which you want to create a Multi-Region Access Point. Defaults to automatically determined account ID of the AWS provider.
        :param pulumi.Input[pulumi.InputType['MultiRegionAccessPointDetailsArgs']] details: A configuration block containing details about the Multi-Region Access Point. See Details Configuration Block below for more details
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MultiRegionAccessPointArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage an S3 Multi-Region Access Point associated with specified buckets.

        > This resource cannot be used with S3 directory buckets.

        ## Example Usage

        ### Multiple AWS Buckets in Different Regions

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        foo_bucket = aws.s3.BucketV2("foo_bucket", bucket="example-bucket-foo")
        bar_bucket = aws.s3.BucketV2("bar_bucket", bucket="example-bucket-bar")
        example = aws.s3control.MultiRegionAccessPoint("example", details=aws.s3control.MultiRegionAccessPointDetailsArgs(
            name="example",
            regions=[
                aws.s3control.MultiRegionAccessPointDetailsRegionArgs(
                    bucket=foo_bucket.id,
                ),
                aws.s3control.MultiRegionAccessPointDetailsRegionArgs(
                    bucket=bar_bucket.id,
                ),
            ],
        ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Multi-Region Access Points using the `account_id` and `name` of the Multi-Region Access Point separated by a colon (`:`). For example:

        ```sh
        $ pulumi import aws:s3control/multiRegionAccessPoint:MultiRegionAccessPoint example 123456789012:example
        ```

        :param str resource_name: The name of the resource.
        :param MultiRegionAccessPointArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MultiRegionAccessPointArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 details: Optional[pulumi.Input[pulumi.InputType['MultiRegionAccessPointDetailsArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MultiRegionAccessPointArgs.__new__(MultiRegionAccessPointArgs)

            __props__.__dict__["account_id"] = account_id
            if details is None and not opts.urn:
                raise TypeError("Missing required property 'details'")
            __props__.__dict__["details"] = details
            __props__.__dict__["alias"] = None
            __props__.__dict__["arn"] = None
            __props__.__dict__["domain_name"] = None
            __props__.__dict__["status"] = None
        super(MultiRegionAccessPoint, __self__).__init__(
            'aws:s3control/multiRegionAccessPoint:MultiRegionAccessPoint',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_id: Optional[pulumi.Input[str]] = None,
            alias: Optional[pulumi.Input[str]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            details: Optional[pulumi.Input[pulumi.InputType['MultiRegionAccessPointDetailsArgs']]] = None,
            domain_name: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'MultiRegionAccessPoint':
        """
        Get an existing MultiRegionAccessPoint resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: The AWS account ID for the owner of the buckets for which you want to create a Multi-Region Access Point. Defaults to automatically determined account ID of the AWS provider.
        :param pulumi.Input[str] alias: The alias for the Multi-Region Access Point.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the Multi-Region Access Point.
        :param pulumi.Input[pulumi.InputType['MultiRegionAccessPointDetailsArgs']] details: A configuration block containing details about the Multi-Region Access Point. See Details Configuration Block below for more details
        :param pulumi.Input[str] domain_name: The DNS domain name of the S3 Multi-Region Access Point in the format _`alias`_.accesspoint.s3-global.amazonaws.com. For more information, see the documentation on [Multi-Region Access Point Requests](https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiRegionAccessPointRequests.html).
        :param pulumi.Input[str] status: The current status of the Multi-Region Access Point. One of: `READY`, `INCONSISTENT_ACROSS_REGIONS`, `CREATING`, `PARTIALLY_CREATED`, `PARTIALLY_DELETED`, `DELETING`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _MultiRegionAccessPointState.__new__(_MultiRegionAccessPointState)

        __props__.__dict__["account_id"] = account_id
        __props__.__dict__["alias"] = alias
        __props__.__dict__["arn"] = arn
        __props__.__dict__["details"] = details
        __props__.__dict__["domain_name"] = domain_name
        __props__.__dict__["status"] = status
        return MultiRegionAccessPoint(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Output[str]:
        """
        The AWS account ID for the owner of the buckets for which you want to create a Multi-Region Access Point. Defaults to automatically determined account ID of the AWS provider.
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def alias(self) -> pulumi.Output[str]:
        """
        The alias for the Multi-Region Access Point.
        """
        return pulumi.get(self, "alias")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the Multi-Region Access Point.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def details(self) -> pulumi.Output['outputs.MultiRegionAccessPointDetails']:
        """
        A configuration block containing details about the Multi-Region Access Point. See Details Configuration Block below for more details
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Output[str]:
        """
        The DNS domain name of the S3 Multi-Region Access Point in the format _`alias`_.accesspoint.s3-global.amazonaws.com. For more information, see the documentation on [Multi-Region Access Point Requests](https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiRegionAccessPointRequests.html).
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The current status of the Multi-Region Access Point. One of: `READY`, `INCONSISTENT_ACROSS_REGIONS`, `CREATING`, `PARTIALLY_CREATED`, `PARTIALLY_DELETED`, `DELETING`.
        """
        return pulumi.get(self, "status")

