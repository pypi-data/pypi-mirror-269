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

__all__ = [
    'GetVolumeResult',
    'AwaitableGetVolumeResult',
    'get_volume',
    'get_volume_output',
]

@pulumi.output_type
class GetVolumeResult:
    """
    A collection of values returned by getVolume.
    """
    def __init__(__self__, arn=None, availability_zone=None, encrypted=None, filters=None, id=None, iops=None, kms_key_id=None, most_recent=None, multi_attach_enabled=None, outpost_arn=None, size=None, snapshot_id=None, tags=None, throughput=None, volume_id=None, volume_type=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if availability_zone and not isinstance(availability_zone, str):
            raise TypeError("Expected argument 'availability_zone' to be a str")
        pulumi.set(__self__, "availability_zone", availability_zone)
        if encrypted and not isinstance(encrypted, bool):
            raise TypeError("Expected argument 'encrypted' to be a bool")
        pulumi.set(__self__, "encrypted", encrypted)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if iops and not isinstance(iops, int):
            raise TypeError("Expected argument 'iops' to be a int")
        pulumi.set(__self__, "iops", iops)
        if kms_key_id and not isinstance(kms_key_id, str):
            raise TypeError("Expected argument 'kms_key_id' to be a str")
        pulumi.set(__self__, "kms_key_id", kms_key_id)
        if most_recent and not isinstance(most_recent, bool):
            raise TypeError("Expected argument 'most_recent' to be a bool")
        pulumi.set(__self__, "most_recent", most_recent)
        if multi_attach_enabled and not isinstance(multi_attach_enabled, bool):
            raise TypeError("Expected argument 'multi_attach_enabled' to be a bool")
        pulumi.set(__self__, "multi_attach_enabled", multi_attach_enabled)
        if outpost_arn and not isinstance(outpost_arn, str):
            raise TypeError("Expected argument 'outpost_arn' to be a str")
        pulumi.set(__self__, "outpost_arn", outpost_arn)
        if size and not isinstance(size, int):
            raise TypeError("Expected argument 'size' to be a int")
        pulumi.set(__self__, "size", size)
        if snapshot_id and not isinstance(snapshot_id, str):
            raise TypeError("Expected argument 'snapshot_id' to be a str")
        pulumi.set(__self__, "snapshot_id", snapshot_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if throughput and not isinstance(throughput, int):
            raise TypeError("Expected argument 'throughput' to be a int")
        pulumi.set(__self__, "throughput", throughput)
        if volume_id and not isinstance(volume_id, str):
            raise TypeError("Expected argument 'volume_id' to be a str")
        pulumi.set(__self__, "volume_id", volume_id)
        if volume_type and not isinstance(volume_type, str):
            raise TypeError("Expected argument 'volume_type' to be a str")
        pulumi.set(__self__, "volume_type", volume_type)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        Volume ARN (e.g., arn:aws:ec2:us-east-1:0123456789012:volume/vol-59fcb34e).
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> str:
        """
        AZ where the EBS volume exists.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter
    def encrypted(self) -> bool:
        """
        Whether the disk is encrypted.
        """
        return pulumi.get(self, "encrypted")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetVolumeFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def iops(self) -> int:
        """
        Amount of IOPS for the disk.
        """
        return pulumi.get(self, "iops")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> str:
        """
        ARN for the KMS encryption key.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="mostRecent")
    def most_recent(self) -> Optional[bool]:
        return pulumi.get(self, "most_recent")

    @property
    @pulumi.getter(name="multiAttachEnabled")
    def multi_attach_enabled(self) -> bool:
        """
        (Optional) Specifies whether Amazon EBS Multi-Attach is enabled.
        """
        return pulumi.get(self, "multi_attach_enabled")

    @property
    @pulumi.getter(name="outpostArn")
    def outpost_arn(self) -> str:
        """
        ARN of the Outpost.
        """
        return pulumi.get(self, "outpost_arn")

    @property
    @pulumi.getter
    def size(self) -> int:
        """
        Size of the drive in GiBs.
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter(name="snapshotId")
    def snapshot_id(self) -> str:
        """
        Snapshot_id the EBS volume is based off.
        """
        return pulumi.get(self, "snapshot_id")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Map of tags for the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def throughput(self) -> int:
        """
        Throughput that the volume supports, in MiB/s.
        """
        return pulumi.get(self, "throughput")

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> str:
        """
        Volume ID (e.g., vol-59fcb34e).
        """
        return pulumi.get(self, "volume_id")

    @property
    @pulumi.getter(name="volumeType")
    def volume_type(self) -> str:
        """
        Type of EBS volume.
        """
        return pulumi.get(self, "volume_type")


class AwaitableGetVolumeResult(GetVolumeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVolumeResult(
            arn=self.arn,
            availability_zone=self.availability_zone,
            encrypted=self.encrypted,
            filters=self.filters,
            id=self.id,
            iops=self.iops,
            kms_key_id=self.kms_key_id,
            most_recent=self.most_recent,
            multi_attach_enabled=self.multi_attach_enabled,
            outpost_arn=self.outpost_arn,
            size=self.size,
            snapshot_id=self.snapshot_id,
            tags=self.tags,
            throughput=self.throughput,
            volume_id=self.volume_id,
            volume_type=self.volume_type)


def get_volume(filters: Optional[Sequence[pulumi.InputType['GetVolumeFilterArgs']]] = None,
               most_recent: Optional[bool] = None,
               tags: Optional[Mapping[str, str]] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVolumeResult:
    """
    Use this data source to get information about an EBS volume for use in other
    resources.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    ebs_volume = aws.ebs.get_volume(most_recent=True,
        filters=[
            aws.ebs.GetVolumeFilterArgs(
                name="volume-type",
                values=["gp2"],
            ),
            aws.ebs.GetVolumeFilterArgs(
                name="tag:Name",
                values=["Example"],
            ),
        ])
    ```
    <!--End PulumiCodeChooser -->


    :param Sequence[pulumi.InputType['GetVolumeFilterArgs']] filters: One or more name/value pairs to filter off of. There are
           several valid keys, for a full reference, check out
           [describe-volumes in the AWS CLI reference][1].
    :param bool most_recent: If more than one result is returned, use the most
           recent Volume.
    :param Mapping[str, str] tags: Map of tags for the resource.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['mostRecent'] = most_recent
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ebs/getVolume:getVolume', __args__, opts=opts, typ=GetVolumeResult).value

    return AwaitableGetVolumeResult(
        arn=pulumi.get(__ret__, 'arn'),
        availability_zone=pulumi.get(__ret__, 'availability_zone'),
        encrypted=pulumi.get(__ret__, 'encrypted'),
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        iops=pulumi.get(__ret__, 'iops'),
        kms_key_id=pulumi.get(__ret__, 'kms_key_id'),
        most_recent=pulumi.get(__ret__, 'most_recent'),
        multi_attach_enabled=pulumi.get(__ret__, 'multi_attach_enabled'),
        outpost_arn=pulumi.get(__ret__, 'outpost_arn'),
        size=pulumi.get(__ret__, 'size'),
        snapshot_id=pulumi.get(__ret__, 'snapshot_id'),
        tags=pulumi.get(__ret__, 'tags'),
        throughput=pulumi.get(__ret__, 'throughput'),
        volume_id=pulumi.get(__ret__, 'volume_id'),
        volume_type=pulumi.get(__ret__, 'volume_type'))


@_utilities.lift_output_func(get_volume)
def get_volume_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetVolumeFilterArgs']]]]] = None,
                      most_recent: Optional[pulumi.Input[Optional[bool]]] = None,
                      tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVolumeResult]:
    """
    Use this data source to get information about an EBS volume for use in other
    resources.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    ebs_volume = aws.ebs.get_volume(most_recent=True,
        filters=[
            aws.ebs.GetVolumeFilterArgs(
                name="volume-type",
                values=["gp2"],
            ),
            aws.ebs.GetVolumeFilterArgs(
                name="tag:Name",
                values=["Example"],
            ),
        ])
    ```
    <!--End PulumiCodeChooser -->


    :param Sequence[pulumi.InputType['GetVolumeFilterArgs']] filters: One or more name/value pairs to filter off of. There are
           several valid keys, for a full reference, check out
           [describe-volumes in the AWS CLI reference][1].
    :param bool most_recent: If more than one result is returned, use the most
           recent Volume.
    :param Mapping[str, str] tags: Map of tags for the resource.
    """
    ...
