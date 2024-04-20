# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['TrustArgs', 'Trust']

@pulumi.input_type
class TrustArgs:
    def __init__(__self__, *,
                 directory_id: pulumi.Input[str],
                 remote_domain_name: pulumi.Input[str],
                 trust_direction: pulumi.Input[str],
                 trust_password: pulumi.Input[str],
                 conditional_forwarder_ip_addrs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 delete_associated_conditional_forwarder: Optional[pulumi.Input[bool]] = None,
                 selective_auth: Optional[pulumi.Input[str]] = None,
                 trust_type: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Trust resource.
        :param pulumi.Input[str] directory_id: ID of the Directory.
        :param pulumi.Input[str] remote_domain_name: Fully qualified domain name of the remote Directory.
        :param pulumi.Input[str] trust_direction: The direction of the Trust relationship.
               Valid values are `One-Way: Outgoing`, `One-Way: Incoming`, and `Two-Way`.
        :param pulumi.Input[str] trust_password: Password for the Trust.
               Does not need to match the passwords for either Directory.
               Can contain upper- and lower-case letters, numbers, and punctuation characters.
               May be up to 128 characters long.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] conditional_forwarder_ip_addrs: Set of IPv4 addresses for the DNS server associated with the remote Directory.
               Can contain between 1 and 4 values.
        :param pulumi.Input[bool] delete_associated_conditional_forwarder: Whether to delete the conditional forwarder when deleting the Trust relationship.
        :param pulumi.Input[str] selective_auth: Whether to enable selective authentication.
               Valid values are `Enabled` and `Disabled`.
               Default value is `Disabled`.
        :param pulumi.Input[str] trust_type: Type of the Trust relationship.
               Valid values are `Forest` and `External`.
               Default value is `Forest`.
        """
        pulumi.set(__self__, "directory_id", directory_id)
        pulumi.set(__self__, "remote_domain_name", remote_domain_name)
        pulumi.set(__self__, "trust_direction", trust_direction)
        pulumi.set(__self__, "trust_password", trust_password)
        if conditional_forwarder_ip_addrs is not None:
            pulumi.set(__self__, "conditional_forwarder_ip_addrs", conditional_forwarder_ip_addrs)
        if delete_associated_conditional_forwarder is not None:
            pulumi.set(__self__, "delete_associated_conditional_forwarder", delete_associated_conditional_forwarder)
        if selective_auth is not None:
            pulumi.set(__self__, "selective_auth", selective_auth)
        if trust_type is not None:
            pulumi.set(__self__, "trust_type", trust_type)

    @property
    @pulumi.getter(name="directoryId")
    def directory_id(self) -> pulumi.Input[str]:
        """
        ID of the Directory.
        """
        return pulumi.get(self, "directory_id")

    @directory_id.setter
    def directory_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "directory_id", value)

    @property
    @pulumi.getter(name="remoteDomainName")
    def remote_domain_name(self) -> pulumi.Input[str]:
        """
        Fully qualified domain name of the remote Directory.
        """
        return pulumi.get(self, "remote_domain_name")

    @remote_domain_name.setter
    def remote_domain_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "remote_domain_name", value)

    @property
    @pulumi.getter(name="trustDirection")
    def trust_direction(self) -> pulumi.Input[str]:
        """
        The direction of the Trust relationship.
        Valid values are `One-Way: Outgoing`, `One-Way: Incoming`, and `Two-Way`.
        """
        return pulumi.get(self, "trust_direction")

    @trust_direction.setter
    def trust_direction(self, value: pulumi.Input[str]):
        pulumi.set(self, "trust_direction", value)

    @property
    @pulumi.getter(name="trustPassword")
    def trust_password(self) -> pulumi.Input[str]:
        """
        Password for the Trust.
        Does not need to match the passwords for either Directory.
        Can contain upper- and lower-case letters, numbers, and punctuation characters.
        May be up to 128 characters long.
        """
        return pulumi.get(self, "trust_password")

    @trust_password.setter
    def trust_password(self, value: pulumi.Input[str]):
        pulumi.set(self, "trust_password", value)

    @property
    @pulumi.getter(name="conditionalForwarderIpAddrs")
    def conditional_forwarder_ip_addrs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Set of IPv4 addresses for the DNS server associated with the remote Directory.
        Can contain between 1 and 4 values.
        """
        return pulumi.get(self, "conditional_forwarder_ip_addrs")

    @conditional_forwarder_ip_addrs.setter
    def conditional_forwarder_ip_addrs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "conditional_forwarder_ip_addrs", value)

    @property
    @pulumi.getter(name="deleteAssociatedConditionalForwarder")
    def delete_associated_conditional_forwarder(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to delete the conditional forwarder when deleting the Trust relationship.
        """
        return pulumi.get(self, "delete_associated_conditional_forwarder")

    @delete_associated_conditional_forwarder.setter
    def delete_associated_conditional_forwarder(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delete_associated_conditional_forwarder", value)

    @property
    @pulumi.getter(name="selectiveAuth")
    def selective_auth(self) -> Optional[pulumi.Input[str]]:
        """
        Whether to enable selective authentication.
        Valid values are `Enabled` and `Disabled`.
        Default value is `Disabled`.
        """
        return pulumi.get(self, "selective_auth")

    @selective_auth.setter
    def selective_auth(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "selective_auth", value)

    @property
    @pulumi.getter(name="trustType")
    def trust_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of the Trust relationship.
        Valid values are `Forest` and `External`.
        Default value is `Forest`.
        """
        return pulumi.get(self, "trust_type")

    @trust_type.setter
    def trust_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "trust_type", value)


@pulumi.input_type
class _TrustState:
    def __init__(__self__, *,
                 conditional_forwarder_ip_addrs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 created_date_time: Optional[pulumi.Input[str]] = None,
                 delete_associated_conditional_forwarder: Optional[pulumi.Input[bool]] = None,
                 directory_id: Optional[pulumi.Input[str]] = None,
                 last_updated_date_time: Optional[pulumi.Input[str]] = None,
                 remote_domain_name: Optional[pulumi.Input[str]] = None,
                 selective_auth: Optional[pulumi.Input[str]] = None,
                 state_last_updated_date_time: Optional[pulumi.Input[str]] = None,
                 trust_direction: Optional[pulumi.Input[str]] = None,
                 trust_password: Optional[pulumi.Input[str]] = None,
                 trust_state: Optional[pulumi.Input[str]] = None,
                 trust_state_reason: Optional[pulumi.Input[str]] = None,
                 trust_type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Trust resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] conditional_forwarder_ip_addrs: Set of IPv4 addresses for the DNS server associated with the remote Directory.
               Can contain between 1 and 4 values.
        :param pulumi.Input[str] created_date_time: Date and time when the Trust was created.
        :param pulumi.Input[bool] delete_associated_conditional_forwarder: Whether to delete the conditional forwarder when deleting the Trust relationship.
        :param pulumi.Input[str] directory_id: ID of the Directory.
        :param pulumi.Input[str] last_updated_date_time: Date and time when the Trust was last updated.
        :param pulumi.Input[str] remote_domain_name: Fully qualified domain name of the remote Directory.
        :param pulumi.Input[str] selective_auth: Whether to enable selective authentication.
               Valid values are `Enabled` and `Disabled`.
               Default value is `Disabled`.
        :param pulumi.Input[str] state_last_updated_date_time: Date and time when the Trust state in `trust_state` was last updated.
        :param pulumi.Input[str] trust_direction: The direction of the Trust relationship.
               Valid values are `One-Way: Outgoing`, `One-Way: Incoming`, and `Two-Way`.
        :param pulumi.Input[str] trust_password: Password for the Trust.
               Does not need to match the passwords for either Directory.
               Can contain upper- and lower-case letters, numbers, and punctuation characters.
               May be up to 128 characters long.
        :param pulumi.Input[str] trust_state: State of the Trust relationship.
               One of `Created`, `VerifyFailed`,`Verified`, `UpdateFailed`,`Updated`,`Deleted`, or `Failed`.
        :param pulumi.Input[str] trust_state_reason: Reason for the Trust state set in `trust_state`.
        :param pulumi.Input[str] trust_type: Type of the Trust relationship.
               Valid values are `Forest` and `External`.
               Default value is `Forest`.
        """
        if conditional_forwarder_ip_addrs is not None:
            pulumi.set(__self__, "conditional_forwarder_ip_addrs", conditional_forwarder_ip_addrs)
        if created_date_time is not None:
            pulumi.set(__self__, "created_date_time", created_date_time)
        if delete_associated_conditional_forwarder is not None:
            pulumi.set(__self__, "delete_associated_conditional_forwarder", delete_associated_conditional_forwarder)
        if directory_id is not None:
            pulumi.set(__self__, "directory_id", directory_id)
        if last_updated_date_time is not None:
            pulumi.set(__self__, "last_updated_date_time", last_updated_date_time)
        if remote_domain_name is not None:
            pulumi.set(__self__, "remote_domain_name", remote_domain_name)
        if selective_auth is not None:
            pulumi.set(__self__, "selective_auth", selective_auth)
        if state_last_updated_date_time is not None:
            pulumi.set(__self__, "state_last_updated_date_time", state_last_updated_date_time)
        if trust_direction is not None:
            pulumi.set(__self__, "trust_direction", trust_direction)
        if trust_password is not None:
            pulumi.set(__self__, "trust_password", trust_password)
        if trust_state is not None:
            pulumi.set(__self__, "trust_state", trust_state)
        if trust_state_reason is not None:
            pulumi.set(__self__, "trust_state_reason", trust_state_reason)
        if trust_type is not None:
            pulumi.set(__self__, "trust_type", trust_type)

    @property
    @pulumi.getter(name="conditionalForwarderIpAddrs")
    def conditional_forwarder_ip_addrs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Set of IPv4 addresses for the DNS server associated with the remote Directory.
        Can contain between 1 and 4 values.
        """
        return pulumi.get(self, "conditional_forwarder_ip_addrs")

    @conditional_forwarder_ip_addrs.setter
    def conditional_forwarder_ip_addrs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "conditional_forwarder_ip_addrs", value)

    @property
    @pulumi.getter(name="createdDateTime")
    def created_date_time(self) -> Optional[pulumi.Input[str]]:
        """
        Date and time when the Trust was created.
        """
        return pulumi.get(self, "created_date_time")

    @created_date_time.setter
    def created_date_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_date_time", value)

    @property
    @pulumi.getter(name="deleteAssociatedConditionalForwarder")
    def delete_associated_conditional_forwarder(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to delete the conditional forwarder when deleting the Trust relationship.
        """
        return pulumi.get(self, "delete_associated_conditional_forwarder")

    @delete_associated_conditional_forwarder.setter
    def delete_associated_conditional_forwarder(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delete_associated_conditional_forwarder", value)

    @property
    @pulumi.getter(name="directoryId")
    def directory_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the Directory.
        """
        return pulumi.get(self, "directory_id")

    @directory_id.setter
    def directory_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "directory_id", value)

    @property
    @pulumi.getter(name="lastUpdatedDateTime")
    def last_updated_date_time(self) -> Optional[pulumi.Input[str]]:
        """
        Date and time when the Trust was last updated.
        """
        return pulumi.get(self, "last_updated_date_time")

    @last_updated_date_time.setter
    def last_updated_date_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_updated_date_time", value)

    @property
    @pulumi.getter(name="remoteDomainName")
    def remote_domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        Fully qualified domain name of the remote Directory.
        """
        return pulumi.get(self, "remote_domain_name")

    @remote_domain_name.setter
    def remote_domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "remote_domain_name", value)

    @property
    @pulumi.getter(name="selectiveAuth")
    def selective_auth(self) -> Optional[pulumi.Input[str]]:
        """
        Whether to enable selective authentication.
        Valid values are `Enabled` and `Disabled`.
        Default value is `Disabled`.
        """
        return pulumi.get(self, "selective_auth")

    @selective_auth.setter
    def selective_auth(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "selective_auth", value)

    @property
    @pulumi.getter(name="stateLastUpdatedDateTime")
    def state_last_updated_date_time(self) -> Optional[pulumi.Input[str]]:
        """
        Date and time when the Trust state in `trust_state` was last updated.
        """
        return pulumi.get(self, "state_last_updated_date_time")

    @state_last_updated_date_time.setter
    def state_last_updated_date_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state_last_updated_date_time", value)

    @property
    @pulumi.getter(name="trustDirection")
    def trust_direction(self) -> Optional[pulumi.Input[str]]:
        """
        The direction of the Trust relationship.
        Valid values are `One-Way: Outgoing`, `One-Way: Incoming`, and `Two-Way`.
        """
        return pulumi.get(self, "trust_direction")

    @trust_direction.setter
    def trust_direction(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "trust_direction", value)

    @property
    @pulumi.getter(name="trustPassword")
    def trust_password(self) -> Optional[pulumi.Input[str]]:
        """
        Password for the Trust.
        Does not need to match the passwords for either Directory.
        Can contain upper- and lower-case letters, numbers, and punctuation characters.
        May be up to 128 characters long.
        """
        return pulumi.get(self, "trust_password")

    @trust_password.setter
    def trust_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "trust_password", value)

    @property
    @pulumi.getter(name="trustState")
    def trust_state(self) -> Optional[pulumi.Input[str]]:
        """
        State of the Trust relationship.
        One of `Created`, `VerifyFailed`,`Verified`, `UpdateFailed`,`Updated`,`Deleted`, or `Failed`.
        """
        return pulumi.get(self, "trust_state")

    @trust_state.setter
    def trust_state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "trust_state", value)

    @property
    @pulumi.getter(name="trustStateReason")
    def trust_state_reason(self) -> Optional[pulumi.Input[str]]:
        """
        Reason for the Trust state set in `trust_state`.
        """
        return pulumi.get(self, "trust_state_reason")

    @trust_state_reason.setter
    def trust_state_reason(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "trust_state_reason", value)

    @property
    @pulumi.getter(name="trustType")
    def trust_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of the Trust relationship.
        Valid values are `Forest` and `External`.
        Default value is `Forest`.
        """
        return pulumi.get(self, "trust_type")

    @trust_type.setter
    def trust_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "trust_type", value)


class Trust(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 conditional_forwarder_ip_addrs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 delete_associated_conditional_forwarder: Optional[pulumi.Input[bool]] = None,
                 directory_id: Optional[pulumi.Input[str]] = None,
                 remote_domain_name: Optional[pulumi.Input[str]] = None,
                 selective_auth: Optional[pulumi.Input[str]] = None,
                 trust_direction: Optional[pulumi.Input[str]] = None,
                 trust_password: Optional[pulumi.Input[str]] = None,
                 trust_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a trust relationship between two Active Directory Directories.

        The directories may either be both AWS Managed Microsoft AD domains or an AWS Managed Microsoft AD domain and a self-managed Active Directory Domain.

        The Trust relationship must be configured on both sides of the relationship.
        If a Trust has only been created on one side, it will be in the state `VerifyFailed`.
        Once the second Trust is created, the first will update to the correct state.

        ## Example Usage

        ### Two-Way Trust

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        one_directory = aws.directoryservice.Directory("one",
            name="one.example.com",
            type="MicrosoftAD")
        two_directory = aws.directoryservice.Directory("two",
            name="two.example.com",
            type="MicrosoftAD")
        one = aws.directoryservice.Trust("one",
            directory_id=one_directory.id,
            remote_domain_name=two_directory.name,
            trust_direction="Two-Way",
            trust_password="Some0therPassword",
            conditional_forwarder_ip_addrs=two_directory.dns_ip_addresses)
        two = aws.directoryservice.Trust("two",
            directory_id=two_directory.id,
            remote_domain_name=one_directory.name,
            trust_direction="Two-Way",
            trust_password="Some0therPassword",
            conditional_forwarder_ip_addrs=one_directory.dns_ip_addresses)
        ```
        <!--End PulumiCodeChooser -->

        ### One-Way Trust

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        one_directory = aws.directoryservice.Directory("one",
            name="one.example.com",
            type="MicrosoftAD")
        two_directory = aws.directoryservice.Directory("two",
            name="two.example.com",
            type="MicrosoftAD")
        one = aws.directoryservice.Trust("one",
            directory_id=one_directory.id,
            remote_domain_name=two_directory.name,
            trust_direction="One-Way: Incoming",
            trust_password="Some0therPassword",
            conditional_forwarder_ip_addrs=two_directory.dns_ip_addresses)
        two = aws.directoryservice.Trust("two",
            directory_id=two_directory.id,
            remote_domain_name=one_directory.name,
            trust_direction="One-Way: Outgoing",
            trust_password="Some0therPassword",
            conditional_forwarder_ip_addrs=one_directory.dns_ip_addresses)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import the Trust relationship using the directory ID and remote domain name, separated by a `/`. For example:

        ```sh
        $ pulumi import aws:directoryservice/trust:Trust example d-926724cf57/directory.example.com
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] conditional_forwarder_ip_addrs: Set of IPv4 addresses for the DNS server associated with the remote Directory.
               Can contain between 1 and 4 values.
        :param pulumi.Input[bool] delete_associated_conditional_forwarder: Whether to delete the conditional forwarder when deleting the Trust relationship.
        :param pulumi.Input[str] directory_id: ID of the Directory.
        :param pulumi.Input[str] remote_domain_name: Fully qualified domain name of the remote Directory.
        :param pulumi.Input[str] selective_auth: Whether to enable selective authentication.
               Valid values are `Enabled` and `Disabled`.
               Default value is `Disabled`.
        :param pulumi.Input[str] trust_direction: The direction of the Trust relationship.
               Valid values are `One-Way: Outgoing`, `One-Way: Incoming`, and `Two-Way`.
        :param pulumi.Input[str] trust_password: Password for the Trust.
               Does not need to match the passwords for either Directory.
               Can contain upper- and lower-case letters, numbers, and punctuation characters.
               May be up to 128 characters long.
        :param pulumi.Input[str] trust_type: Type of the Trust relationship.
               Valid values are `Forest` and `External`.
               Default value is `Forest`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TrustArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a trust relationship between two Active Directory Directories.

        The directories may either be both AWS Managed Microsoft AD domains or an AWS Managed Microsoft AD domain and a self-managed Active Directory Domain.

        The Trust relationship must be configured on both sides of the relationship.
        If a Trust has only been created on one side, it will be in the state `VerifyFailed`.
        Once the second Trust is created, the first will update to the correct state.

        ## Example Usage

        ### Two-Way Trust

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        one_directory = aws.directoryservice.Directory("one",
            name="one.example.com",
            type="MicrosoftAD")
        two_directory = aws.directoryservice.Directory("two",
            name="two.example.com",
            type="MicrosoftAD")
        one = aws.directoryservice.Trust("one",
            directory_id=one_directory.id,
            remote_domain_name=two_directory.name,
            trust_direction="Two-Way",
            trust_password="Some0therPassword",
            conditional_forwarder_ip_addrs=two_directory.dns_ip_addresses)
        two = aws.directoryservice.Trust("two",
            directory_id=two_directory.id,
            remote_domain_name=one_directory.name,
            trust_direction="Two-Way",
            trust_password="Some0therPassword",
            conditional_forwarder_ip_addrs=one_directory.dns_ip_addresses)
        ```
        <!--End PulumiCodeChooser -->

        ### One-Way Trust

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        one_directory = aws.directoryservice.Directory("one",
            name="one.example.com",
            type="MicrosoftAD")
        two_directory = aws.directoryservice.Directory("two",
            name="two.example.com",
            type="MicrosoftAD")
        one = aws.directoryservice.Trust("one",
            directory_id=one_directory.id,
            remote_domain_name=two_directory.name,
            trust_direction="One-Way: Incoming",
            trust_password="Some0therPassword",
            conditional_forwarder_ip_addrs=two_directory.dns_ip_addresses)
        two = aws.directoryservice.Trust("two",
            directory_id=two_directory.id,
            remote_domain_name=one_directory.name,
            trust_direction="One-Way: Outgoing",
            trust_password="Some0therPassword",
            conditional_forwarder_ip_addrs=one_directory.dns_ip_addresses)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import the Trust relationship using the directory ID and remote domain name, separated by a `/`. For example:

        ```sh
        $ pulumi import aws:directoryservice/trust:Trust example d-926724cf57/directory.example.com
        ```

        :param str resource_name: The name of the resource.
        :param TrustArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TrustArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 conditional_forwarder_ip_addrs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 delete_associated_conditional_forwarder: Optional[pulumi.Input[bool]] = None,
                 directory_id: Optional[pulumi.Input[str]] = None,
                 remote_domain_name: Optional[pulumi.Input[str]] = None,
                 selective_auth: Optional[pulumi.Input[str]] = None,
                 trust_direction: Optional[pulumi.Input[str]] = None,
                 trust_password: Optional[pulumi.Input[str]] = None,
                 trust_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TrustArgs.__new__(TrustArgs)

            __props__.__dict__["conditional_forwarder_ip_addrs"] = conditional_forwarder_ip_addrs
            __props__.__dict__["delete_associated_conditional_forwarder"] = delete_associated_conditional_forwarder
            if directory_id is None and not opts.urn:
                raise TypeError("Missing required property 'directory_id'")
            __props__.__dict__["directory_id"] = directory_id
            if remote_domain_name is None and not opts.urn:
                raise TypeError("Missing required property 'remote_domain_name'")
            __props__.__dict__["remote_domain_name"] = remote_domain_name
            __props__.__dict__["selective_auth"] = selective_auth
            if trust_direction is None and not opts.urn:
                raise TypeError("Missing required property 'trust_direction'")
            __props__.__dict__["trust_direction"] = trust_direction
            if trust_password is None and not opts.urn:
                raise TypeError("Missing required property 'trust_password'")
            __props__.__dict__["trust_password"] = trust_password
            __props__.__dict__["trust_type"] = trust_type
            __props__.__dict__["created_date_time"] = None
            __props__.__dict__["last_updated_date_time"] = None
            __props__.__dict__["state_last_updated_date_time"] = None
            __props__.__dict__["trust_state"] = None
            __props__.__dict__["trust_state_reason"] = None
        super(Trust, __self__).__init__(
            'aws:directoryservice/trust:Trust',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            conditional_forwarder_ip_addrs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            created_date_time: Optional[pulumi.Input[str]] = None,
            delete_associated_conditional_forwarder: Optional[pulumi.Input[bool]] = None,
            directory_id: Optional[pulumi.Input[str]] = None,
            last_updated_date_time: Optional[pulumi.Input[str]] = None,
            remote_domain_name: Optional[pulumi.Input[str]] = None,
            selective_auth: Optional[pulumi.Input[str]] = None,
            state_last_updated_date_time: Optional[pulumi.Input[str]] = None,
            trust_direction: Optional[pulumi.Input[str]] = None,
            trust_password: Optional[pulumi.Input[str]] = None,
            trust_state: Optional[pulumi.Input[str]] = None,
            trust_state_reason: Optional[pulumi.Input[str]] = None,
            trust_type: Optional[pulumi.Input[str]] = None) -> 'Trust':
        """
        Get an existing Trust resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] conditional_forwarder_ip_addrs: Set of IPv4 addresses for the DNS server associated with the remote Directory.
               Can contain between 1 and 4 values.
        :param pulumi.Input[str] created_date_time: Date and time when the Trust was created.
        :param pulumi.Input[bool] delete_associated_conditional_forwarder: Whether to delete the conditional forwarder when deleting the Trust relationship.
        :param pulumi.Input[str] directory_id: ID of the Directory.
        :param pulumi.Input[str] last_updated_date_time: Date and time when the Trust was last updated.
        :param pulumi.Input[str] remote_domain_name: Fully qualified domain name of the remote Directory.
        :param pulumi.Input[str] selective_auth: Whether to enable selective authentication.
               Valid values are `Enabled` and `Disabled`.
               Default value is `Disabled`.
        :param pulumi.Input[str] state_last_updated_date_time: Date and time when the Trust state in `trust_state` was last updated.
        :param pulumi.Input[str] trust_direction: The direction of the Trust relationship.
               Valid values are `One-Way: Outgoing`, `One-Way: Incoming`, and `Two-Way`.
        :param pulumi.Input[str] trust_password: Password for the Trust.
               Does not need to match the passwords for either Directory.
               Can contain upper- and lower-case letters, numbers, and punctuation characters.
               May be up to 128 characters long.
        :param pulumi.Input[str] trust_state: State of the Trust relationship.
               One of `Created`, `VerifyFailed`,`Verified`, `UpdateFailed`,`Updated`,`Deleted`, or `Failed`.
        :param pulumi.Input[str] trust_state_reason: Reason for the Trust state set in `trust_state`.
        :param pulumi.Input[str] trust_type: Type of the Trust relationship.
               Valid values are `Forest` and `External`.
               Default value is `Forest`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TrustState.__new__(_TrustState)

        __props__.__dict__["conditional_forwarder_ip_addrs"] = conditional_forwarder_ip_addrs
        __props__.__dict__["created_date_time"] = created_date_time
        __props__.__dict__["delete_associated_conditional_forwarder"] = delete_associated_conditional_forwarder
        __props__.__dict__["directory_id"] = directory_id
        __props__.__dict__["last_updated_date_time"] = last_updated_date_time
        __props__.__dict__["remote_domain_name"] = remote_domain_name
        __props__.__dict__["selective_auth"] = selective_auth
        __props__.__dict__["state_last_updated_date_time"] = state_last_updated_date_time
        __props__.__dict__["trust_direction"] = trust_direction
        __props__.__dict__["trust_password"] = trust_password
        __props__.__dict__["trust_state"] = trust_state
        __props__.__dict__["trust_state_reason"] = trust_state_reason
        __props__.__dict__["trust_type"] = trust_type
        return Trust(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="conditionalForwarderIpAddrs")
    def conditional_forwarder_ip_addrs(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Set of IPv4 addresses for the DNS server associated with the remote Directory.
        Can contain between 1 and 4 values.
        """
        return pulumi.get(self, "conditional_forwarder_ip_addrs")

    @property
    @pulumi.getter(name="createdDateTime")
    def created_date_time(self) -> pulumi.Output[str]:
        """
        Date and time when the Trust was created.
        """
        return pulumi.get(self, "created_date_time")

    @property
    @pulumi.getter(name="deleteAssociatedConditionalForwarder")
    def delete_associated_conditional_forwarder(self) -> pulumi.Output[bool]:
        """
        Whether to delete the conditional forwarder when deleting the Trust relationship.
        """
        return pulumi.get(self, "delete_associated_conditional_forwarder")

    @property
    @pulumi.getter(name="directoryId")
    def directory_id(self) -> pulumi.Output[str]:
        """
        ID of the Directory.
        """
        return pulumi.get(self, "directory_id")

    @property
    @pulumi.getter(name="lastUpdatedDateTime")
    def last_updated_date_time(self) -> pulumi.Output[str]:
        """
        Date and time when the Trust was last updated.
        """
        return pulumi.get(self, "last_updated_date_time")

    @property
    @pulumi.getter(name="remoteDomainName")
    def remote_domain_name(self) -> pulumi.Output[str]:
        """
        Fully qualified domain name of the remote Directory.
        """
        return pulumi.get(self, "remote_domain_name")

    @property
    @pulumi.getter(name="selectiveAuth")
    def selective_auth(self) -> pulumi.Output[str]:
        """
        Whether to enable selective authentication.
        Valid values are `Enabled` and `Disabled`.
        Default value is `Disabled`.
        """
        return pulumi.get(self, "selective_auth")

    @property
    @pulumi.getter(name="stateLastUpdatedDateTime")
    def state_last_updated_date_time(self) -> pulumi.Output[str]:
        """
        Date and time when the Trust state in `trust_state` was last updated.
        """
        return pulumi.get(self, "state_last_updated_date_time")

    @property
    @pulumi.getter(name="trustDirection")
    def trust_direction(self) -> pulumi.Output[str]:
        """
        The direction of the Trust relationship.
        Valid values are `One-Way: Outgoing`, `One-Way: Incoming`, and `Two-Way`.
        """
        return pulumi.get(self, "trust_direction")

    @property
    @pulumi.getter(name="trustPassword")
    def trust_password(self) -> pulumi.Output[str]:
        """
        Password for the Trust.
        Does not need to match the passwords for either Directory.
        Can contain upper- and lower-case letters, numbers, and punctuation characters.
        May be up to 128 characters long.
        """
        return pulumi.get(self, "trust_password")

    @property
    @pulumi.getter(name="trustState")
    def trust_state(self) -> pulumi.Output[str]:
        """
        State of the Trust relationship.
        One of `Created`, `VerifyFailed`,`Verified`, `UpdateFailed`,`Updated`,`Deleted`, or `Failed`.
        """
        return pulumi.get(self, "trust_state")

    @property
    @pulumi.getter(name="trustStateReason")
    def trust_state_reason(self) -> pulumi.Output[str]:
        """
        Reason for the Trust state set in `trust_state`.
        """
        return pulumi.get(self, "trust_state_reason")

    @property
    @pulumi.getter(name="trustType")
    def trust_type(self) -> pulumi.Output[str]:
        """
        Type of the Trust relationship.
        Valid values are `Forest` and `External`.
        Default value is `Forest`.
        """
        return pulumi.get(self, "trust_type")

