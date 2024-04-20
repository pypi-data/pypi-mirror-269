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

__all__ = ['DeviceArgs', 'Device']

@pulumi.input_type
class DeviceArgs:
    def __init__(__self__, *,
                 device: pulumi.Input['DeviceDeviceArgs'],
                 device_fleet_name: pulumi.Input[str]):
        """
        The set of arguments for constructing a Device resource.
        :param pulumi.Input['DeviceDeviceArgs'] device: The device to register with SageMaker Edge Manager. See Device details below.
        :param pulumi.Input[str] device_fleet_name: The name of the Device Fleet.
        """
        pulumi.set(__self__, "device", device)
        pulumi.set(__self__, "device_fleet_name", device_fleet_name)

    @property
    @pulumi.getter
    def device(self) -> pulumi.Input['DeviceDeviceArgs']:
        """
        The device to register with SageMaker Edge Manager. See Device details below.
        """
        return pulumi.get(self, "device")

    @device.setter
    def device(self, value: pulumi.Input['DeviceDeviceArgs']):
        pulumi.set(self, "device", value)

    @property
    @pulumi.getter(name="deviceFleetName")
    def device_fleet_name(self) -> pulumi.Input[str]:
        """
        The name of the Device Fleet.
        """
        return pulumi.get(self, "device_fleet_name")

    @device_fleet_name.setter
    def device_fleet_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "device_fleet_name", value)


@pulumi.input_type
class _DeviceState:
    def __init__(__self__, *,
                 agent_version: Optional[pulumi.Input[str]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 device: Optional[pulumi.Input['DeviceDeviceArgs']] = None,
                 device_fleet_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Device resources.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) assigned by AWS to this Device.
        :param pulumi.Input['DeviceDeviceArgs'] device: The device to register with SageMaker Edge Manager. See Device details below.
        :param pulumi.Input[str] device_fleet_name: The name of the Device Fleet.
        """
        if agent_version is not None:
            pulumi.set(__self__, "agent_version", agent_version)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if device is not None:
            pulumi.set(__self__, "device", device)
        if device_fleet_name is not None:
            pulumi.set(__self__, "device_fleet_name", device_fleet_name)

    @property
    @pulumi.getter(name="agentVersion")
    def agent_version(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "agent_version")

    @agent_version.setter
    def agent_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "agent_version", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) assigned by AWS to this Device.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def device(self) -> Optional[pulumi.Input['DeviceDeviceArgs']]:
        """
        The device to register with SageMaker Edge Manager. See Device details below.
        """
        return pulumi.get(self, "device")

    @device.setter
    def device(self, value: Optional[pulumi.Input['DeviceDeviceArgs']]):
        pulumi.set(self, "device", value)

    @property
    @pulumi.getter(name="deviceFleetName")
    def device_fleet_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Device Fleet.
        """
        return pulumi.get(self, "device_fleet_name")

    @device_fleet_name.setter
    def device_fleet_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "device_fleet_name", value)


class Device(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device: Optional[pulumi.Input[pulumi.InputType['DeviceDeviceArgs']]] = None,
                 device_fleet_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a SageMaker Device resource.

        ## Example Usage

        ### Basic usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sagemaker.Device("example",
            device_fleet_name=example_aws_sagemaker_device_fleet["deviceFleetName"],
            device=aws.sagemaker.DeviceDeviceArgs(
                device_name="example",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import SageMaker Devices using the `device-fleet-name/device-name`. For example:

        ```sh
        $ pulumi import aws:sagemaker/device:Device example my-fleet/my-device
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['DeviceDeviceArgs']] device: The device to register with SageMaker Edge Manager. See Device details below.
        :param pulumi.Input[str] device_fleet_name: The name of the Device Fleet.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DeviceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a SageMaker Device resource.

        ## Example Usage

        ### Basic usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sagemaker.Device("example",
            device_fleet_name=example_aws_sagemaker_device_fleet["deviceFleetName"],
            device=aws.sagemaker.DeviceDeviceArgs(
                device_name="example",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import SageMaker Devices using the `device-fleet-name/device-name`. For example:

        ```sh
        $ pulumi import aws:sagemaker/device:Device example my-fleet/my-device
        ```

        :param str resource_name: The name of the resource.
        :param DeviceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DeviceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device: Optional[pulumi.Input[pulumi.InputType['DeviceDeviceArgs']]] = None,
                 device_fleet_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DeviceArgs.__new__(DeviceArgs)

            if device is None and not opts.urn:
                raise TypeError("Missing required property 'device'")
            __props__.__dict__["device"] = device
            if device_fleet_name is None and not opts.urn:
                raise TypeError("Missing required property 'device_fleet_name'")
            __props__.__dict__["device_fleet_name"] = device_fleet_name
            __props__.__dict__["agent_version"] = None
            __props__.__dict__["arn"] = None
        super(Device, __self__).__init__(
            'aws:sagemaker/device:Device',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            agent_version: Optional[pulumi.Input[str]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            device: Optional[pulumi.Input[pulumi.InputType['DeviceDeviceArgs']]] = None,
            device_fleet_name: Optional[pulumi.Input[str]] = None) -> 'Device':
        """
        Get an existing Device resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) assigned by AWS to this Device.
        :param pulumi.Input[pulumi.InputType['DeviceDeviceArgs']] device: The device to register with SageMaker Edge Manager. See Device details below.
        :param pulumi.Input[str] device_fleet_name: The name of the Device Fleet.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DeviceState.__new__(_DeviceState)

        __props__.__dict__["agent_version"] = agent_version
        __props__.__dict__["arn"] = arn
        __props__.__dict__["device"] = device
        __props__.__dict__["device_fleet_name"] = device_fleet_name
        return Device(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="agentVersion")
    def agent_version(self) -> pulumi.Output[str]:
        return pulumi.get(self, "agent_version")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) assigned by AWS to this Device.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def device(self) -> pulumi.Output['outputs.DeviceDevice']:
        """
        The device to register with SageMaker Edge Manager. See Device details below.
        """
        return pulumi.get(self, "device")

    @property
    @pulumi.getter(name="deviceFleetName")
    def device_fleet_name(self) -> pulumi.Output[str]:
        """
        The name of the Device Fleet.
        """
        return pulumi.get(self, "device_fleet_name")

