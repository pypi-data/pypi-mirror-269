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

__all__ = ['PackageArgs', 'Package']

@pulumi.input_type
class PackageArgs:
    def __init__(__self__, *,
                 package_name: pulumi.Input[str],
                 package_source: pulumi.Input['PackagePackageSourceArgs'],
                 package_type: pulumi.Input[str],
                 package_description: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Package resource.
        :param pulumi.Input[str] package_name: Unique name for the package.
        :param pulumi.Input['PackagePackageSourceArgs'] package_source: Configuration block for the package source options.
        :param pulumi.Input[str] package_type: The type of package.
        :param pulumi.Input[str] package_description: Description of the package.
        """
        pulumi.set(__self__, "package_name", package_name)
        pulumi.set(__self__, "package_source", package_source)
        pulumi.set(__self__, "package_type", package_type)
        if package_description is not None:
            pulumi.set(__self__, "package_description", package_description)

    @property
    @pulumi.getter(name="packageName")
    def package_name(self) -> pulumi.Input[str]:
        """
        Unique name for the package.
        """
        return pulumi.get(self, "package_name")

    @package_name.setter
    def package_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "package_name", value)

    @property
    @pulumi.getter(name="packageSource")
    def package_source(self) -> pulumi.Input['PackagePackageSourceArgs']:
        """
        Configuration block for the package source options.
        """
        return pulumi.get(self, "package_source")

    @package_source.setter
    def package_source(self, value: pulumi.Input['PackagePackageSourceArgs']):
        pulumi.set(self, "package_source", value)

    @property
    @pulumi.getter(name="packageType")
    def package_type(self) -> pulumi.Input[str]:
        """
        The type of package.
        """
        return pulumi.get(self, "package_type")

    @package_type.setter
    def package_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "package_type", value)

    @property
    @pulumi.getter(name="packageDescription")
    def package_description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the package.
        """
        return pulumi.get(self, "package_description")

    @package_description.setter
    def package_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "package_description", value)


@pulumi.input_type
class _PackageState:
    def __init__(__self__, *,
                 available_package_version: Optional[pulumi.Input[str]] = None,
                 package_description: Optional[pulumi.Input[str]] = None,
                 package_id: Optional[pulumi.Input[str]] = None,
                 package_name: Optional[pulumi.Input[str]] = None,
                 package_source: Optional[pulumi.Input['PackagePackageSourceArgs']] = None,
                 package_type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Package resources.
        :param pulumi.Input[str] available_package_version: The current version of the package.
        :param pulumi.Input[str] package_description: Description of the package.
        :param pulumi.Input[str] package_name: Unique name for the package.
        :param pulumi.Input['PackagePackageSourceArgs'] package_source: Configuration block for the package source options.
        :param pulumi.Input[str] package_type: The type of package.
        """
        if available_package_version is not None:
            pulumi.set(__self__, "available_package_version", available_package_version)
        if package_description is not None:
            pulumi.set(__self__, "package_description", package_description)
        if package_id is not None:
            pulumi.set(__self__, "package_id", package_id)
        if package_name is not None:
            pulumi.set(__self__, "package_name", package_name)
        if package_source is not None:
            pulumi.set(__self__, "package_source", package_source)
        if package_type is not None:
            pulumi.set(__self__, "package_type", package_type)

    @property
    @pulumi.getter(name="availablePackageVersion")
    def available_package_version(self) -> Optional[pulumi.Input[str]]:
        """
        The current version of the package.
        """
        return pulumi.get(self, "available_package_version")

    @available_package_version.setter
    def available_package_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "available_package_version", value)

    @property
    @pulumi.getter(name="packageDescription")
    def package_description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the package.
        """
        return pulumi.get(self, "package_description")

    @package_description.setter
    def package_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "package_description", value)

    @property
    @pulumi.getter(name="packageId")
    def package_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "package_id")

    @package_id.setter
    def package_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "package_id", value)

    @property
    @pulumi.getter(name="packageName")
    def package_name(self) -> Optional[pulumi.Input[str]]:
        """
        Unique name for the package.
        """
        return pulumi.get(self, "package_name")

    @package_name.setter
    def package_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "package_name", value)

    @property
    @pulumi.getter(name="packageSource")
    def package_source(self) -> Optional[pulumi.Input['PackagePackageSourceArgs']]:
        """
        Configuration block for the package source options.
        """
        return pulumi.get(self, "package_source")

    @package_source.setter
    def package_source(self, value: Optional[pulumi.Input['PackagePackageSourceArgs']]):
        pulumi.set(self, "package_source", value)

    @property
    @pulumi.getter(name="packageType")
    def package_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of package.
        """
        return pulumi.get(self, "package_type")

    @package_type.setter
    def package_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "package_type", value)


class Package(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 package_description: Optional[pulumi.Input[str]] = None,
                 package_name: Optional[pulumi.Input[str]] = None,
                 package_source: Optional[pulumi.Input[pulumi.InputType['PackagePackageSourceArgs']]] = None,
                 package_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages an AWS Opensearch Package.

        ## Example Usage

        ### Basic Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_std as std

        my_opensearch_packages = aws.s3.BucketV2("my_opensearch_packages", bucket="my-opensearch-packages")
        example = aws.s3.BucketObjectv2("example",
            bucket=my_opensearch_packages.bucket,
            key="example.txt",
            source=pulumi.FileAsset("./example.txt"),
            etag=std.filemd5(input="./example.txt").result)
        example_package = aws.opensearch.Package("example",
            package_name="example-txt",
            package_source=aws.opensearch.PackagePackageSourceArgs(
                s3_bucket_name=my_opensearch_packages.bucket,
                s3_key=example.key,
            ),
            package_type="TXT-DICTIONARY")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import AWS Opensearch Packages using the Package ID. For example:

        ```sh
        $ pulumi import aws:opensearch/package:Package example package-id
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] package_description: Description of the package.
        :param pulumi.Input[str] package_name: Unique name for the package.
        :param pulumi.Input[pulumi.InputType['PackagePackageSourceArgs']] package_source: Configuration block for the package source options.
        :param pulumi.Input[str] package_type: The type of package.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PackageArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an AWS Opensearch Package.

        ## Example Usage

        ### Basic Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_std as std

        my_opensearch_packages = aws.s3.BucketV2("my_opensearch_packages", bucket="my-opensearch-packages")
        example = aws.s3.BucketObjectv2("example",
            bucket=my_opensearch_packages.bucket,
            key="example.txt",
            source=pulumi.FileAsset("./example.txt"),
            etag=std.filemd5(input="./example.txt").result)
        example_package = aws.opensearch.Package("example",
            package_name="example-txt",
            package_source=aws.opensearch.PackagePackageSourceArgs(
                s3_bucket_name=my_opensearch_packages.bucket,
                s3_key=example.key,
            ),
            package_type="TXT-DICTIONARY")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import AWS Opensearch Packages using the Package ID. For example:

        ```sh
        $ pulumi import aws:opensearch/package:Package example package-id
        ```

        :param str resource_name: The name of the resource.
        :param PackageArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PackageArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 package_description: Optional[pulumi.Input[str]] = None,
                 package_name: Optional[pulumi.Input[str]] = None,
                 package_source: Optional[pulumi.Input[pulumi.InputType['PackagePackageSourceArgs']]] = None,
                 package_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PackageArgs.__new__(PackageArgs)

            __props__.__dict__["package_description"] = package_description
            if package_name is None and not opts.urn:
                raise TypeError("Missing required property 'package_name'")
            __props__.__dict__["package_name"] = package_name
            if package_source is None and not opts.urn:
                raise TypeError("Missing required property 'package_source'")
            __props__.__dict__["package_source"] = package_source
            if package_type is None and not opts.urn:
                raise TypeError("Missing required property 'package_type'")
            __props__.__dict__["package_type"] = package_type
            __props__.__dict__["available_package_version"] = None
            __props__.__dict__["package_id"] = None
        super(Package, __self__).__init__(
            'aws:opensearch/package:Package',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            available_package_version: Optional[pulumi.Input[str]] = None,
            package_description: Optional[pulumi.Input[str]] = None,
            package_id: Optional[pulumi.Input[str]] = None,
            package_name: Optional[pulumi.Input[str]] = None,
            package_source: Optional[pulumi.Input[pulumi.InputType['PackagePackageSourceArgs']]] = None,
            package_type: Optional[pulumi.Input[str]] = None) -> 'Package':
        """
        Get an existing Package resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] available_package_version: The current version of the package.
        :param pulumi.Input[str] package_description: Description of the package.
        :param pulumi.Input[str] package_name: Unique name for the package.
        :param pulumi.Input[pulumi.InputType['PackagePackageSourceArgs']] package_source: Configuration block for the package source options.
        :param pulumi.Input[str] package_type: The type of package.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PackageState.__new__(_PackageState)

        __props__.__dict__["available_package_version"] = available_package_version
        __props__.__dict__["package_description"] = package_description
        __props__.__dict__["package_id"] = package_id
        __props__.__dict__["package_name"] = package_name
        __props__.__dict__["package_source"] = package_source
        __props__.__dict__["package_type"] = package_type
        return Package(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="availablePackageVersion")
    def available_package_version(self) -> pulumi.Output[str]:
        """
        The current version of the package.
        """
        return pulumi.get(self, "available_package_version")

    @property
    @pulumi.getter(name="packageDescription")
    def package_description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the package.
        """
        return pulumi.get(self, "package_description")

    @property
    @pulumi.getter(name="packageId")
    def package_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "package_id")

    @property
    @pulumi.getter(name="packageName")
    def package_name(self) -> pulumi.Output[str]:
        """
        Unique name for the package.
        """
        return pulumi.get(self, "package_name")

    @property
    @pulumi.getter(name="packageSource")
    def package_source(self) -> pulumi.Output['outputs.PackagePackageSource']:
        """
        Configuration block for the package source options.
        """
        return pulumi.get(self, "package_source")

    @property
    @pulumi.getter(name="packageType")
    def package_type(self) -> pulumi.Output[str]:
        """
        The type of package.
        """
        return pulumi.get(self, "package_type")

