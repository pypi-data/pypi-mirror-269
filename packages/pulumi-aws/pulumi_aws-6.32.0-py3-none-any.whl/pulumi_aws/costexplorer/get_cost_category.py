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

__all__ = [
    'GetCostCategoryResult',
    'AwaitableGetCostCategoryResult',
    'get_cost_category',
    'get_cost_category_output',
]

@pulumi.output_type
class GetCostCategoryResult:
    """
    A collection of values returned by getCostCategory.
    """
    def __init__(__self__, cost_category_arn=None, default_value=None, effective_end=None, effective_start=None, id=None, name=None, rule_version=None, rules=None, split_charge_rules=None, tags=None):
        if cost_category_arn and not isinstance(cost_category_arn, str):
            raise TypeError("Expected argument 'cost_category_arn' to be a str")
        pulumi.set(__self__, "cost_category_arn", cost_category_arn)
        if default_value and not isinstance(default_value, str):
            raise TypeError("Expected argument 'default_value' to be a str")
        pulumi.set(__self__, "default_value", default_value)
        if effective_end and not isinstance(effective_end, str):
            raise TypeError("Expected argument 'effective_end' to be a str")
        pulumi.set(__self__, "effective_end", effective_end)
        if effective_start and not isinstance(effective_start, str):
            raise TypeError("Expected argument 'effective_start' to be a str")
        pulumi.set(__self__, "effective_start", effective_start)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if rule_version and not isinstance(rule_version, str):
            raise TypeError("Expected argument 'rule_version' to be a str")
        pulumi.set(__self__, "rule_version", rule_version)
        if rules and not isinstance(rules, list):
            raise TypeError("Expected argument 'rules' to be a list")
        pulumi.set(__self__, "rules", rules)
        if split_charge_rules and not isinstance(split_charge_rules, list):
            raise TypeError("Expected argument 'split_charge_rules' to be a list")
        pulumi.set(__self__, "split_charge_rules", split_charge_rules)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="costCategoryArn")
    def cost_category_arn(self) -> str:
        return pulumi.get(self, "cost_category_arn")

    @property
    @pulumi.getter(name="defaultValue")
    def default_value(self) -> str:
        """
        Default value for the cost category.
        """
        return pulumi.get(self, "default_value")

    @property
    @pulumi.getter(name="effectiveEnd")
    def effective_end(self) -> str:
        """
        Effective end data of your Cost Category.
        """
        return pulumi.get(self, "effective_end")

    @property
    @pulumi.getter(name="effectiveStart")
    def effective_start(self) -> str:
        """
        Effective state data of your Cost Category.
        """
        return pulumi.get(self, "effective_start")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="ruleVersion")
    def rule_version(self) -> str:
        """
        Rule schema version in this particular Cost Category.
        """
        return pulumi.get(self, "rule_version")

    @property
    @pulumi.getter
    def rules(self) -> Sequence['outputs.GetCostCategoryRuleResult']:
        """
        Configuration block for the `Expression` object used to categorize costs. See below.
        """
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter(name="splitChargeRules")
    def split_charge_rules(self) -> Sequence['outputs.GetCostCategorySplitChargeRuleResult']:
        """
        Configuration block for the split charge rules used to allocate your charges between your Cost Category values. See below.
        """
        return pulumi.get(self, "split_charge_rules")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Configuration block for the specific `Tag` to use for `Expression`. See below.
        """
        return pulumi.get(self, "tags")


class AwaitableGetCostCategoryResult(GetCostCategoryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCostCategoryResult(
            cost_category_arn=self.cost_category_arn,
            default_value=self.default_value,
            effective_end=self.effective_end,
            effective_start=self.effective_start,
            id=self.id,
            name=self.name,
            rule_version=self.rule_version,
            rules=self.rules,
            split_charge_rules=self.split_charge_rules,
            tags=self.tags)


def get_cost_category(cost_category_arn: Optional[str] = None,
                      tags: Optional[Mapping[str, str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCostCategoryResult:
    """
    Provides details about a specific CostExplorer Cost Category.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.costexplorer.get_cost_category(cost_category_arn="costCategoryARN")
    ```
    <!--End PulumiCodeChooser -->


    :param str cost_category_arn: Unique name for the Cost Category.
    :param Mapping[str, str] tags: Configuration block for the specific `Tag` to use for `Expression`. See below.
    """
    __args__ = dict()
    __args__['costCategoryArn'] = cost_category_arn
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:costexplorer/getCostCategory:getCostCategory', __args__, opts=opts, typ=GetCostCategoryResult).value

    return AwaitableGetCostCategoryResult(
        cost_category_arn=pulumi.get(__ret__, 'cost_category_arn'),
        default_value=pulumi.get(__ret__, 'default_value'),
        effective_end=pulumi.get(__ret__, 'effective_end'),
        effective_start=pulumi.get(__ret__, 'effective_start'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        rule_version=pulumi.get(__ret__, 'rule_version'),
        rules=pulumi.get(__ret__, 'rules'),
        split_charge_rules=pulumi.get(__ret__, 'split_charge_rules'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_cost_category)
def get_cost_category_output(cost_category_arn: Optional[pulumi.Input[str]] = None,
                             tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCostCategoryResult]:
    """
    Provides details about a specific CostExplorer Cost Category.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.costexplorer.get_cost_category(cost_category_arn="costCategoryARN")
    ```
    <!--End PulumiCodeChooser -->


    :param str cost_category_arn: Unique name for the Cost Category.
    :param Mapping[str, str] tags: Configuration block for the specific `Tag` to use for `Expression`. See below.
    """
    ...
