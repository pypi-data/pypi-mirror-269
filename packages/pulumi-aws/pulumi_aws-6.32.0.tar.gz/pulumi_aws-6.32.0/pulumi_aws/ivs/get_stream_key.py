# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetStreamKeyResult',
    'AwaitableGetStreamKeyResult',
    'get_stream_key',
    'get_stream_key_output',
]

@pulumi.output_type
class GetStreamKeyResult:
    """
    A collection of values returned by getStreamKey.
    """
    def __init__(__self__, arn=None, channel_arn=None, id=None, tags=None, value=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if channel_arn and not isinstance(channel_arn, str):
            raise TypeError("Expected argument 'channel_arn' to be a str")
        pulumi.set(__self__, "channel_arn", channel_arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if value and not isinstance(value, str):
            raise TypeError("Expected argument 'value' to be a str")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the Stream Key.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="channelArn")
    def channel_arn(self) -> str:
        return pulumi.get(self, "channel_arn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Map of tags assigned to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Stream Key value.
        """
        return pulumi.get(self, "value")


class AwaitableGetStreamKeyResult(GetStreamKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStreamKeyResult(
            arn=self.arn,
            channel_arn=self.channel_arn,
            id=self.id,
            tags=self.tags,
            value=self.value)


def get_stream_key(channel_arn: Optional[str] = None,
                   tags: Optional[Mapping[str, str]] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStreamKeyResult:
    """
    Data source for managing an AWS IVS (Interactive Video) Stream Key.

    ## Example Usage

    ### Basic Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ivs.get_stream_key(channel_arn="arn:aws:ivs:us-west-2:326937407773:channel/0Y1lcs4U7jk5")
    ```
    <!--End PulumiCodeChooser -->


    :param str channel_arn: ARN of the Channel.
    :param Mapping[str, str] tags: Map of tags assigned to the resource.
    """
    __args__ = dict()
    __args__['channelArn'] = channel_arn
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ivs/getStreamKey:getStreamKey', __args__, opts=opts, typ=GetStreamKeyResult).value

    return AwaitableGetStreamKeyResult(
        arn=pulumi.get(__ret__, 'arn'),
        channel_arn=pulumi.get(__ret__, 'channel_arn'),
        id=pulumi.get(__ret__, 'id'),
        tags=pulumi.get(__ret__, 'tags'),
        value=pulumi.get(__ret__, 'value'))


@_utilities.lift_output_func(get_stream_key)
def get_stream_key_output(channel_arn: Optional[pulumi.Input[str]] = None,
                          tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetStreamKeyResult]:
    """
    Data source for managing an AWS IVS (Interactive Video) Stream Key.

    ## Example Usage

    ### Basic Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ivs.get_stream_key(channel_arn="arn:aws:ivs:us-west-2:326937407773:channel/0Y1lcs4U7jk5")
    ```
    <!--End PulumiCodeChooser -->


    :param str channel_arn: ARN of the Channel.
    :param Mapping[str, str] tags: Map of tags assigned to the resource.
    """
    ...
