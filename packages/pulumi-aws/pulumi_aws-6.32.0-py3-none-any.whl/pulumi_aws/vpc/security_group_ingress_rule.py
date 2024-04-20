# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SecurityGroupIngressRuleArgs', 'SecurityGroupIngressRule']

@pulumi.input_type
class SecurityGroupIngressRuleArgs:
    def __init__(__self__, *,
                 ip_protocol: pulumi.Input[str],
                 security_group_id: pulumi.Input[str],
                 cidr_ipv4: Optional[pulumi.Input[str]] = None,
                 cidr_ipv6: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 from_port: Optional[pulumi.Input[int]] = None,
                 prefix_list_id: Optional[pulumi.Input[str]] = None,
                 referenced_security_group_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 to_port: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a SecurityGroupIngressRule resource.
        :param pulumi.Input[str] ip_protocol: The IP protocol name or number. Use `-1` to specify all protocols. Note that if `ip_protocol` is set to `-1`, it translates to all protocols, all port ranges, and `from_port` and `to_port` values should not be defined.
        :param pulumi.Input[str] security_group_id: The ID of the security group.
        :param pulumi.Input[str] cidr_ipv4: The source IPv4 CIDR range.
        :param pulumi.Input[str] cidr_ipv6: The source IPv6 CIDR range.
        :param pulumi.Input[str] description: The security group rule description.
        :param pulumi.Input[int] from_port: The start of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 type.
        :param pulumi.Input[str] prefix_list_id: The ID of the source prefix list.
        :param pulumi.Input[str] referenced_security_group_id: The source security group that is referenced in the rule.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[int] to_port: The end of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 code.
        """
        pulumi.set(__self__, "ip_protocol", ip_protocol)
        pulumi.set(__self__, "security_group_id", security_group_id)
        if cidr_ipv4 is not None:
            pulumi.set(__self__, "cidr_ipv4", cidr_ipv4)
        if cidr_ipv6 is not None:
            pulumi.set(__self__, "cidr_ipv6", cidr_ipv6)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if from_port is not None:
            pulumi.set(__self__, "from_port", from_port)
        if prefix_list_id is not None:
            pulumi.set(__self__, "prefix_list_id", prefix_list_id)
        if referenced_security_group_id is not None:
            pulumi.set(__self__, "referenced_security_group_id", referenced_security_group_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if to_port is not None:
            pulumi.set(__self__, "to_port", to_port)

    @property
    @pulumi.getter(name="ipProtocol")
    def ip_protocol(self) -> pulumi.Input[str]:
        """
        The IP protocol name or number. Use `-1` to specify all protocols. Note that if `ip_protocol` is set to `-1`, it translates to all protocols, all port ranges, and `from_port` and `to_port` values should not be defined.
        """
        return pulumi.get(self, "ip_protocol")

    @ip_protocol.setter
    def ip_protocol(self, value: pulumi.Input[str]):
        pulumi.set(self, "ip_protocol", value)

    @property
    @pulumi.getter(name="securityGroupId")
    def security_group_id(self) -> pulumi.Input[str]:
        """
        The ID of the security group.
        """
        return pulumi.get(self, "security_group_id")

    @security_group_id.setter
    def security_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "security_group_id", value)

    @property
    @pulumi.getter(name="cidrIpv4")
    def cidr_ipv4(self) -> Optional[pulumi.Input[str]]:
        """
        The source IPv4 CIDR range.
        """
        return pulumi.get(self, "cidr_ipv4")

    @cidr_ipv4.setter
    def cidr_ipv4(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cidr_ipv4", value)

    @property
    @pulumi.getter(name="cidrIpv6")
    def cidr_ipv6(self) -> Optional[pulumi.Input[str]]:
        """
        The source IPv6 CIDR range.
        """
        return pulumi.get(self, "cidr_ipv6")

    @cidr_ipv6.setter
    def cidr_ipv6(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cidr_ipv6", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The security group rule description.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="fromPort")
    def from_port(self) -> Optional[pulumi.Input[int]]:
        """
        The start of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 type.
        """
        return pulumi.get(self, "from_port")

    @from_port.setter
    def from_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "from_port", value)

    @property
    @pulumi.getter(name="prefixListId")
    def prefix_list_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the source prefix list.
        """
        return pulumi.get(self, "prefix_list_id")

    @prefix_list_id.setter
    def prefix_list_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "prefix_list_id", value)

    @property
    @pulumi.getter(name="referencedSecurityGroupId")
    def referenced_security_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The source security group that is referenced in the rule.
        """
        return pulumi.get(self, "referenced_security_group_id")

    @referenced_security_group_id.setter
    def referenced_security_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "referenced_security_group_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="toPort")
    def to_port(self) -> Optional[pulumi.Input[int]]:
        """
        The end of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 code.
        """
        return pulumi.get(self, "to_port")

    @to_port.setter
    def to_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "to_port", value)


@pulumi.input_type
class _SecurityGroupIngressRuleState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 cidr_ipv4: Optional[pulumi.Input[str]] = None,
                 cidr_ipv6: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 from_port: Optional[pulumi.Input[int]] = None,
                 ip_protocol: Optional[pulumi.Input[str]] = None,
                 prefix_list_id: Optional[pulumi.Input[str]] = None,
                 referenced_security_group_id: Optional[pulumi.Input[str]] = None,
                 security_group_id: Optional[pulumi.Input[str]] = None,
                 security_group_rule_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 to_port: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering SecurityGroupIngressRule resources.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the security group rule.
        :param pulumi.Input[str] cidr_ipv4: The source IPv4 CIDR range.
        :param pulumi.Input[str] cidr_ipv6: The source IPv6 CIDR range.
        :param pulumi.Input[str] description: The security group rule description.
        :param pulumi.Input[int] from_port: The start of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 type.
        :param pulumi.Input[str] ip_protocol: The IP protocol name or number. Use `-1` to specify all protocols. Note that if `ip_protocol` is set to `-1`, it translates to all protocols, all port ranges, and `from_port` and `to_port` values should not be defined.
        :param pulumi.Input[str] prefix_list_id: The ID of the source prefix list.
        :param pulumi.Input[str] referenced_security_group_id: The source security group that is referenced in the rule.
        :param pulumi.Input[str] security_group_id: The ID of the security group.
        :param pulumi.Input[str] security_group_rule_id: The ID of the security group rule.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[int] to_port: The end of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 code.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if cidr_ipv4 is not None:
            pulumi.set(__self__, "cidr_ipv4", cidr_ipv4)
        if cidr_ipv6 is not None:
            pulumi.set(__self__, "cidr_ipv6", cidr_ipv6)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if from_port is not None:
            pulumi.set(__self__, "from_port", from_port)
        if ip_protocol is not None:
            pulumi.set(__self__, "ip_protocol", ip_protocol)
        if prefix_list_id is not None:
            pulumi.set(__self__, "prefix_list_id", prefix_list_id)
        if referenced_security_group_id is not None:
            pulumi.set(__self__, "referenced_security_group_id", referenced_security_group_id)
        if security_group_id is not None:
            pulumi.set(__self__, "security_group_id", security_group_id)
        if security_group_rule_id is not None:
            pulumi.set(__self__, "security_group_rule_id", security_group_rule_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if to_port is not None:
            pulumi.set(__self__, "to_port", to_port)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the security group rule.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="cidrIpv4")
    def cidr_ipv4(self) -> Optional[pulumi.Input[str]]:
        """
        The source IPv4 CIDR range.
        """
        return pulumi.get(self, "cidr_ipv4")

    @cidr_ipv4.setter
    def cidr_ipv4(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cidr_ipv4", value)

    @property
    @pulumi.getter(name="cidrIpv6")
    def cidr_ipv6(self) -> Optional[pulumi.Input[str]]:
        """
        The source IPv6 CIDR range.
        """
        return pulumi.get(self, "cidr_ipv6")

    @cidr_ipv6.setter
    def cidr_ipv6(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cidr_ipv6", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The security group rule description.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="fromPort")
    def from_port(self) -> Optional[pulumi.Input[int]]:
        """
        The start of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 type.
        """
        return pulumi.get(self, "from_port")

    @from_port.setter
    def from_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "from_port", value)

    @property
    @pulumi.getter(name="ipProtocol")
    def ip_protocol(self) -> Optional[pulumi.Input[str]]:
        """
        The IP protocol name or number. Use `-1` to specify all protocols. Note that if `ip_protocol` is set to `-1`, it translates to all protocols, all port ranges, and `from_port` and `to_port` values should not be defined.
        """
        return pulumi.get(self, "ip_protocol")

    @ip_protocol.setter
    def ip_protocol(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_protocol", value)

    @property
    @pulumi.getter(name="prefixListId")
    def prefix_list_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the source prefix list.
        """
        return pulumi.get(self, "prefix_list_id")

    @prefix_list_id.setter
    def prefix_list_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "prefix_list_id", value)

    @property
    @pulumi.getter(name="referencedSecurityGroupId")
    def referenced_security_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The source security group that is referenced in the rule.
        """
        return pulumi.get(self, "referenced_security_group_id")

    @referenced_security_group_id.setter
    def referenced_security_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "referenced_security_group_id", value)

    @property
    @pulumi.getter(name="securityGroupId")
    def security_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the security group.
        """
        return pulumi.get(self, "security_group_id")

    @security_group_id.setter
    def security_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "security_group_id", value)

    @property
    @pulumi.getter(name="securityGroupRuleId")
    def security_group_rule_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the security group rule.
        """
        return pulumi.get(self, "security_group_rule_id")

    @security_group_rule_id.setter
    def security_group_rule_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "security_group_rule_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter(name="toPort")
    def to_port(self) -> Optional[pulumi.Input[int]]:
        """
        The end of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 code.
        """
        return pulumi.get(self, "to_port")

    @to_port.setter
    def to_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "to_port", value)


class SecurityGroupIngressRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cidr_ipv4: Optional[pulumi.Input[str]] = None,
                 cidr_ipv6: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 from_port: Optional[pulumi.Input[int]] = None,
                 ip_protocol: Optional[pulumi.Input[str]] = None,
                 prefix_list_id: Optional[pulumi.Input[str]] = None,
                 referenced_security_group_id: Optional[pulumi.Input[str]] = None,
                 security_group_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 to_port: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Manages an inbound (ingress) rule for a security group.

        When specifying an inbound rule for your security group in a VPC, the configuration must include a source for the traffic.

        > **NOTE on Security Groups and Security Group Rules:** this provider currently provides a Security Group resource with `ingress` and `egress` rules defined in-line and a Security Group Rule resource which manages one or more `ingress` or
        `egress` rules. Both of these resource were added before AWS assigned a [security group rule unique ID](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-rules.html), and they do not work well in all scenarios using the`description` and `tags` attributes, which rely on the unique ID.
        The `vpc.SecurityGroupIngressRule` resource has been added to address these limitations and should be used for all new security group rules.
        You should not use the `vpc.SecurityGroupIngressRule` resource in conjunction with an `ec2.SecurityGroup` resource with in-line rules or with `ec2.SecurityGroupRule` resources defined for the same Security Group, as rule conflicts may occur and rules will be overwritten.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ec2.SecurityGroup("example",
            name="example",
            description="example",
            vpc_id=main["id"],
            tags={
                "Name": "example",
            })
        example_security_group_ingress_rule = aws.vpc.SecurityGroupIngressRule("example",
            security_group_id=example.id,
            cidr_ipv4="10.0.0.0/8",
            from_port=80,
            ip_protocol="tcp",
            to_port=80)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import security group ingress rules using the `security_group_rule_id`. For example:

        ```sh
        $ pulumi import aws:vpc/securityGroupIngressRule:SecurityGroupIngressRule example sgr-02108b27edd666983
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cidr_ipv4: The source IPv4 CIDR range.
        :param pulumi.Input[str] cidr_ipv6: The source IPv6 CIDR range.
        :param pulumi.Input[str] description: The security group rule description.
        :param pulumi.Input[int] from_port: The start of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 type.
        :param pulumi.Input[str] ip_protocol: The IP protocol name or number. Use `-1` to specify all protocols. Note that if `ip_protocol` is set to `-1`, it translates to all protocols, all port ranges, and `from_port` and `to_port` values should not be defined.
        :param pulumi.Input[str] prefix_list_id: The ID of the source prefix list.
        :param pulumi.Input[str] referenced_security_group_id: The source security group that is referenced in the rule.
        :param pulumi.Input[str] security_group_id: The ID of the security group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[int] to_port: The end of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 code.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SecurityGroupIngressRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an inbound (ingress) rule for a security group.

        When specifying an inbound rule for your security group in a VPC, the configuration must include a source for the traffic.

        > **NOTE on Security Groups and Security Group Rules:** this provider currently provides a Security Group resource with `ingress` and `egress` rules defined in-line and a Security Group Rule resource which manages one or more `ingress` or
        `egress` rules. Both of these resource were added before AWS assigned a [security group rule unique ID](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-rules.html), and they do not work well in all scenarios using the`description` and `tags` attributes, which rely on the unique ID.
        The `vpc.SecurityGroupIngressRule` resource has been added to address these limitations and should be used for all new security group rules.
        You should not use the `vpc.SecurityGroupIngressRule` resource in conjunction with an `ec2.SecurityGroup` resource with in-line rules or with `ec2.SecurityGroupRule` resources defined for the same Security Group, as rule conflicts may occur and rules will be overwritten.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ec2.SecurityGroup("example",
            name="example",
            description="example",
            vpc_id=main["id"],
            tags={
                "Name": "example",
            })
        example_security_group_ingress_rule = aws.vpc.SecurityGroupIngressRule("example",
            security_group_id=example.id,
            cidr_ipv4="10.0.0.0/8",
            from_port=80,
            ip_protocol="tcp",
            to_port=80)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import security group ingress rules using the `security_group_rule_id`. For example:

        ```sh
        $ pulumi import aws:vpc/securityGroupIngressRule:SecurityGroupIngressRule example sgr-02108b27edd666983
        ```

        :param str resource_name: The name of the resource.
        :param SecurityGroupIngressRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SecurityGroupIngressRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cidr_ipv4: Optional[pulumi.Input[str]] = None,
                 cidr_ipv6: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 from_port: Optional[pulumi.Input[int]] = None,
                 ip_protocol: Optional[pulumi.Input[str]] = None,
                 prefix_list_id: Optional[pulumi.Input[str]] = None,
                 referenced_security_group_id: Optional[pulumi.Input[str]] = None,
                 security_group_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 to_port: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SecurityGroupIngressRuleArgs.__new__(SecurityGroupIngressRuleArgs)

            __props__.__dict__["cidr_ipv4"] = cidr_ipv4
            __props__.__dict__["cidr_ipv6"] = cidr_ipv6
            __props__.__dict__["description"] = description
            __props__.__dict__["from_port"] = from_port
            if ip_protocol is None and not opts.urn:
                raise TypeError("Missing required property 'ip_protocol'")
            __props__.__dict__["ip_protocol"] = ip_protocol
            __props__.__dict__["prefix_list_id"] = prefix_list_id
            __props__.__dict__["referenced_security_group_id"] = referenced_security_group_id
            if security_group_id is None and not opts.urn:
                raise TypeError("Missing required property 'security_group_id'")
            __props__.__dict__["security_group_id"] = security_group_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["to_port"] = to_port
            __props__.__dict__["arn"] = None
            __props__.__dict__["security_group_rule_id"] = None
            __props__.__dict__["tags_all"] = None
        super(SecurityGroupIngressRule, __self__).__init__(
            'aws:vpc/securityGroupIngressRule:SecurityGroupIngressRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            cidr_ipv4: Optional[pulumi.Input[str]] = None,
            cidr_ipv6: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            from_port: Optional[pulumi.Input[int]] = None,
            ip_protocol: Optional[pulumi.Input[str]] = None,
            prefix_list_id: Optional[pulumi.Input[str]] = None,
            referenced_security_group_id: Optional[pulumi.Input[str]] = None,
            security_group_id: Optional[pulumi.Input[str]] = None,
            security_group_rule_id: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            to_port: Optional[pulumi.Input[int]] = None) -> 'SecurityGroupIngressRule':
        """
        Get an existing SecurityGroupIngressRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the security group rule.
        :param pulumi.Input[str] cidr_ipv4: The source IPv4 CIDR range.
        :param pulumi.Input[str] cidr_ipv6: The source IPv6 CIDR range.
        :param pulumi.Input[str] description: The security group rule description.
        :param pulumi.Input[int] from_port: The start of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 type.
        :param pulumi.Input[str] ip_protocol: The IP protocol name or number. Use `-1` to specify all protocols. Note that if `ip_protocol` is set to `-1`, it translates to all protocols, all port ranges, and `from_port` and `to_port` values should not be defined.
        :param pulumi.Input[str] prefix_list_id: The ID of the source prefix list.
        :param pulumi.Input[str] referenced_security_group_id: The source security group that is referenced in the rule.
        :param pulumi.Input[str] security_group_id: The ID of the security group.
        :param pulumi.Input[str] security_group_rule_id: The ID of the security group rule.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[int] to_port: The end of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 code.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SecurityGroupIngressRuleState.__new__(_SecurityGroupIngressRuleState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["cidr_ipv4"] = cidr_ipv4
        __props__.__dict__["cidr_ipv6"] = cidr_ipv6
        __props__.__dict__["description"] = description
        __props__.__dict__["from_port"] = from_port
        __props__.__dict__["ip_protocol"] = ip_protocol
        __props__.__dict__["prefix_list_id"] = prefix_list_id
        __props__.__dict__["referenced_security_group_id"] = referenced_security_group_id
        __props__.__dict__["security_group_id"] = security_group_id
        __props__.__dict__["security_group_rule_id"] = security_group_rule_id
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["to_port"] = to_port
        return SecurityGroupIngressRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the security group rule.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="cidrIpv4")
    def cidr_ipv4(self) -> pulumi.Output[Optional[str]]:
        """
        The source IPv4 CIDR range.
        """
        return pulumi.get(self, "cidr_ipv4")

    @property
    @pulumi.getter(name="cidrIpv6")
    def cidr_ipv6(self) -> pulumi.Output[Optional[str]]:
        """
        The source IPv6 CIDR range.
        """
        return pulumi.get(self, "cidr_ipv6")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The security group rule description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="fromPort")
    def from_port(self) -> pulumi.Output[Optional[int]]:
        """
        The start of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 type.
        """
        return pulumi.get(self, "from_port")

    @property
    @pulumi.getter(name="ipProtocol")
    def ip_protocol(self) -> pulumi.Output[str]:
        """
        The IP protocol name or number. Use `-1` to specify all protocols. Note that if `ip_protocol` is set to `-1`, it translates to all protocols, all port ranges, and `from_port` and `to_port` values should not be defined.
        """
        return pulumi.get(self, "ip_protocol")

    @property
    @pulumi.getter(name="prefixListId")
    def prefix_list_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the source prefix list.
        """
        return pulumi.get(self, "prefix_list_id")

    @property
    @pulumi.getter(name="referencedSecurityGroupId")
    def referenced_security_group_id(self) -> pulumi.Output[Optional[str]]:
        """
        The source security group that is referenced in the rule.
        """
        return pulumi.get(self, "referenced_security_group_id")

    @property
    @pulumi.getter(name="securityGroupId")
    def security_group_id(self) -> pulumi.Output[str]:
        """
        The ID of the security group.
        """
        return pulumi.get(self, "security_group_id")

    @property
    @pulumi.getter(name="securityGroupRuleId")
    def security_group_rule_id(self) -> pulumi.Output[str]:
        """
        The ID of the security group rule.
        """
        return pulumi.get(self, "security_group_rule_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter(name="toPort")
    def to_port(self) -> pulumi.Output[Optional[int]]:
        """
        The end of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 code.
        """
        return pulumi.get(self, "to_port")

