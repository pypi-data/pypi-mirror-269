# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['BucketAccessKeyArgs', 'BucketAccessKey']

@pulumi.input_type
class BucketAccessKeyArgs:
    def __init__(__self__, *,
                 bucket_name: pulumi.Input[str]):
        """
        The set of arguments for constructing a BucketAccessKey resource.
        :param pulumi.Input[str] bucket_name: The name of the bucket that the new access key will belong to, and grant access to.
        """
        pulumi.set(__self__, "bucket_name", bucket_name)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> pulumi.Input[str]:
        """
        The name of the bucket that the new access key will belong to, and grant access to.
        """
        return pulumi.get(self, "bucket_name")

    @bucket_name.setter
    def bucket_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket_name", value)


@pulumi.input_type
class _BucketAccessKeyState:
    def __init__(__self__, *,
                 access_key_id: Optional[pulumi.Input[str]] = None,
                 bucket_name: Optional[pulumi.Input[str]] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 secret_access_key: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BucketAccessKey resources.
        :param pulumi.Input[str] access_key_id: The ID of the access key.
        :param pulumi.Input[str] bucket_name: The name of the bucket that the new access key will belong to, and grant access to.
        :param pulumi.Input[str] created_at: The timestamp when the access key was created.
        :param pulumi.Input[str] secret_access_key: The secret access key used to sign requests. This attribute is not available for imported resources. Note that this will be written to the state file.
        :param pulumi.Input[str] status: The status of the access key.
        """
        if access_key_id is not None:
            pulumi.set(__self__, "access_key_id", access_key_id)
        if bucket_name is not None:
            pulumi.set(__self__, "bucket_name", bucket_name)
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if secret_access_key is not None:
            pulumi.set(__self__, "secret_access_key", secret_access_key)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="accessKeyId")
    def access_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the access key.
        """
        return pulumi.get(self, "access_key_id")

    @access_key_id.setter
    def access_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_key_id", value)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the bucket that the new access key will belong to, and grant access to.
        """
        return pulumi.get(self, "bucket_name")

    @bucket_name.setter
    def bucket_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket_name", value)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        """
        The timestamp when the access key was created.
        """
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter(name="secretAccessKey")
    def secret_access_key(self) -> Optional[pulumi.Input[str]]:
        """
        The secret access key used to sign requests. This attribute is not available for imported resources. Note that this will be written to the state file.
        """
        return pulumi.get(self, "secret_access_key")

    @secret_access_key.setter
    def secret_access_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret_access_key", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the access key.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class BucketAccessKey(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a lightsail bucket access key. This is a set of credentials that allow API requests to be made to the lightsail bucket.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.lightsail.Bucket("test",
            name="mytestbucket",
            bundle_id="small_1_0")
        test_lightsail_bucket_access_key_access_key = aws.index.LightsailBucketAccessKeyAccessKey("test", bucket_name=test_aws_lightsail_bucket_access_key.id)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import `aws_lightsail_bucket_access_key` using the `id` attribute. For example:

        ```sh
        $ pulumi import aws:lightsail/bucketAccessKey:BucketAccessKey test example-bucket,AKIAIOSFODNN7EXAMPLE
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket_name: The name of the bucket that the new access key will belong to, and grant access to.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BucketAccessKeyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a lightsail bucket access key. This is a set of credentials that allow API requests to be made to the lightsail bucket.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.lightsail.Bucket("test",
            name="mytestbucket",
            bundle_id="small_1_0")
        test_lightsail_bucket_access_key_access_key = aws.index.LightsailBucketAccessKeyAccessKey("test", bucket_name=test_aws_lightsail_bucket_access_key.id)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import `aws_lightsail_bucket_access_key` using the `id` attribute. For example:

        ```sh
        $ pulumi import aws:lightsail/bucketAccessKey:BucketAccessKey test example-bucket,AKIAIOSFODNN7EXAMPLE
        ```

        :param str resource_name: The name of the resource.
        :param BucketAccessKeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BucketAccessKeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BucketAccessKeyArgs.__new__(BucketAccessKeyArgs)

            if bucket_name is None and not opts.urn:
                raise TypeError("Missing required property 'bucket_name'")
            __props__.__dict__["bucket_name"] = bucket_name
            __props__.__dict__["access_key_id"] = None
            __props__.__dict__["created_at"] = None
            __props__.__dict__["secret_access_key"] = None
            __props__.__dict__["status"] = None
        super(BucketAccessKey, __self__).__init__(
            'aws:lightsail/bucketAccessKey:BucketAccessKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_key_id: Optional[pulumi.Input[str]] = None,
            bucket_name: Optional[pulumi.Input[str]] = None,
            created_at: Optional[pulumi.Input[str]] = None,
            secret_access_key: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'BucketAccessKey':
        """
        Get an existing BucketAccessKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_key_id: The ID of the access key.
        :param pulumi.Input[str] bucket_name: The name of the bucket that the new access key will belong to, and grant access to.
        :param pulumi.Input[str] created_at: The timestamp when the access key was created.
        :param pulumi.Input[str] secret_access_key: The secret access key used to sign requests. This attribute is not available for imported resources. Note that this will be written to the state file.
        :param pulumi.Input[str] status: The status of the access key.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BucketAccessKeyState.__new__(_BucketAccessKeyState)

        __props__.__dict__["access_key_id"] = access_key_id
        __props__.__dict__["bucket_name"] = bucket_name
        __props__.__dict__["created_at"] = created_at
        __props__.__dict__["secret_access_key"] = secret_access_key
        __props__.__dict__["status"] = status
        return BucketAccessKey(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessKeyId")
    def access_key_id(self) -> pulumi.Output[str]:
        """
        The ID of the access key.
        """
        return pulumi.get(self, "access_key_id")

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> pulumi.Output[str]:
        """
        The name of the bucket that the new access key will belong to, and grant access to.
        """
        return pulumi.get(self, "bucket_name")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        The timestamp when the access key was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="secretAccessKey")
    def secret_access_key(self) -> pulumi.Output[str]:
        """
        The secret access key used to sign requests. This attribute is not available for imported resources. Note that this will be written to the state file.
        """
        return pulumi.get(self, "secret_access_key")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the access key.
        """
        return pulumi.get(self, "status")

