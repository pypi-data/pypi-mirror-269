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

__all__ = ['BucketVersioningV2Args', 'BucketVersioningV2']

@pulumi.input_type
class BucketVersioningV2Args:
    def __init__(__self__, *,
                 bucket: pulumi.Input[str],
                 versioning_configuration: pulumi.Input['BucketVersioningV2VersioningConfigurationArgs'],
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None,
                 mfa: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a BucketVersioningV2 resource.
        :param pulumi.Input[str] bucket: Name of the S3 bucket.
        :param pulumi.Input['BucketVersioningV2VersioningConfigurationArgs'] versioning_configuration: Configuration block for the versioning parameters. See below.
        :param pulumi.Input[str] expected_bucket_owner: Account ID of the expected bucket owner.
        :param pulumi.Input[str] mfa: Concatenation of the authentication device's serial number, a space, and the value that is displayed on your authentication device.
        """
        pulumi.set(__self__, "bucket", bucket)
        pulumi.set(__self__, "versioning_configuration", versioning_configuration)
        if expected_bucket_owner is not None:
            pulumi.set(__self__, "expected_bucket_owner", expected_bucket_owner)
        if mfa is not None:
            pulumi.set(__self__, "mfa", mfa)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Input[str]:
        """
        Name of the S3 bucket.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter(name="versioningConfiguration")
    def versioning_configuration(self) -> pulumi.Input['BucketVersioningV2VersioningConfigurationArgs']:
        """
        Configuration block for the versioning parameters. See below.
        """
        return pulumi.get(self, "versioning_configuration")

    @versioning_configuration.setter
    def versioning_configuration(self, value: pulumi.Input['BucketVersioningV2VersioningConfigurationArgs']):
        pulumi.set(self, "versioning_configuration", value)

    @property
    @pulumi.getter(name="expectedBucketOwner")
    def expected_bucket_owner(self) -> Optional[pulumi.Input[str]]:
        """
        Account ID of the expected bucket owner.
        """
        return pulumi.get(self, "expected_bucket_owner")

    @expected_bucket_owner.setter
    def expected_bucket_owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expected_bucket_owner", value)

    @property
    @pulumi.getter
    def mfa(self) -> Optional[pulumi.Input[str]]:
        """
        Concatenation of the authentication device's serial number, a space, and the value that is displayed on your authentication device.
        """
        return pulumi.get(self, "mfa")

    @mfa.setter
    def mfa(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mfa", value)


@pulumi.input_type
class _BucketVersioningV2State:
    def __init__(__self__, *,
                 bucket: Optional[pulumi.Input[str]] = None,
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None,
                 mfa: Optional[pulumi.Input[str]] = None,
                 versioning_configuration: Optional[pulumi.Input['BucketVersioningV2VersioningConfigurationArgs']] = None):
        """
        Input properties used for looking up and filtering BucketVersioningV2 resources.
        :param pulumi.Input[str] bucket: Name of the S3 bucket.
        :param pulumi.Input[str] expected_bucket_owner: Account ID of the expected bucket owner.
        :param pulumi.Input[str] mfa: Concatenation of the authentication device's serial number, a space, and the value that is displayed on your authentication device.
        :param pulumi.Input['BucketVersioningV2VersioningConfigurationArgs'] versioning_configuration: Configuration block for the versioning parameters. See below.
        """
        if bucket is not None:
            pulumi.set(__self__, "bucket", bucket)
        if expected_bucket_owner is not None:
            pulumi.set(__self__, "expected_bucket_owner", expected_bucket_owner)
        if mfa is not None:
            pulumi.set(__self__, "mfa", mfa)
        if versioning_configuration is not None:
            pulumi.set(__self__, "versioning_configuration", versioning_configuration)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the S3 bucket.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter(name="expectedBucketOwner")
    def expected_bucket_owner(self) -> Optional[pulumi.Input[str]]:
        """
        Account ID of the expected bucket owner.
        """
        return pulumi.get(self, "expected_bucket_owner")

    @expected_bucket_owner.setter
    def expected_bucket_owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expected_bucket_owner", value)

    @property
    @pulumi.getter
    def mfa(self) -> Optional[pulumi.Input[str]]:
        """
        Concatenation of the authentication device's serial number, a space, and the value that is displayed on your authentication device.
        """
        return pulumi.get(self, "mfa")

    @mfa.setter
    def mfa(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mfa", value)

    @property
    @pulumi.getter(name="versioningConfiguration")
    def versioning_configuration(self) -> Optional[pulumi.Input['BucketVersioningV2VersioningConfigurationArgs']]:
        """
        Configuration block for the versioning parameters. See below.
        """
        return pulumi.get(self, "versioning_configuration")

    @versioning_configuration.setter
    def versioning_configuration(self, value: Optional[pulumi.Input['BucketVersioningV2VersioningConfigurationArgs']]):
        pulumi.set(self, "versioning_configuration", value)


class BucketVersioningV2(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None,
                 mfa: Optional[pulumi.Input[str]] = None,
                 versioning_configuration: Optional[pulumi.Input[pulumi.InputType['BucketVersioningV2VersioningConfigurationArgs']]] = None,
                 __props__=None):
        """
        Provides a resource for controlling versioning on an S3 bucket.
        Deleting this resource will either suspend versioning on the associated S3 bucket or
        simply remove the resource from state if the associated S3 bucket is unversioned.

        For more information, see [How S3 versioning works](https://docs.aws.amazon.com/AmazonS3/latest/userguide/manage-versioning-examples.html).

        > **NOTE:** If you are enabling versioning on the bucket for the first time, AWS recommends that you wait for 15 minutes after enabling versioning before issuing write operations (PUT or DELETE) on objects in the bucket.

        > This resource cannot be used with S3 directory buckets.

        ## Example Usage

        ### With Versioning Enabled

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example", bucket="example-bucket")
        example_bucket_acl_v2 = aws.s3.BucketAclV2("example",
            bucket=example.id,
            acl="private")
        versioning_example = aws.s3.BucketVersioningV2("versioning_example",
            bucket=example.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Enabled",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ### With Versioning Disabled

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example", bucket="example-bucket")
        example_bucket_acl_v2 = aws.s3.BucketAclV2("example",
            bucket=example.id,
            acl="private")
        versioning_example = aws.s3.BucketVersioningV2("versioning_example",
            bucket=example.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Disabled",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ### Object Dependency On Versioning

        When you create an object whose `version_id` you need and an `s3.BucketVersioningV2` resource in the same configuration, you are more likely to have success by ensuring the `s3_object` depends either implicitly (see below) or explicitly (i.e., using `depends_on = [aws_s3_bucket_versioning.example]`) on the `s3.BucketVersioningV2` resource.

        > **NOTE:** For critical and/or production S3 objects, do not create a bucket, enable versioning, and create an object in the bucket within the same configuration. Doing so will not allow the AWS-recommended 15 minutes between enabling versioning and writing to the bucket.

        This example shows the `aws_s3_object.example` depending implicitly on the versioning resource through the reference to `aws_s3_bucket_versioning.example.bucket` to define `bucket`:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example", bucket="yotto")
        example_bucket_versioning_v2 = aws.s3.BucketVersioningV2("example",
            bucket=example.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Enabled",
            ))
        example_bucket_objectv2 = aws.s3.BucketObjectv2("example",
            bucket=example_bucket_versioning_v2.id,
            key="droeloe",
            source=pulumi.FileAsset("example.txt"))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        If the owner (account ID) of the source bucket differs from the account used to configure the AWS Provider, import using the `bucket` and `expected_bucket_owner` separated by a comma (`,`):

        __Using `pulumi import` to import__ S3 bucket versioning using the `bucket` or using the `bucket` and `expected_bucket_owner` separated by a comma (`,`). For example:

        If the owner (account ID) of the source bucket is the same account used to configure the AWS Provider, import using the `bucket`:

        ```sh
        $ pulumi import aws:s3/bucketVersioningV2:BucketVersioningV2 example bucket-name
        ```
        If the owner (account ID) of the source bucket differs from the account used to configure the AWS Provider, import using the `bucket` and `expected_bucket_owner` separated by a comma (`,`):

        ```sh
        $ pulumi import aws:s3/bucketVersioningV2:BucketVersioningV2 example bucket-name,123456789012
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: Name of the S3 bucket.
        :param pulumi.Input[str] expected_bucket_owner: Account ID of the expected bucket owner.
        :param pulumi.Input[str] mfa: Concatenation of the authentication device's serial number, a space, and the value that is displayed on your authentication device.
        :param pulumi.Input[pulumi.InputType['BucketVersioningV2VersioningConfigurationArgs']] versioning_configuration: Configuration block for the versioning parameters. See below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BucketVersioningV2Args,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource for controlling versioning on an S3 bucket.
        Deleting this resource will either suspend versioning on the associated S3 bucket or
        simply remove the resource from state if the associated S3 bucket is unversioned.

        For more information, see [How S3 versioning works](https://docs.aws.amazon.com/AmazonS3/latest/userguide/manage-versioning-examples.html).

        > **NOTE:** If you are enabling versioning on the bucket for the first time, AWS recommends that you wait for 15 minutes after enabling versioning before issuing write operations (PUT or DELETE) on objects in the bucket.

        > This resource cannot be used with S3 directory buckets.

        ## Example Usage

        ### With Versioning Enabled

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example", bucket="example-bucket")
        example_bucket_acl_v2 = aws.s3.BucketAclV2("example",
            bucket=example.id,
            acl="private")
        versioning_example = aws.s3.BucketVersioningV2("versioning_example",
            bucket=example.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Enabled",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ### With Versioning Disabled

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example", bucket="example-bucket")
        example_bucket_acl_v2 = aws.s3.BucketAclV2("example",
            bucket=example.id,
            acl="private")
        versioning_example = aws.s3.BucketVersioningV2("versioning_example",
            bucket=example.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Disabled",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ### Object Dependency On Versioning

        When you create an object whose `version_id` you need and an `s3.BucketVersioningV2` resource in the same configuration, you are more likely to have success by ensuring the `s3_object` depends either implicitly (see below) or explicitly (i.e., using `depends_on = [aws_s3_bucket_versioning.example]`) on the `s3.BucketVersioningV2` resource.

        > **NOTE:** For critical and/or production S3 objects, do not create a bucket, enable versioning, and create an object in the bucket within the same configuration. Doing so will not allow the AWS-recommended 15 minutes between enabling versioning and writing to the bucket.

        This example shows the `aws_s3_object.example` depending implicitly on the versioning resource through the reference to `aws_s3_bucket_versioning.example.bucket` to define `bucket`:

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example", bucket="yotto")
        example_bucket_versioning_v2 = aws.s3.BucketVersioningV2("example",
            bucket=example.id,
            versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
                status="Enabled",
            ))
        example_bucket_objectv2 = aws.s3.BucketObjectv2("example",
            bucket=example_bucket_versioning_v2.id,
            key="droeloe",
            source=pulumi.FileAsset("example.txt"))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        If the owner (account ID) of the source bucket differs from the account used to configure the AWS Provider, import using the `bucket` and `expected_bucket_owner` separated by a comma (`,`):

        __Using `pulumi import` to import__ S3 bucket versioning using the `bucket` or using the `bucket` and `expected_bucket_owner` separated by a comma (`,`). For example:

        If the owner (account ID) of the source bucket is the same account used to configure the AWS Provider, import using the `bucket`:

        ```sh
        $ pulumi import aws:s3/bucketVersioningV2:BucketVersioningV2 example bucket-name
        ```
        If the owner (account ID) of the source bucket differs from the account used to configure the AWS Provider, import using the `bucket` and `expected_bucket_owner` separated by a comma (`,`):

        ```sh
        $ pulumi import aws:s3/bucketVersioningV2:BucketVersioningV2 example bucket-name,123456789012
        ```

        :param str resource_name: The name of the resource.
        :param BucketVersioningV2Args args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BucketVersioningV2Args, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 expected_bucket_owner: Optional[pulumi.Input[str]] = None,
                 mfa: Optional[pulumi.Input[str]] = None,
                 versioning_configuration: Optional[pulumi.Input[pulumi.InputType['BucketVersioningV2VersioningConfigurationArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BucketVersioningV2Args.__new__(BucketVersioningV2Args)

            if bucket is None and not opts.urn:
                raise TypeError("Missing required property 'bucket'")
            __props__.__dict__["bucket"] = bucket
            __props__.__dict__["expected_bucket_owner"] = expected_bucket_owner
            __props__.__dict__["mfa"] = mfa
            if versioning_configuration is None and not opts.urn:
                raise TypeError("Missing required property 'versioning_configuration'")
            __props__.__dict__["versioning_configuration"] = versioning_configuration
        super(BucketVersioningV2, __self__).__init__(
            'aws:s3/bucketVersioningV2:BucketVersioningV2',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bucket: Optional[pulumi.Input[str]] = None,
            expected_bucket_owner: Optional[pulumi.Input[str]] = None,
            mfa: Optional[pulumi.Input[str]] = None,
            versioning_configuration: Optional[pulumi.Input[pulumi.InputType['BucketVersioningV2VersioningConfigurationArgs']]] = None) -> 'BucketVersioningV2':
        """
        Get an existing BucketVersioningV2 resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: Name of the S3 bucket.
        :param pulumi.Input[str] expected_bucket_owner: Account ID of the expected bucket owner.
        :param pulumi.Input[str] mfa: Concatenation of the authentication device's serial number, a space, and the value that is displayed on your authentication device.
        :param pulumi.Input[pulumi.InputType['BucketVersioningV2VersioningConfigurationArgs']] versioning_configuration: Configuration block for the versioning parameters. See below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BucketVersioningV2State.__new__(_BucketVersioningV2State)

        __props__.__dict__["bucket"] = bucket
        __props__.__dict__["expected_bucket_owner"] = expected_bucket_owner
        __props__.__dict__["mfa"] = mfa
        __props__.__dict__["versioning_configuration"] = versioning_configuration
        return BucketVersioningV2(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Output[str]:
        """
        Name of the S3 bucket.
        """
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter(name="expectedBucketOwner")
    def expected_bucket_owner(self) -> pulumi.Output[Optional[str]]:
        """
        Account ID of the expected bucket owner.
        """
        return pulumi.get(self, "expected_bucket_owner")

    @property
    @pulumi.getter
    def mfa(self) -> pulumi.Output[Optional[str]]:
        """
        Concatenation of the authentication device's serial number, a space, and the value that is displayed on your authentication device.
        """
        return pulumi.get(self, "mfa")

    @property
    @pulumi.getter(name="versioningConfiguration")
    def versioning_configuration(self) -> pulumi.Output['outputs.BucketVersioningV2VersioningConfiguration']:
        """
        Configuration block for the versioning parameters. See below.
        """
        return pulumi.get(self, "versioning_configuration")

