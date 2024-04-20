# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AssessmentReportArgs', 'AssessmentReport']

@pulumi.input_type
class AssessmentReportArgs:
    def __init__(__self__, *,
                 assessment_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AssessmentReport resource.
        :param pulumi.Input[str] assessment_id: Unique identifier of the assessment to create the report from.
               
               The following arguments are optional:
        :param pulumi.Input[str] description: Description of the assessment report.
        :param pulumi.Input[str] name: Name of the assessment report.
        """
        pulumi.set(__self__, "assessment_id", assessment_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="assessmentId")
    def assessment_id(self) -> pulumi.Input[str]:
        """
        Unique identifier of the assessment to create the report from.

        The following arguments are optional:
        """
        return pulumi.get(self, "assessment_id")

    @assessment_id.setter
    def assessment_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "assessment_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the assessment report.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the assessment report.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _AssessmentReportState:
    def __init__(__self__, *,
                 assessment_id: Optional[pulumi.Input[str]] = None,
                 author: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AssessmentReport resources.
        :param pulumi.Input[str] assessment_id: Unique identifier of the assessment to create the report from.
               
               The following arguments are optional:
        :param pulumi.Input[str] author: Name of the user who created the assessment report.
        :param pulumi.Input[str] description: Description of the assessment report.
        :param pulumi.Input[str] name: Name of the assessment report.
        :param pulumi.Input[str] status: Current status of the specified assessment report. Valid values are `COMPLETE`, `IN_PROGRESS`, and `FAILED`.
        """
        if assessment_id is not None:
            pulumi.set(__self__, "assessment_id", assessment_id)
        if author is not None:
            pulumi.set(__self__, "author", author)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="assessmentId")
    def assessment_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the assessment to create the report from.

        The following arguments are optional:
        """
        return pulumi.get(self, "assessment_id")

    @assessment_id.setter
    def assessment_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "assessment_id", value)

    @property
    @pulumi.getter
    def author(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the user who created the assessment report.
        """
        return pulumi.get(self, "author")

    @author.setter
    def author(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "author", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the assessment report.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the assessment report.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Current status of the specified assessment report. Valid values are `COMPLETE`, `IN_PROGRESS`, and `FAILED`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class AssessmentReport(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 assessment_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for managing an AWS Audit Manager Assessment Report.

        ## Example Usage

        ### Basic Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.auditmanager.AssessmentReport("test",
            name="example",
            assessment_id=test_aws_auditmanager_assessment["id"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Audit Manager Assessment Reports using the assessment report `id`. For example:

        ```sh
        $ pulumi import aws:auditmanager/assessmentReport:AssessmentReport example abc123-de45
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] assessment_id: Unique identifier of the assessment to create the report from.
               
               The following arguments are optional:
        :param pulumi.Input[str] description: Description of the assessment report.
        :param pulumi.Input[str] name: Name of the assessment report.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AssessmentReportArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS Audit Manager Assessment Report.

        ## Example Usage

        ### Basic Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.auditmanager.AssessmentReport("test",
            name="example",
            assessment_id=test_aws_auditmanager_assessment["id"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Audit Manager Assessment Reports using the assessment report `id`. For example:

        ```sh
        $ pulumi import aws:auditmanager/assessmentReport:AssessmentReport example abc123-de45
        ```

        :param str resource_name: The name of the resource.
        :param AssessmentReportArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AssessmentReportArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 assessment_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AssessmentReportArgs.__new__(AssessmentReportArgs)

            if assessment_id is None and not opts.urn:
                raise TypeError("Missing required property 'assessment_id'")
            __props__.__dict__["assessment_id"] = assessment_id
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            __props__.__dict__["author"] = None
            __props__.__dict__["status"] = None
        super(AssessmentReport, __self__).__init__(
            'aws:auditmanager/assessmentReport:AssessmentReport',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            assessment_id: Optional[pulumi.Input[str]] = None,
            author: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'AssessmentReport':
        """
        Get an existing AssessmentReport resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] assessment_id: Unique identifier of the assessment to create the report from.
               
               The following arguments are optional:
        :param pulumi.Input[str] author: Name of the user who created the assessment report.
        :param pulumi.Input[str] description: Description of the assessment report.
        :param pulumi.Input[str] name: Name of the assessment report.
        :param pulumi.Input[str] status: Current status of the specified assessment report. Valid values are `COMPLETE`, `IN_PROGRESS`, and `FAILED`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AssessmentReportState.__new__(_AssessmentReportState)

        __props__.__dict__["assessment_id"] = assessment_id
        __props__.__dict__["author"] = author
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["status"] = status
        return AssessmentReport(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="assessmentId")
    def assessment_id(self) -> pulumi.Output[str]:
        """
        Unique identifier of the assessment to create the report from.

        The following arguments are optional:
        """
        return pulumi.get(self, "assessment_id")

    @property
    @pulumi.getter
    def author(self) -> pulumi.Output[str]:
        """
        Name of the user who created the assessment report.
        """
        return pulumi.get(self, "author")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the assessment report.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the assessment report.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Current status of the specified assessment report. Valid values are `COMPLETE`, `IN_PROGRESS`, and `FAILED`.
        """
        return pulumi.get(self, "status")

