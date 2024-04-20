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

__all__ = ['AnalyzerArgs', 'Analyzer']

@pulumi.input_type
class AnalyzerArgs:
    def __init__(__self__, *,
                 analyzer_name: pulumi.Input[str],
                 configuration: Optional[pulumi.Input['AnalyzerConfigurationArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Analyzer resource.
        :param pulumi.Input[str] analyzer_name: Name of the Analyzer.
               
               The following arguments are optional:
        :param pulumi.Input['AnalyzerConfigurationArgs'] configuration: A block that specifies the configuration of the analyzer. Documented below
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] type: Type of Analyzer. Valid values are `ACCOUNT`, `ORGANIZATION`, `ACCOUNT_UNUSED_ACCESS `, `ORGANIZATION_UNUSED_ACCESS`. Defaults to `ACCOUNT`.
        """
        pulumi.set(__self__, "analyzer_name", analyzer_name)
        if configuration is not None:
            pulumi.set(__self__, "configuration", configuration)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="analyzerName")
    def analyzer_name(self) -> pulumi.Input[str]:
        """
        Name of the Analyzer.

        The following arguments are optional:
        """
        return pulumi.get(self, "analyzer_name")

    @analyzer_name.setter
    def analyzer_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "analyzer_name", value)

    @property
    @pulumi.getter
    def configuration(self) -> Optional[pulumi.Input['AnalyzerConfigurationArgs']]:
        """
        A block that specifies the configuration of the analyzer. Documented below
        """
        return pulumi.get(self, "configuration")

    @configuration.setter
    def configuration(self, value: Optional[pulumi.Input['AnalyzerConfigurationArgs']]):
        pulumi.set(self, "configuration", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of Analyzer. Valid values are `ACCOUNT`, `ORGANIZATION`, `ACCOUNT_UNUSED_ACCESS `, `ORGANIZATION_UNUSED_ACCESS`. Defaults to `ACCOUNT`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class _AnalyzerState:
    def __init__(__self__, *,
                 analyzer_name: Optional[pulumi.Input[str]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 configuration: Optional[pulumi.Input['AnalyzerConfigurationArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Analyzer resources.
        :param pulumi.Input[str] analyzer_name: Name of the Analyzer.
               
               The following arguments are optional:
        :param pulumi.Input[str] arn: ARN of the Analyzer.
        :param pulumi.Input['AnalyzerConfigurationArgs'] configuration: A block that specifies the configuration of the analyzer. Documented below
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] type: Type of Analyzer. Valid values are `ACCOUNT`, `ORGANIZATION`, `ACCOUNT_UNUSED_ACCESS `, `ORGANIZATION_UNUSED_ACCESS`. Defaults to `ACCOUNT`.
        """
        if analyzer_name is not None:
            pulumi.set(__self__, "analyzer_name", analyzer_name)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if configuration is not None:
            pulumi.set(__self__, "configuration", configuration)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="analyzerName")
    def analyzer_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Analyzer.

        The following arguments are optional:
        """
        return pulumi.get(self, "analyzer_name")

    @analyzer_name.setter
    def analyzer_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "analyzer_name", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the Analyzer.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def configuration(self) -> Optional[pulumi.Input['AnalyzerConfigurationArgs']]:
        """
        A block that specifies the configuration of the analyzer. Documented below
        """
        return pulumi.get(self, "configuration")

    @configuration.setter
    def configuration(self, value: Optional[pulumi.Input['AnalyzerConfigurationArgs']]):
        pulumi.set(self, "configuration", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of Analyzer. Valid values are `ACCOUNT`, `ORGANIZATION`, `ACCOUNT_UNUSED_ACCESS `, `ORGANIZATION_UNUSED_ACCESS`. Defaults to `ACCOUNT`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class Analyzer(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 analyzer_name: Optional[pulumi.Input[str]] = None,
                 configuration: Optional[pulumi.Input[pulumi.InputType['AnalyzerConfigurationArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages an Access Analyzer Analyzer. More information can be found in the [Access Analyzer User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html).

        ## Example Usage

        ### Account Analyzer

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.accessanalyzer.Analyzer("example", analyzer_name="example")
        ```
        <!--End PulumiCodeChooser -->

        ### Organization Analyzer

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.organizations.Organization("example", aws_service_access_principals=["access-analyzer.amazonaws.com"])
        example_analyzer = aws.accessanalyzer.Analyzer("example",
            analyzer_name="example",
            type="ORGANIZATION",
            opts=pulumi.ResourceOptions(depends_on=[example]))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Access Analyzer Analyzers using the `analyzer_name`. For example:

        ```sh
        $ pulumi import aws:accessanalyzer/analyzer:Analyzer example example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] analyzer_name: Name of the Analyzer.
               
               The following arguments are optional:
        :param pulumi.Input[pulumi.InputType['AnalyzerConfigurationArgs']] configuration: A block that specifies the configuration of the analyzer. Documented below
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] type: Type of Analyzer. Valid values are `ACCOUNT`, `ORGANIZATION`, `ACCOUNT_UNUSED_ACCESS `, `ORGANIZATION_UNUSED_ACCESS`. Defaults to `ACCOUNT`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AnalyzerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an Access Analyzer Analyzer. More information can be found in the [Access Analyzer User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html).

        ## Example Usage

        ### Account Analyzer

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.accessanalyzer.Analyzer("example", analyzer_name="example")
        ```
        <!--End PulumiCodeChooser -->

        ### Organization Analyzer

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.organizations.Organization("example", aws_service_access_principals=["access-analyzer.amazonaws.com"])
        example_analyzer = aws.accessanalyzer.Analyzer("example",
            analyzer_name="example",
            type="ORGANIZATION",
            opts=pulumi.ResourceOptions(depends_on=[example]))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Access Analyzer Analyzers using the `analyzer_name`. For example:

        ```sh
        $ pulumi import aws:accessanalyzer/analyzer:Analyzer example example
        ```

        :param str resource_name: The name of the resource.
        :param AnalyzerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AnalyzerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 analyzer_name: Optional[pulumi.Input[str]] = None,
                 configuration: Optional[pulumi.Input[pulumi.InputType['AnalyzerConfigurationArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AnalyzerArgs.__new__(AnalyzerArgs)

            if analyzer_name is None and not opts.urn:
                raise TypeError("Missing required property 'analyzer_name'")
            __props__.__dict__["analyzer_name"] = analyzer_name
            __props__.__dict__["configuration"] = configuration
            __props__.__dict__["tags"] = tags
            __props__.__dict__["type"] = type
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(Analyzer, __self__).__init__(
            'aws:accessanalyzer/analyzer:Analyzer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            analyzer_name: Optional[pulumi.Input[str]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            configuration: Optional[pulumi.Input[pulumi.InputType['AnalyzerConfigurationArgs']]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'Analyzer':
        """
        Get an existing Analyzer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] analyzer_name: Name of the Analyzer.
               
               The following arguments are optional:
        :param pulumi.Input[str] arn: ARN of the Analyzer.
        :param pulumi.Input[pulumi.InputType['AnalyzerConfigurationArgs']] configuration: A block that specifies the configuration of the analyzer. Documented below
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] type: Type of Analyzer. Valid values are `ACCOUNT`, `ORGANIZATION`, `ACCOUNT_UNUSED_ACCESS `, `ORGANIZATION_UNUSED_ACCESS`. Defaults to `ACCOUNT`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AnalyzerState.__new__(_AnalyzerState)

        __props__.__dict__["analyzer_name"] = analyzer_name
        __props__.__dict__["arn"] = arn
        __props__.__dict__["configuration"] = configuration
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["type"] = type
        return Analyzer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="analyzerName")
    def analyzer_name(self) -> pulumi.Output[str]:
        """
        Name of the Analyzer.

        The following arguments are optional:
        """
        return pulumi.get(self, "analyzer_name")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the Analyzer.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def configuration(self) -> pulumi.Output[Optional['outputs.AnalyzerConfiguration']]:
        """
        A block that specifies the configuration of the analyzer. Documented below
        """
        return pulumi.get(self, "configuration")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[Optional[str]]:
        """
        Type of Analyzer. Valid values are `ACCOUNT`, `ORGANIZATION`, `ACCOUNT_UNUSED_ACCESS `, `ORGANIZATION_UNUSED_ACCESS`. Defaults to `ACCOUNT`.
        """
        return pulumi.get(self, "type")

