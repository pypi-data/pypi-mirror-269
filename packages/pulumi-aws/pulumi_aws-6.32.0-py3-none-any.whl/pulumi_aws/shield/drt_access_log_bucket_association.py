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

__all__ = ['DrtAccessLogBucketAssociationArgs', 'DrtAccessLogBucketAssociation']

@pulumi.input_type
class DrtAccessLogBucketAssociationArgs:
    def __init__(__self__, *,
                 log_bucket: pulumi.Input[str],
                 role_arn_association_id: pulumi.Input[str],
                 timeouts: Optional[pulumi.Input['DrtAccessLogBucketAssociationTimeoutsArgs']] = None):
        """
        The set of arguments for constructing a DrtAccessLogBucketAssociation resource.
        :param pulumi.Input[str] log_bucket: The Amazon S3 bucket that contains the logs that you want to share.
        :param pulumi.Input[str] role_arn_association_id: The ID of the Role Arn association used for allowing Shield DRT Access.
        """
        pulumi.set(__self__, "log_bucket", log_bucket)
        pulumi.set(__self__, "role_arn_association_id", role_arn_association_id)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)

    @property
    @pulumi.getter(name="logBucket")
    def log_bucket(self) -> pulumi.Input[str]:
        """
        The Amazon S3 bucket that contains the logs that you want to share.
        """
        return pulumi.get(self, "log_bucket")

    @log_bucket.setter
    def log_bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_bucket", value)

    @property
    @pulumi.getter(name="roleArnAssociationId")
    def role_arn_association_id(self) -> pulumi.Input[str]:
        """
        The ID of the Role Arn association used for allowing Shield DRT Access.
        """
        return pulumi.get(self, "role_arn_association_id")

    @role_arn_association_id.setter
    def role_arn_association_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_arn_association_id", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input['DrtAccessLogBucketAssociationTimeoutsArgs']]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input['DrtAccessLogBucketAssociationTimeoutsArgs']]):
        pulumi.set(self, "timeouts", value)


@pulumi.input_type
class _DrtAccessLogBucketAssociationState:
    def __init__(__self__, *,
                 log_bucket: Optional[pulumi.Input[str]] = None,
                 role_arn_association_id: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input['DrtAccessLogBucketAssociationTimeoutsArgs']] = None):
        """
        Input properties used for looking up and filtering DrtAccessLogBucketAssociation resources.
        :param pulumi.Input[str] log_bucket: The Amazon S3 bucket that contains the logs that you want to share.
        :param pulumi.Input[str] role_arn_association_id: The ID of the Role Arn association used for allowing Shield DRT Access.
        """
        if log_bucket is not None:
            pulumi.set(__self__, "log_bucket", log_bucket)
        if role_arn_association_id is not None:
            pulumi.set(__self__, "role_arn_association_id", role_arn_association_id)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)

    @property
    @pulumi.getter(name="logBucket")
    def log_bucket(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon S3 bucket that contains the logs that you want to share.
        """
        return pulumi.get(self, "log_bucket")

    @log_bucket.setter
    def log_bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_bucket", value)

    @property
    @pulumi.getter(name="roleArnAssociationId")
    def role_arn_association_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Role Arn association used for allowing Shield DRT Access.
        """
        return pulumi.get(self, "role_arn_association_id")

    @role_arn_association_id.setter
    def role_arn_association_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_arn_association_id", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input['DrtAccessLogBucketAssociationTimeoutsArgs']]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input['DrtAccessLogBucketAssociationTimeoutsArgs']]):
        pulumi.set(self, "timeouts", value)


class DrtAccessLogBucketAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 log_bucket: Optional[pulumi.Input[str]] = None,
                 role_arn_association_id: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input[pulumi.InputType['DrtAccessLogBucketAssociationTimeoutsArgs']]] = None,
                 __props__=None):
        """
        Resource for managing an AWS Shield DRT Access Log Bucket Association.
        Up to 10 log buckets can be associated for DRT Access sharing with the Shield Response Team (SRT).

        ## Example Usage

        ### Basic Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.shield.DrtAccessRoleArnAssociation("test", role_arn=f"arn:aws:iam:{current['name']}:{current_aws_caller_identity['accountId']}:{shield_drt_access_role_name}")
        test_drt_access_log_bucket_association = aws.shield.DrtAccessLogBucketAssociation("test",
            log_bucket=shield_drt_access_log_bucket,
            role_arn_association_id=test.id)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Shield DRT access log bucket associations using the `log_bucket`. For example:

        ```sh
        $ pulumi import aws:shield/drtAccessLogBucketAssociation:DrtAccessLogBucketAssociation example example-bucket
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] log_bucket: The Amazon S3 bucket that contains the logs that you want to share.
        :param pulumi.Input[str] role_arn_association_id: The ID of the Role Arn association used for allowing Shield DRT Access.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DrtAccessLogBucketAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS Shield DRT Access Log Bucket Association.
        Up to 10 log buckets can be associated for DRT Access sharing with the Shield Response Team (SRT).

        ## Example Usage

        ### Basic Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.shield.DrtAccessRoleArnAssociation("test", role_arn=f"arn:aws:iam:{current['name']}:{current_aws_caller_identity['accountId']}:{shield_drt_access_role_name}")
        test_drt_access_log_bucket_association = aws.shield.DrtAccessLogBucketAssociation("test",
            log_bucket=shield_drt_access_log_bucket,
            role_arn_association_id=test.id)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Shield DRT access log bucket associations using the `log_bucket`. For example:

        ```sh
        $ pulumi import aws:shield/drtAccessLogBucketAssociation:DrtAccessLogBucketAssociation example example-bucket
        ```

        :param str resource_name: The name of the resource.
        :param DrtAccessLogBucketAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DrtAccessLogBucketAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 log_bucket: Optional[pulumi.Input[str]] = None,
                 role_arn_association_id: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input[pulumi.InputType['DrtAccessLogBucketAssociationTimeoutsArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DrtAccessLogBucketAssociationArgs.__new__(DrtAccessLogBucketAssociationArgs)

            if log_bucket is None and not opts.urn:
                raise TypeError("Missing required property 'log_bucket'")
            __props__.__dict__["log_bucket"] = log_bucket
            if role_arn_association_id is None and not opts.urn:
                raise TypeError("Missing required property 'role_arn_association_id'")
            __props__.__dict__["role_arn_association_id"] = role_arn_association_id
            __props__.__dict__["timeouts"] = timeouts
        super(DrtAccessLogBucketAssociation, __self__).__init__(
            'aws:shield/drtAccessLogBucketAssociation:DrtAccessLogBucketAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            log_bucket: Optional[pulumi.Input[str]] = None,
            role_arn_association_id: Optional[pulumi.Input[str]] = None,
            timeouts: Optional[pulumi.Input[pulumi.InputType['DrtAccessLogBucketAssociationTimeoutsArgs']]] = None) -> 'DrtAccessLogBucketAssociation':
        """
        Get an existing DrtAccessLogBucketAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] log_bucket: The Amazon S3 bucket that contains the logs that you want to share.
        :param pulumi.Input[str] role_arn_association_id: The ID of the Role Arn association used for allowing Shield DRT Access.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DrtAccessLogBucketAssociationState.__new__(_DrtAccessLogBucketAssociationState)

        __props__.__dict__["log_bucket"] = log_bucket
        __props__.__dict__["role_arn_association_id"] = role_arn_association_id
        __props__.__dict__["timeouts"] = timeouts
        return DrtAccessLogBucketAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="logBucket")
    def log_bucket(self) -> pulumi.Output[str]:
        """
        The Amazon S3 bucket that contains the logs that you want to share.
        """
        return pulumi.get(self, "log_bucket")

    @property
    @pulumi.getter(name="roleArnAssociationId")
    def role_arn_association_id(self) -> pulumi.Output[str]:
        """
        The ID of the Role Arn association used for allowing Shield DRT Access.
        """
        return pulumi.get(self, "role_arn_association_id")

    @property
    @pulumi.getter
    def timeouts(self) -> pulumi.Output[Optional['outputs.DrtAccessLogBucketAssociationTimeouts']]:
        return pulumi.get(self, "timeouts")

