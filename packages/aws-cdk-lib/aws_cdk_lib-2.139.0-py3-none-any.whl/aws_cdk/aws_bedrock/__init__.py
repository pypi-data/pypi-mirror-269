'''
# Amazon Bedrock Construct Library

Amazon Bedrock is a fully managed service that offers a choice of foundation models (FMs)
along with a broad set of capabilities for building generative AI applications.

CloudFormation does not currently support any Bedrock resource types.
This construct library is a collection of constructs that can look up existing Bedrock models
for use with other services' CDK constructs, such as AWS Step Functions.

To look up a Bedrock base foundation model:

```python
import aws_cdk.aws_bedrock as bedrock


bedrock.FoundationModel.from_foundation_model_id(self, "Model", bedrock.FoundationModelIdentifier.ANTHROPIC_CLAUDE_V2)
```

To look up a Bedrock provisioned throughput model:

```python
import aws_cdk.aws_bedrock as bedrock


bedrock.ProvisionedModel.from_provisioned_model_arn(self, "Model", "arn:aws:bedrock:us-east-2:123456789012:provisioned-model/abc-123")
```
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_9df397a6,
    IInspectable as _IInspectable_c2943556,
    IResolvable as _IResolvable_da3f097b,
    ITaggableV2 as _ITaggableV2_4e6798f8,
    TagManager as _TagManager_0a598cb3,
    TreeInspector as _TreeInspector_488e0dd5,
)


@jsii.implements(_IInspectable_c2943556, _ITaggableV2_4e6798f8)
class CfnAgent(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_bedrock.CfnAgent",
):
    '''Specifies an agent as a resource in a top-level template. Minimally, you must specify the following properties:.

    - AgentName – Specify a name for the agent.
    - AgentResourceRoleArn – Specify the Amazon Resource Name (ARN) of the service role with permissions to invoke API operations on the agent. For more information, see `Create a service role for Agents for Amazon Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-permissions.html>`_ .
    - FoundationModel – Specify the model ID of a foundation model to use when invoking the agent. For more information, see `Supported regions and models for Agents for Amazon Bedrock <https://docs.aws.amazon.com//bedrock/latest/userguide/agents-supported.html>`_ .

    For more information about using agents in Amazon Bedrock , see `Agents for Amazon Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html>`_ .

    See the *Properties* section below for descriptions of both the required and optional properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html
    :cloudformationResource: AWS::Bedrock::Agent
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_bedrock as bedrock
        
        cfn_agent = bedrock.CfnAgent(self, "MyCfnAgent",
            agent_name="agentName",
        
            # the properties below are optional
            action_groups=[bedrock.CfnAgent.AgentActionGroupProperty(
                action_group_name="actionGroupName",
        
                # the properties below are optional
                action_group_executor=bedrock.CfnAgent.ActionGroupExecutorProperty(
                    lambda_="lambda"
                ),
                action_group_state="actionGroupState",
                api_schema=bedrock.CfnAgent.APISchemaProperty(
                    payload="payload",
                    s3=bedrock.CfnAgent.S3IdentifierProperty(
                        s3_bucket_name="s3BucketName",
                        s3_object_key="s3ObjectKey"
                    )
                ),
                description="description",
                parent_action_group_signature="parentActionGroupSignature",
                skip_resource_in_use_check_on_delete=False
            )],
            agent_resource_role_arn="agentResourceRoleArn",
            auto_prepare=False,
            customer_encryption_key_arn="customerEncryptionKeyArn",
            description="description",
            foundation_model="foundationModel",
            idle_session_ttl_in_seconds=123,
            instruction="instruction",
            knowledge_bases=[bedrock.CfnAgent.AgentKnowledgeBaseProperty(
                description="description",
                knowledge_base_id="knowledgeBaseId",
        
                # the properties below are optional
                knowledge_base_state="knowledgeBaseState"
            )],
            prompt_override_configuration=bedrock.CfnAgent.PromptOverrideConfigurationProperty(
                prompt_configurations=[bedrock.CfnAgent.PromptConfigurationProperty(
                    base_prompt_template="basePromptTemplate",
                    inference_configuration=bedrock.CfnAgent.InferenceConfigurationProperty(
                        maximum_length=123,
                        stop_sequences=["stopSequences"],
                        temperature=123,
                        top_k=123,
                        top_p=123
                    ),
                    parser_mode="parserMode",
                    prompt_creation_mode="promptCreationMode",
                    prompt_state="promptState",
                    prompt_type="promptType"
                )],
        
                # the properties below are optional
                override_lambda="overrideLambda"
            ),
            skip_resource_in_use_check_on_delete=False,
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        agent_name: builtins.str,
        action_groups: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union["CfnAgent.AgentActionGroupProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        agent_resource_role_arn: typing.Optional[builtins.str] = None,
        auto_prepare: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        customer_encryption_key_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        foundation_model: typing.Optional[builtins.str] = None,
        idle_session_ttl_in_seconds: typing.Optional[jsii.Number] = None,
        instruction: typing.Optional[builtins.str] = None,
        knowledge_bases: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union["CfnAgent.AgentKnowledgeBaseProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        prompt_override_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union["CfnAgent.PromptOverrideConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        skip_resource_in_use_check_on_delete: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param agent_name: The name of the agent.
        :param action_groups: The action groups that belong to an agent.
        :param agent_resource_role_arn: The Amazon Resource Name (ARN) of the IAM role with permissions to invoke API operations on the agent.
        :param auto_prepare: Specifies whether to automatically update the ``DRAFT`` version of the agent after making changes to the agent. The ``DRAFT`` version can be continually iterated upon during internal development. By default, this value is ``false`` . Default: - false
        :param customer_encryption_key_arn: The Amazon Resource Name (ARN) of the AWS KMS key that encrypts the agent.
        :param description: The description of the agent.
        :param foundation_model: The foundation model used for orchestration by the agent.
        :param idle_session_ttl_in_seconds: The number of seconds for which Amazon Bedrock keeps information about a user's conversation with the agent. A user interaction remains active for the amount of time specified. If no conversation occurs during this time, the session expires and Amazon Bedrock deletes any data provided before the timeout.
        :param instruction: Instructions that tell the agent what it should do and how it should interact with users.
        :param knowledge_bases: The knowledge bases associated with the agent.
        :param prompt_override_configuration: Contains configurations to override prompt templates in different parts of an agent sequence. For more information, see `Advanced prompts <https://docs.aws.amazon.com/bedrock/latest/userguide/advanced-prompts.html>`_ .
        :param skip_resource_in_use_check_on_delete: Specifies whether to delete the resource even if it's in use. By default, this value is ``false`` . Default: - false
        :param tags: Metadata that you can assign to a resource as key-value pairs. For more information, see the following resources:. - `Tag naming limits and requirements <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-conventions>`_ - `Tagging best practices <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-best-practices>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__facaad57ffe16da42f099d2b7997f3e6fd3b9eba46fd226d8fb5afe286371e74)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAgentProps(
            agent_name=agent_name,
            action_groups=action_groups,
            agent_resource_role_arn=agent_resource_role_arn,
            auto_prepare=auto_prepare,
            customer_encryption_key_arn=customer_encryption_key_arn,
            description=description,
            foundation_model=foundation_model,
            idle_session_ttl_in_seconds=idle_session_ttl_in_seconds,
            instruction=instruction,
            knowledge_bases=knowledge_bases,
            prompt_override_configuration=prompt_override_configuration,
            skip_resource_in_use_check_on_delete=skip_resource_in_use_check_on_delete,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c671dddc0216853bf62cdd51e6c2889b8dfe0d7819a455df2ad71c5b8d67daba)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0633cd876f44b7c72e1346d6b26f361a0d1afbb01604add4ba48210303ccc35c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAgentArn")
    def attr_agent_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the agent.

        :cloudformationAttribute: AgentArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAgentArn"))

    @builtins.property
    @jsii.member(jsii_name="attrAgentId")
    def attr_agent_id(self) -> builtins.str:
        '''The unique identifier of the agent.

        :cloudformationAttribute: AgentId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAgentId"))

    @builtins.property
    @jsii.member(jsii_name="attrAgentStatus")
    def attr_agent_status(self) -> builtins.str:
        '''The status of the agent and whether it is ready for use. The following statuses are possible:.

        - CREATING – The agent is being created.
        - PREPARING – The agent is being prepared.
        - PREPARED – The agent is prepared and ready to be invoked.
        - NOT_PREPARED – The agent has been created but not yet prepared.
        - FAILED – The agent API operation failed.
        - UPDATING – The agent is being updated.
        - DELETING – The agent is being deleted.

        :cloudformationAttribute: AgentStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAgentStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrAgentVersion")
    def attr_agent_version(self) -> builtins.str:
        '''The version of the agent.

        :cloudformationAttribute: AgentVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAgentVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The time at which the agent was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrFailureReasons")
    def attr_failure_reasons(self) -> typing.List[builtins.str]:
        '''Contains reasons that the agent-related API that you invoked failed.

        :cloudformationAttribute: FailureReasons
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrFailureReasons"))

    @builtins.property
    @jsii.member(jsii_name="attrPreparedAt")
    def attr_prepared_at(self) -> builtins.str:
        '''The time at which the agent was last prepared.

        :cloudformationAttribute: PreparedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPreparedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrRecommendedActions")
    def attr_recommended_actions(self) -> typing.List[builtins.str]:
        '''Contains recommended actions to take for the agent-related API that you invoked to succeed.

        :cloudformationAttribute: RecommendedActions
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrRecommendedActions"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The time at which the agent was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> _TagManager_0a598cb3:
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="agentName")
    def agent_name(self) -> builtins.str:
        '''The name of the agent.'''
        return typing.cast(builtins.str, jsii.get(self, "agentName"))

    @agent_name.setter
    def agent_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c19306b2dfaafb18e03ff6cb134d14ba6e0563e4a2c79c53886ba8207714cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentName", value)

    @builtins.property
    @jsii.member(jsii_name="actionGroups")
    def action_groups(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, "CfnAgent.AgentActionGroupProperty"]]]]:
        '''The action groups that belong to an agent.'''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, "CfnAgent.AgentActionGroupProperty"]]]], jsii.get(self, "actionGroups"))

    @action_groups.setter
    def action_groups(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, "CfnAgent.AgentActionGroupProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f670733e4a574d57292a648f4a8ad68ef64492d8f6667729aee160997a190e16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionGroups", value)

    @builtins.property
    @jsii.member(jsii_name="agentResourceRoleArn")
    def agent_resource_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role with permissions to invoke API operations on the agent.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentResourceRoleArn"))

    @agent_resource_role_arn.setter
    def agent_resource_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b021046f759c8bbfbfb02bceb7d337926c83d3e866d3dcd420bb7819e254ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentResourceRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="autoPrepare")
    def auto_prepare(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''Specifies whether to automatically update the ``DRAFT`` version of the agent after making changes to the agent.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], jsii.get(self, "autoPrepare"))

    @auto_prepare.setter
    def auto_prepare(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc98d7cbd7435359b362ef11a9b384386d54f878814d4c596d3dfa290281e67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoPrepare", value)

    @builtins.property
    @jsii.member(jsii_name="customerEncryptionKeyArn")
    def customer_encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS KMS key that encrypts the agent.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerEncryptionKeyArn"))

    @customer_encryption_key_arn.setter
    def customer_encryption_key_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea763219d3fed10a3841f0a137399ddf8f575abf9b1691273415e66f4f0763c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerEncryptionKeyArn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the agent.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd6874957339badfe5e02e7733947f3ba0b1fdc8c597003bfe10fc7ff96c537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="foundationModel")
    def foundation_model(self) -> typing.Optional[builtins.str]:
        '''The foundation model used for orchestration by the agent.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "foundationModel"))

    @foundation_model.setter
    def foundation_model(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75110aa6cf6cc2a463a78a36e9a6327c59875b1ef94d53da3047b8ec62c79fd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "foundationModel", value)

    @builtins.property
    @jsii.member(jsii_name="idleSessionTtlInSeconds")
    def idle_session_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds for which Amazon Bedrock keeps information about a user's conversation with the agent.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "idleSessionTtlInSeconds"))

    @idle_session_ttl_in_seconds.setter
    def idle_session_ttl_in_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e29f42af6a8bf7aee6adb6b35e7809da69175082446368854bd402491896a71f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleSessionTtlInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="instruction")
    def instruction(self) -> typing.Optional[builtins.str]:
        '''Instructions that tell the agent what it should do and how it should interact with users.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instruction"))

    @instruction.setter
    def instruction(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51c531a159f9cc0e23a07b5bc12cf53006e4207dd460e3ce580c57fa76109e86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instruction", value)

    @builtins.property
    @jsii.member(jsii_name="knowledgeBases")
    def knowledge_bases(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, "CfnAgent.AgentKnowledgeBaseProperty"]]]]:
        '''The knowledge bases associated with the agent.'''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, "CfnAgent.AgentKnowledgeBaseProperty"]]]], jsii.get(self, "knowledgeBases"))

    @knowledge_bases.setter
    def knowledge_bases(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, "CfnAgent.AgentKnowledgeBaseProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8842d93181ada69f14f22e8ff6855e528b858dd0baf705a1ae228b3d96ef38d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "knowledgeBases", value)

    @builtins.property
    @jsii.member(jsii_name="promptOverrideConfiguration")
    def prompt_override_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnAgent.PromptOverrideConfigurationProperty"]]:
        '''Contains configurations to override prompt templates in different parts of an agent sequence.'''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnAgent.PromptOverrideConfigurationProperty"]], jsii.get(self, "promptOverrideConfiguration"))

    @prompt_override_configuration.setter
    def prompt_override_configuration(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnAgent.PromptOverrideConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d115c78c31e0cc4b4828b953c3afd44f4b9271c4e3aaad46777846216d6e9b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "promptOverrideConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="skipResourceInUseCheckOnDelete")
    def skip_resource_in_use_check_on_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''Specifies whether to delete the resource even if it's in use.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], jsii.get(self, "skipResourceInUseCheckOnDelete"))

    @skip_resource_in_use_check_on_delete.setter
    def skip_resource_in_use_check_on_delete(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f4401bf1c7d6b30870233c265d99a973b05e80ad9e53ab7945a82208a3bf49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipResourceInUseCheckOnDelete", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata that you can assign to a resource as key-value pairs.

        For more information, see the following resources:.
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9e79489cae3525b40539f62fddb8a1f8b194bc0b1d166146c12f85a52d978be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnAgent.APISchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"payload": "payload", "s3": "s3"},
    )
    class APISchemaProperty:
        def __init__(
            self,
            *,
            payload: typing.Optional[builtins.str] = None,
            s3: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union["CfnAgent.S3IdentifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains details about the OpenAPI schema for the action group.

            For more information, see `Action group OpenAPI schemas <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html>`_ . You can either include the schema directly in the ``payload`` field or you can upload it to an S3 bucket and specify the S3 bucket location in the ``s3`` field.

            :param payload: The JSON or YAML-formatted payload defining the OpenAPI schema for the action group. For more information, see `Action group OpenAPI schemas <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html>`_ .
            :param s3: Contains details about the S3 object containing the OpenAPI schema for the action group. For more information, see `Action group OpenAPI schemas <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-apischema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                a_pISchema_property = bedrock.CfnAgent.APISchemaProperty(
                    payload="payload",
                    s3=bedrock.CfnAgent.S3IdentifierProperty(
                        s3_bucket_name="s3BucketName",
                        s3_object_key="s3ObjectKey"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__537a89983eef4dfdf436d52865dbd27f462f778f0de6c8ec6162918153faf331)
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if payload is not None:
                self._values["payload"] = payload
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def payload(self) -> typing.Optional[builtins.str]:
            '''The JSON or YAML-formatted payload defining the OpenAPI schema for the action group.

            For more information, see `Action group OpenAPI schemas <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-apischema.html#cfn-bedrock-agent-apischema-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnAgent.S3IdentifierProperty"]]:
            '''Contains details about the S3 object containing the OpenAPI schema for the action group.

            For more information, see `Action group OpenAPI schemas <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-apischema.html#cfn-bedrock-agent-apischema-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnAgent.S3IdentifierProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "APISchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnAgent.ActionGroupExecutorProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_": "lambda"},
    )
    class ActionGroupExecutorProperty:
        def __init__(self, *, lambda_: builtins.str) -> None:
            '''Contains details about the Lambda function containing the business logic that is carried out upon invoking the action.

            :param lambda_: The Amazon Resource Name (ARN) of the Lambda function containing the business logic that is carried out upon invoking the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-actiongroupexecutor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                action_group_executor_property = bedrock.CfnAgent.ActionGroupExecutorProperty(
                    lambda_="lambda"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27e0c43d5a1e3dda92d710404aea51beb5f30a149322d9ec3e8d354b889735eb)
                check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "lambda_": lambda_,
            }

        @builtins.property
        def lambda_(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the Lambda function containing the business logic that is carried out upon invoking the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-actiongroupexecutor.html#cfn-bedrock-agent-actiongroupexecutor-lambda
            '''
            result = self._values.get("lambda_")
            assert result is not None, "Required property 'lambda_' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionGroupExecutorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnAgent.AgentActionGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_group_name": "actionGroupName",
            "action_group_executor": "actionGroupExecutor",
            "action_group_state": "actionGroupState",
            "api_schema": "apiSchema",
            "description": "description",
            "parent_action_group_signature": "parentActionGroupSignature",
            "skip_resource_in_use_check_on_delete": "skipResourceInUseCheckOnDelete",
        },
    )
    class AgentActionGroupProperty:
        def __init__(
            self,
            *,
            action_group_name: builtins.str,
            action_group_executor: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union["CfnAgent.ActionGroupExecutorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            action_group_state: typing.Optional[builtins.str] = None,
            api_schema: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union["CfnAgent.APISchemaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            description: typing.Optional[builtins.str] = None,
            parent_action_group_signature: typing.Optional[builtins.str] = None,
            skip_resource_in_use_check_on_delete: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Contains details about an action group.

            :param action_group_name: The name of the action group.
            :param action_group_executor: The Amazon Resource Name (ARN) of the Lambda function containing the business logic that is carried out upon invoking the action.
            :param action_group_state: Specifies whether the action group is available for the agent to invoke or not when sending an `InvokeAgent <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html>`_ request.
            :param api_schema: Contains either details about the S3 object containing the OpenAPI schema for the action group or the JSON or YAML-formatted payload defining the schema. For more information, see `Action group OpenAPI schemas <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html>`_ .
            :param description: The description of the action group.
            :param parent_action_group_signature: If this field is set as ``AMAZON.UserInput`` , the agent can request the user for additional information when trying to complete a task. The ``description`` , ``apiSchema`` , and ``actionGroupExecutor`` fields must be blank for this action group. During orchestration, if the agent determines that it needs to invoke an API in an action group, but doesn't have enough information to complete the API request, it will invoke this action group instead and return an `Observation <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Observation.html>`_ reprompting the user for more information.
            :param skip_resource_in_use_check_on_delete: Specifies whether to delete the resource even if it's in use. By default, this value is ``false`` . Default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-agentactiongroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                agent_action_group_property = bedrock.CfnAgent.AgentActionGroupProperty(
                    action_group_name="actionGroupName",
                
                    # the properties below are optional
                    action_group_executor=bedrock.CfnAgent.ActionGroupExecutorProperty(
                        lambda_="lambda"
                    ),
                    action_group_state="actionGroupState",
                    api_schema=bedrock.CfnAgent.APISchemaProperty(
                        payload="payload",
                        s3=bedrock.CfnAgent.S3IdentifierProperty(
                            s3_bucket_name="s3BucketName",
                            s3_object_key="s3ObjectKey"
                        )
                    ),
                    description="description",
                    parent_action_group_signature="parentActionGroupSignature",
                    skip_resource_in_use_check_on_delete=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__adb9c2568194cbbe9c081f2a8339eaee9966d82b8c5c5ffbc732275ef4a1b76a)
                check_type(argname="argument action_group_name", value=action_group_name, expected_type=type_hints["action_group_name"])
                check_type(argname="argument action_group_executor", value=action_group_executor, expected_type=type_hints["action_group_executor"])
                check_type(argname="argument action_group_state", value=action_group_state, expected_type=type_hints["action_group_state"])
                check_type(argname="argument api_schema", value=api_schema, expected_type=type_hints["api_schema"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument parent_action_group_signature", value=parent_action_group_signature, expected_type=type_hints["parent_action_group_signature"])
                check_type(argname="argument skip_resource_in_use_check_on_delete", value=skip_resource_in_use_check_on_delete, expected_type=type_hints["skip_resource_in_use_check_on_delete"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action_group_name": action_group_name,
            }
            if action_group_executor is not None:
                self._values["action_group_executor"] = action_group_executor
            if action_group_state is not None:
                self._values["action_group_state"] = action_group_state
            if api_schema is not None:
                self._values["api_schema"] = api_schema
            if description is not None:
                self._values["description"] = description
            if parent_action_group_signature is not None:
                self._values["parent_action_group_signature"] = parent_action_group_signature
            if skip_resource_in_use_check_on_delete is not None:
                self._values["skip_resource_in_use_check_on_delete"] = skip_resource_in_use_check_on_delete

        @builtins.property
        def action_group_name(self) -> builtins.str:
            '''The name of the action group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-agentactiongroup.html#cfn-bedrock-agent-agentactiongroup-actiongroupname
            '''
            result = self._values.get("action_group_name")
            assert result is not None, "Required property 'action_group_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def action_group_executor(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnAgent.ActionGroupExecutorProperty"]]:
            '''The Amazon Resource Name (ARN) of the Lambda function containing the business logic that is carried out upon invoking the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-agentactiongroup.html#cfn-bedrock-agent-agentactiongroup-actiongroupexecutor
            '''
            result = self._values.get("action_group_executor")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnAgent.ActionGroupExecutorProperty"]], result)

        @builtins.property
        def action_group_state(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the action group is available for the agent to invoke or not when sending an `InvokeAgent <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html>`_ request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-agentactiongroup.html#cfn-bedrock-agent-agentactiongroup-actiongroupstate
            '''
            result = self._values.get("action_group_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def api_schema(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnAgent.APISchemaProperty"]]:
            '''Contains either details about the S3 object containing the OpenAPI schema for the action group or the JSON or YAML-formatted payload defining the schema.

            For more information, see `Action group OpenAPI schemas <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-agentactiongroup.html#cfn-bedrock-agent-agentactiongroup-apischema
            '''
            result = self._values.get("api_schema")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnAgent.APISchemaProperty"]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the action group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-agentactiongroup.html#cfn-bedrock-agent-agentactiongroup-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parent_action_group_signature(self) -> typing.Optional[builtins.str]:
            '''If this field is set as ``AMAZON.UserInput`` , the agent can request the user for additional information when trying to complete a task. The ``description`` , ``apiSchema`` , and ``actionGroupExecutor`` fields must be blank for this action group.

            During orchestration, if the agent determines that it needs to invoke an API in an action group, but doesn't have enough information to complete the API request, it will invoke this action group instead and return an `Observation <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_Observation.html>`_ reprompting the user for more information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-agentactiongroup.html#cfn-bedrock-agent-agentactiongroup-parentactiongroupsignature
            '''
            result = self._values.get("parent_action_group_signature")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def skip_resource_in_use_check_on_delete(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''Specifies whether to delete the resource even if it's in use.

            By default, this value is ``false`` .

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-agentactiongroup.html#cfn-bedrock-agent-agentactiongroup-skipresourceinusecheckondelete
            '''
            result = self._values.get("skip_resource_in_use_check_on_delete")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AgentActionGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnAgent.AgentKnowledgeBaseProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "knowledge_base_id": "knowledgeBaseId",
            "knowledge_base_state": "knowledgeBaseState",
        },
    )
    class AgentKnowledgeBaseProperty:
        def __init__(
            self,
            *,
            description: builtins.str,
            knowledge_base_id: builtins.str,
            knowledge_base_state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains details about a knowledge base that is associated with an agent.

            :param description: The description of the association between the agent and the knowledge base.
            :param knowledge_base_id: The unique identifier of the association between the agent and the knowledge base.
            :param knowledge_base_state: Specifies whether to use the knowledge base or not when sending an `InvokeAgent <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html>`_ request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-agentknowledgebase.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                agent_knowledge_base_property = bedrock.CfnAgent.AgentKnowledgeBaseProperty(
                    description="description",
                    knowledge_base_id="knowledgeBaseId",
                
                    # the properties below are optional
                    knowledge_base_state="knowledgeBaseState"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__45f582a007ade3e95453c6c5cd09673a7089ab2673014cc97bc0c1eee1d85391)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument knowledge_base_id", value=knowledge_base_id, expected_type=type_hints["knowledge_base_id"])
                check_type(argname="argument knowledge_base_state", value=knowledge_base_state, expected_type=type_hints["knowledge_base_state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "description": description,
                "knowledge_base_id": knowledge_base_id,
            }
            if knowledge_base_state is not None:
                self._values["knowledge_base_state"] = knowledge_base_state

        @builtins.property
        def description(self) -> builtins.str:
            '''The description of the association between the agent and the knowledge base.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-agentknowledgebase.html#cfn-bedrock-agent-agentknowledgebase-description
            '''
            result = self._values.get("description")
            assert result is not None, "Required property 'description' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def knowledge_base_id(self) -> builtins.str:
            '''The unique identifier of the association between the agent and the knowledge base.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-agentknowledgebase.html#cfn-bedrock-agent-agentknowledgebase-knowledgebaseid
            '''
            result = self._values.get("knowledge_base_id")
            assert result is not None, "Required property 'knowledge_base_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def knowledge_base_state(self) -> typing.Optional[builtins.str]:
            '''Specifies whether to use the knowledge base or not when sending an `InvokeAgent <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html>`_ request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-agentknowledgebase.html#cfn-bedrock-agent-agentknowledgebase-knowledgebasestate
            '''
            result = self._values.get("knowledge_base_state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AgentKnowledgeBaseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnAgent.InferenceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maximum_length": "maximumLength",
            "stop_sequences": "stopSequences",
            "temperature": "temperature",
            "top_k": "topK",
            "top_p": "topP",
        },
    )
    class InferenceConfigurationProperty:
        def __init__(
            self,
            *,
            maximum_length: typing.Optional[jsii.Number] = None,
            stop_sequences: typing.Optional[typing.Sequence[builtins.str]] = None,
            temperature: typing.Optional[jsii.Number] = None,
            top_k: typing.Optional[jsii.Number] = None,
            top_p: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains inference parameters to use when the agent invokes a foundation model in the part of the agent sequence defined by the ``promptType`` .

            For more information, see `Inference parameters for foundation models <https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html>`_ .

            :param maximum_length: The maximum number of tokens to allow in the generated response.
            :param stop_sequences: A list of stop sequences. A stop sequence is a sequence of characters that causes the model to stop generating the response.
            :param temperature: The likelihood of the model selecting higher-probability options while generating a response. A lower value makes the model more likely to choose higher-probability options, while a higher value makes the model more likely to choose lower-probability options.
            :param top_k: While generating a response, the model determines the probability of the following token at each point of generation. The value that you set for ``topK`` is the number of most-likely candidates from which the model chooses the next token in the sequence. For example, if you set ``topK`` to 50, the model selects the next token from among the top 50 most likely choices.
            :param top_p: While generating a response, the model determines the probability of the following token at each point of generation. The value that you set for ``Top P`` determines the number of most-likely candidates from which the model chooses the next token in the sequence. For example, if you set ``topP`` to 80, the model only selects the next token from the top 80% of the probability distribution of next tokens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-inferenceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                inference_configuration_property = bedrock.CfnAgent.InferenceConfigurationProperty(
                    maximum_length=123,
                    stop_sequences=["stopSequences"],
                    temperature=123,
                    top_k=123,
                    top_p=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b8b0e306d1a46c4fdcedd77b9e6caf3ca221fe8133fe3ce29c1e5e779cc3189)
                check_type(argname="argument maximum_length", value=maximum_length, expected_type=type_hints["maximum_length"])
                check_type(argname="argument stop_sequences", value=stop_sequences, expected_type=type_hints["stop_sequences"])
                check_type(argname="argument temperature", value=temperature, expected_type=type_hints["temperature"])
                check_type(argname="argument top_k", value=top_k, expected_type=type_hints["top_k"])
                check_type(argname="argument top_p", value=top_p, expected_type=type_hints["top_p"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maximum_length is not None:
                self._values["maximum_length"] = maximum_length
            if stop_sequences is not None:
                self._values["stop_sequences"] = stop_sequences
            if temperature is not None:
                self._values["temperature"] = temperature
            if top_k is not None:
                self._values["top_k"] = top_k
            if top_p is not None:
                self._values["top_p"] = top_p

        @builtins.property
        def maximum_length(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of tokens to allow in the generated response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-inferenceconfiguration.html#cfn-bedrock-agent-inferenceconfiguration-maximumlength
            '''
            result = self._values.get("maximum_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stop_sequences(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of stop sequences.

            A stop sequence is a sequence of characters that causes the model to stop generating the response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-inferenceconfiguration.html#cfn-bedrock-agent-inferenceconfiguration-stopsequences
            '''
            result = self._values.get("stop_sequences")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def temperature(self) -> typing.Optional[jsii.Number]:
            '''The likelihood of the model selecting higher-probability options while generating a response.

            A lower value makes the model more likely to choose higher-probability options, while a higher value makes the model more likely to choose lower-probability options.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-inferenceconfiguration.html#cfn-bedrock-agent-inferenceconfiguration-temperature
            '''
            result = self._values.get("temperature")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def top_k(self) -> typing.Optional[jsii.Number]:
            '''While generating a response, the model determines the probability of the following token at each point of generation.

            The value that you set for ``topK`` is the number of most-likely candidates from which the model chooses the next token in the sequence. For example, if you set ``topK`` to 50, the model selects the next token from among the top 50 most likely choices.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-inferenceconfiguration.html#cfn-bedrock-agent-inferenceconfiguration-topk
            '''
            result = self._values.get("top_k")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def top_p(self) -> typing.Optional[jsii.Number]:
            '''While generating a response, the model determines the probability of the following token at each point of generation.

            The value that you set for ``Top P`` determines the number of most-likely candidates from which the model chooses the next token in the sequence. For example, if you set ``topP`` to 80, the model only selects the next token from the top 80% of the probability distribution of next tokens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-inferenceconfiguration.html#cfn-bedrock-agent-inferenceconfiguration-topp
            '''
            result = self._values.get("top_p")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InferenceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnAgent.PromptConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "base_prompt_template": "basePromptTemplate",
            "inference_configuration": "inferenceConfiguration",
            "parser_mode": "parserMode",
            "prompt_creation_mode": "promptCreationMode",
            "prompt_state": "promptState",
            "prompt_type": "promptType",
        },
    )
    class PromptConfigurationProperty:
        def __init__(
            self,
            *,
            base_prompt_template: typing.Optional[builtins.str] = None,
            inference_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union["CfnAgent.InferenceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parser_mode: typing.Optional[builtins.str] = None,
            prompt_creation_mode: typing.Optional[builtins.str] = None,
            prompt_state: typing.Optional[builtins.str] = None,
            prompt_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains configurations to override a prompt template in one part of an agent sequence.

            For more information, see `Advanced prompts <https://docs.aws.amazon.com/bedrock/latest/userguide/advanced-prompts.html>`_ .

            :param base_prompt_template: Defines the prompt template with which to replace the default prompt template. You can use placeholder variables in the base prompt template to customize the prompt. For more information, see `Prompt template placeholder variables <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-placeholders.html>`_ .
            :param inference_configuration: Contains inference parameters to use when the agent invokes a foundation model in the part of the agent sequence defined by the ``promptType`` . For more information, see `Inference parameters for foundation models <https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html>`_ .
            :param parser_mode: Specifies whether to override the default parser Lambda function when parsing the raw foundation model output in the part of the agent sequence defined by the ``promptType`` . If you set the field as ``OVERRIDEN`` , the ``overrideLambda`` field in the `PromptOverrideConfiguration <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PromptOverrideConfiguration.html>`_ must be specified with the ARN of a Lambda function.
            :param prompt_creation_mode: Specifies whether to override the default prompt template for this ``promptType`` . Set this value to ``OVERRIDDEN`` to use the prompt that you provide in the ``basePromptTemplate`` . If you leave it as ``DEFAULT`` , the agent uses a default prompt template.
            :param prompt_state: Specifies whether to allow the agent to carry out the step specified in the ``promptType`` . If you set this value to ``DISABLED`` , the agent skips that step. The default state for each ``promptType`` is as follows. - ``PRE_PROCESSING`` – ``ENABLED`` - ``ORCHESTRATION`` – ``ENABLED`` - ``KNOWLEDGE_BASE_RESPONSE_GENERATION`` – ``ENABLED`` - ``POST_PROCESSING`` – ``DISABLED``
            :param prompt_type: The step in the agent sequence that this prompt configuration applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-promptconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                prompt_configuration_property = bedrock.CfnAgent.PromptConfigurationProperty(
                    base_prompt_template="basePromptTemplate",
                    inference_configuration=bedrock.CfnAgent.InferenceConfigurationProperty(
                        maximum_length=123,
                        stop_sequences=["stopSequences"],
                        temperature=123,
                        top_k=123,
                        top_p=123
                    ),
                    parser_mode="parserMode",
                    prompt_creation_mode="promptCreationMode",
                    prompt_state="promptState",
                    prompt_type="promptType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__072678823f2b5bb708860fe2f54d37c6a24153ba05ec6c798f1cbb1222e7cd7b)
                check_type(argname="argument base_prompt_template", value=base_prompt_template, expected_type=type_hints["base_prompt_template"])
                check_type(argname="argument inference_configuration", value=inference_configuration, expected_type=type_hints["inference_configuration"])
                check_type(argname="argument parser_mode", value=parser_mode, expected_type=type_hints["parser_mode"])
                check_type(argname="argument prompt_creation_mode", value=prompt_creation_mode, expected_type=type_hints["prompt_creation_mode"])
                check_type(argname="argument prompt_state", value=prompt_state, expected_type=type_hints["prompt_state"])
                check_type(argname="argument prompt_type", value=prompt_type, expected_type=type_hints["prompt_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if base_prompt_template is not None:
                self._values["base_prompt_template"] = base_prompt_template
            if inference_configuration is not None:
                self._values["inference_configuration"] = inference_configuration
            if parser_mode is not None:
                self._values["parser_mode"] = parser_mode
            if prompt_creation_mode is not None:
                self._values["prompt_creation_mode"] = prompt_creation_mode
            if prompt_state is not None:
                self._values["prompt_state"] = prompt_state
            if prompt_type is not None:
                self._values["prompt_type"] = prompt_type

        @builtins.property
        def base_prompt_template(self) -> typing.Optional[builtins.str]:
            '''Defines the prompt template with which to replace the default prompt template.

            You can use placeholder variables in the base prompt template to customize the prompt. For more information, see `Prompt template placeholder variables <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-placeholders.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-promptconfiguration.html#cfn-bedrock-agent-promptconfiguration-baseprompttemplate
            '''
            result = self._values.get("base_prompt_template")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inference_configuration(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnAgent.InferenceConfigurationProperty"]]:
            '''Contains inference parameters to use when the agent invokes a foundation model in the part of the agent sequence defined by the ``promptType`` .

            For more information, see `Inference parameters for foundation models <https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-promptconfiguration.html#cfn-bedrock-agent-promptconfiguration-inferenceconfiguration
            '''
            result = self._values.get("inference_configuration")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnAgent.InferenceConfigurationProperty"]], result)

        @builtins.property
        def parser_mode(self) -> typing.Optional[builtins.str]:
            '''Specifies whether to override the default parser Lambda function when parsing the raw foundation model output in the part of the agent sequence defined by the ``promptType`` .

            If you set the field as ``OVERRIDEN`` , the ``overrideLambda`` field in the `PromptOverrideConfiguration <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_PromptOverrideConfiguration.html>`_ must be specified with the ARN of a Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-promptconfiguration.html#cfn-bedrock-agent-promptconfiguration-parsermode
            '''
            result = self._values.get("parser_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prompt_creation_mode(self) -> typing.Optional[builtins.str]:
            '''Specifies whether to override the default prompt template for this ``promptType`` .

            Set this value to ``OVERRIDDEN`` to use the prompt that you provide in the ``basePromptTemplate`` . If you leave it as ``DEFAULT`` , the agent uses a default prompt template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-promptconfiguration.html#cfn-bedrock-agent-promptconfiguration-promptcreationmode
            '''
            result = self._values.get("prompt_creation_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prompt_state(self) -> typing.Optional[builtins.str]:
            '''Specifies whether to allow the agent to carry out the step specified in the ``promptType`` .

            If you set this value to ``DISABLED`` , the agent skips that step. The default state for each ``promptType`` is as follows.

            - ``PRE_PROCESSING`` – ``ENABLED``
            - ``ORCHESTRATION`` – ``ENABLED``
            - ``KNOWLEDGE_BASE_RESPONSE_GENERATION`` – ``ENABLED``
            - ``POST_PROCESSING`` – ``DISABLED``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-promptconfiguration.html#cfn-bedrock-agent-promptconfiguration-promptstate
            '''
            result = self._values.get("prompt_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prompt_type(self) -> typing.Optional[builtins.str]:
            '''The step in the agent sequence that this prompt configuration applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-promptconfiguration.html#cfn-bedrock-agent-promptconfiguration-prompttype
            '''
            result = self._values.get("prompt_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PromptConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnAgent.PromptOverrideConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "prompt_configurations": "promptConfigurations",
            "override_lambda": "overrideLambda",
        },
    )
    class PromptOverrideConfigurationProperty:
        def __init__(
            self,
            *,
            prompt_configurations: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union["CfnAgent.PromptConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]],
            override_lambda: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains configurations to override prompts in different parts of an agent sequence.

            For more information, see `Advanced prompts <https://docs.aws.amazon.com/bedrock/latest/userguide/advanced-prompts.html>`_ .

            :param prompt_configurations: Contains configurations to override a prompt template in one part of an agent sequence. For more information, see `Advanced prompts <https://docs.aws.amazon.com/bedrock/latest/userguide/advanced-prompts.html>`_ .
            :param override_lambda: The ARN of the Lambda function to use when parsing the raw foundation model output in parts of the agent sequence. If you specify this field, at least one of the ``promptConfigurations`` must contain a ``parserMode`` value that is set to ``OVERRIDDEN`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-promptoverrideconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                prompt_override_configuration_property = bedrock.CfnAgent.PromptOverrideConfigurationProperty(
                    prompt_configurations=[bedrock.CfnAgent.PromptConfigurationProperty(
                        base_prompt_template="basePromptTemplate",
                        inference_configuration=bedrock.CfnAgent.InferenceConfigurationProperty(
                            maximum_length=123,
                            stop_sequences=["stopSequences"],
                            temperature=123,
                            top_k=123,
                            top_p=123
                        ),
                        parser_mode="parserMode",
                        prompt_creation_mode="promptCreationMode",
                        prompt_state="promptState",
                        prompt_type="promptType"
                    )],
                
                    # the properties below are optional
                    override_lambda="overrideLambda"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__79a38248b49cbea1e103efe955cc12c1bd5e500b242bd9490c1c81253830d77d)
                check_type(argname="argument prompt_configurations", value=prompt_configurations, expected_type=type_hints["prompt_configurations"])
                check_type(argname="argument override_lambda", value=override_lambda, expected_type=type_hints["override_lambda"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "prompt_configurations": prompt_configurations,
            }
            if override_lambda is not None:
                self._values["override_lambda"] = override_lambda

        @builtins.property
        def prompt_configurations(
            self,
        ) -> typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, "CfnAgent.PromptConfigurationProperty"]]]:
            '''Contains configurations to override a prompt template in one part of an agent sequence.

            For more information, see `Advanced prompts <https://docs.aws.amazon.com/bedrock/latest/userguide/advanced-prompts.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-promptoverrideconfiguration.html#cfn-bedrock-agent-promptoverrideconfiguration-promptconfigurations
            '''
            result = self._values.get("prompt_configurations")
            assert result is not None, "Required property 'prompt_configurations' is missing"
            return typing.cast(typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, "CfnAgent.PromptConfigurationProperty"]]], result)

        @builtins.property
        def override_lambda(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Lambda function to use when parsing the raw foundation model output in parts of the agent sequence.

            If you specify this field, at least one of the ``promptConfigurations`` must contain a ``parserMode`` value that is set to ``OVERRIDDEN`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-promptoverrideconfiguration.html#cfn-bedrock-agent-promptoverrideconfiguration-overridelambda
            '''
            result = self._values.get("override_lambda")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PromptOverrideConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnAgent.S3IdentifierProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_bucket_name": "s3BucketName",
            "s3_object_key": "s3ObjectKey",
        },
    )
    class S3IdentifierProperty:
        def __init__(
            self,
            *,
            s3_bucket_name: typing.Optional[builtins.str] = None,
            s3_object_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the S3 object containing the resource.

            :param s3_bucket_name: The name of the S3 bucket.
            :param s3_object_key: The S3 object key containing the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-s3identifier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                s3_identifier_property = bedrock.CfnAgent.S3IdentifierProperty(
                    s3_bucket_name="s3BucketName",
                    s3_object_key="s3ObjectKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1e9a91ab9025dd36217ed95088c50220259ce5115620391445737700490cba60)
                check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
                check_type(argname="argument s3_object_key", value=s3_object_key, expected_type=type_hints["s3_object_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket_name is not None:
                self._values["s3_bucket_name"] = s3_bucket_name
            if s3_object_key is not None:
                self._values["s3_object_key"] = s3_object_key

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-s3identifier.html#cfn-bedrock-agent-s3identifier-s3bucketname
            '''
            result = self._values.get("s3_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_object_key(self) -> typing.Optional[builtins.str]:
            '''The S3 object key containing the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agent-s3identifier.html#cfn-bedrock-agent-s3identifier-s3objectkey
            '''
            result = self._values.get("s3_object_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3IdentifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_c2943556, _ITaggableV2_4e6798f8)
class CfnAgentAlias(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_bedrock.CfnAgentAlias",
):
    '''Specifies an agent alias as a resource in a top-level template. Minimally, you must specify the following properties:.

    - AgentAliasName – Specify a name for the alias.

    For more information about creating aliases for an agent in Amazon Bedrock , see `Deploy an Amazon Bedrock agent <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-deploy.html>`_ .

    See the *Properties* section below for descriptions of both the required and optional properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agentalias.html
    :cloudformationResource: AWS::Bedrock::AgentAlias
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_bedrock as bedrock
        
        cfn_agent_alias = bedrock.CfnAgentAlias(self, "MyCfnAgentAlias",
            agent_alias_name="agentAliasName",
            agent_id="agentId",
        
            # the properties below are optional
            description="description",
            routing_configuration=[bedrock.CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty(
                agent_version="agentVersion"
            )],
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        agent_alias_name: builtins.str,
        agent_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        routing_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union["CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param agent_alias_name: The name of the alias of the agent.
        :param agent_id: The unique identifier of the agent.
        :param description: The description of the alias of the agent.
        :param routing_configuration: Contains details about the routing configuration of the alias.
        :param tags: Metadata that you can assign to a resource as key-value pairs. For more information, see the following resources:. - `Tag naming limits and requirements <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-conventions>`_ - `Tagging best practices <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-best-practices>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a8230a990c5fac91dc09e3de4211aa6f82fce95537f199a7987ca92f4722ee0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAgentAliasProps(
            agent_alias_name=agent_alias_name,
            agent_id=agent_id,
            description=description,
            routing_configuration=routing_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881be8885c059b078e3110beb1aed396db2ce3f0505bec32be8cedeba399356d)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7100eb19771c4ffaea3a7323fe3cb5fcb6702a3fa7fdaf66bc8a4db1eae875c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAgentAliasArn")
    def attr_agent_alias_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the alias of the agent.

        :cloudformationAttribute: AgentAliasArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAgentAliasArn"))

    @builtins.property
    @jsii.member(jsii_name="attrAgentAliasHistoryEvents")
    def attr_agent_alias_history_events(self) -> _IResolvable_da3f097b:
        '''Contains details about the history of the alias.

        :cloudformationAttribute: AgentAliasHistoryEvents
        '''
        return typing.cast(_IResolvable_da3f097b, jsii.get(self, "attrAgentAliasHistoryEvents"))

    @builtins.property
    @jsii.member(jsii_name="attrAgentAliasId")
    def attr_agent_alias_id(self) -> builtins.str:
        '''The unique identifier of the alias of the agent.

        :cloudformationAttribute: AgentAliasId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAgentAliasId"))

    @builtins.property
    @jsii.member(jsii_name="attrAgentAliasStatus")
    def attr_agent_alias_status(self) -> builtins.str:
        '''The status of the alias of the agent and whether it is ready for use.

        The following statuses are possible:

        - CREATING – The agent alias is being created.
        - PREPARED – The agent alias is finished being created or updated and is ready to be invoked.
        - FAILED – The agent alias API operation failed.
        - UPDATING – The agent alias is being updated.
        - DELETING – The agent alias is being deleted.

        :cloudformationAttribute: AgentAliasStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAgentAliasStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The time at which the alias of the agent was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The time at which the alias was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> _TagManager_0a598cb3:
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="agentAliasName")
    def agent_alias_name(self) -> builtins.str:
        '''The name of the alias of the agent.'''
        return typing.cast(builtins.str, jsii.get(self, "agentAliasName"))

    @agent_alias_name.setter
    def agent_alias_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4929f9d1fe1c750108b588135fd2420ee93abad44713bd60a4f90bf0bab64e78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentAliasName", value)

    @builtins.property
    @jsii.member(jsii_name="agentId")
    def agent_id(self) -> builtins.str:
        '''The unique identifier of the agent.'''
        return typing.cast(builtins.str, jsii.get(self, "agentId"))

    @agent_id.setter
    def agent_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10c310fa33a8cb7b52c456850e88b42ea1b312acb49b915241cc6f52ef15136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the alias of the agent.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ab6386ae765e3eaf37d16d7a5314cdca1d8b60ea095a4fa303d13c84722e78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="routingConfiguration")
    def routing_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, "CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty"]]]]:
        '''Contains details about the routing configuration of the alias.'''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, "CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty"]]]], jsii.get(self, "routingConfiguration"))

    @routing_configuration.setter
    def routing_configuration(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, "CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca75abf30c6951a069bde3673588677ff723ad86067bf5365bb584482bed50a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata that you can assign to a resource as key-value pairs.

        For more information, see the following resources:.
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf90503b3b2050ab4f0f6ba0bf057a037193369214d4f027b567d3062bda19b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnAgentAlias.AgentAliasHistoryEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "end_date": "endDate",
            "routing_configuration": "routingConfiguration",
            "start_date": "startDate",
        },
    )
    class AgentAliasHistoryEventProperty:
        def __init__(
            self,
            *,
            end_date: typing.Optional[builtins.str] = None,
            routing_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union["CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            start_date: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains details about the history of the alias.

            :param end_date: The date that the alias stopped being associated to the version in the ``routingConfiguration`` object.
            :param routing_configuration: Contains details about the version of the agent with which the alias is associated.
            :param start_date: The date that the alias began being associated to the version in the ``routingConfiguration`` object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agentalias-agentaliashistoryevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                agent_alias_history_event_property = bedrock.CfnAgentAlias.AgentAliasHistoryEventProperty(
                    end_date="endDate",
                    routing_configuration=[bedrock.CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty(
                        agent_version="agentVersion"
                    )],
                    start_date="startDate"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4220f7b3bb12c49a75057af394368ca2d4de63c53d832e73767eb01f3bccb2ce)
                check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
                check_type(argname="argument routing_configuration", value=routing_configuration, expected_type=type_hints["routing_configuration"])
                check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end_date is not None:
                self._values["end_date"] = end_date
            if routing_configuration is not None:
                self._values["routing_configuration"] = routing_configuration
            if start_date is not None:
                self._values["start_date"] = start_date

        @builtins.property
        def end_date(self) -> typing.Optional[builtins.str]:
            '''The date that the alias stopped being associated to the version in the ``routingConfiguration`` object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agentalias-agentaliashistoryevent.html#cfn-bedrock-agentalias-agentaliashistoryevent-enddate
            '''
            result = self._values.get("end_date")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def routing_configuration(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, "CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty"]]]]:
            '''Contains details about the version of the agent with which the alias is associated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agentalias-agentaliashistoryevent.html#cfn-bedrock-agentalias-agentaliashistoryevent-routingconfiguration
            '''
            result = self._values.get("routing_configuration")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, "CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty"]]]], result)

        @builtins.property
        def start_date(self) -> typing.Optional[builtins.str]:
            '''The date that the alias began being associated to the version in the ``routingConfiguration`` object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agentalias-agentaliashistoryevent.html#cfn-bedrock-agentalias-agentaliashistoryevent-startdate
            '''
            result = self._values.get("start_date")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AgentAliasHistoryEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty",
        jsii_struct_bases=[],
        name_mapping={"agent_version": "agentVersion"},
    )
    class AgentAliasRoutingConfigurationListItemProperty:
        def __init__(self, *, agent_version: builtins.str) -> None:
            '''Contains details about the routing configuration of the alias.

            :param agent_version: The version of the agent with which the alias is associated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agentalias-agentaliasroutingconfigurationlistitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                agent_alias_routing_configuration_list_item_property = bedrock.CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty(
                    agent_version="agentVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__846d3bcc8614fd45d175f992a20505b220910c107392df0930556bb43637fc79)
                check_type(argname="argument agent_version", value=agent_version, expected_type=type_hints["agent_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "agent_version": agent_version,
            }

        @builtins.property
        def agent_version(self) -> builtins.str:
            '''The version of the agent with which the alias is associated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-agentalias-agentaliasroutingconfigurationlistitem.html#cfn-bedrock-agentalias-agentaliasroutingconfigurationlistitem-agentversion
            '''
            result = self._values.get("agent_version")
            assert result is not None, "Required property 'agent_version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AgentAliasRoutingConfigurationListItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_bedrock.CfnAgentAliasProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_alias_name": "agentAliasName",
        "agent_id": "agentId",
        "description": "description",
        "routing_configuration": "routingConfiguration",
        "tags": "tags",
    },
)
class CfnAgentAliasProps:
    def __init__(
        self,
        *,
        agent_alias_name: builtins.str,
        agent_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        routing_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAgentAlias``.

        :param agent_alias_name: The name of the alias of the agent.
        :param agent_id: The unique identifier of the agent.
        :param description: The description of the alias of the agent.
        :param routing_configuration: Contains details about the routing configuration of the alias.
        :param tags: Metadata that you can assign to a resource as key-value pairs. For more information, see the following resources:. - `Tag naming limits and requirements <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-conventions>`_ - `Tagging best practices <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-best-practices>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agentalias.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_bedrock as bedrock
            
            cfn_agent_alias_props = bedrock.CfnAgentAliasProps(
                agent_alias_name="agentAliasName",
                agent_id="agentId",
            
                # the properties below are optional
                description="description",
                routing_configuration=[bedrock.CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty(
                    agent_version="agentVersion"
                )],
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3144a1c66c11b4a2b15be859f361c848648aefb3df04b8fce2befe94f215c68)
            check_type(argname="argument agent_alias_name", value=agent_alias_name, expected_type=type_hints["agent_alias_name"])
            check_type(argname="argument agent_id", value=agent_id, expected_type=type_hints["agent_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument routing_configuration", value=routing_configuration, expected_type=type_hints["routing_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_alias_name": agent_alias_name,
            "agent_id": agent_id,
        }
        if description is not None:
            self._values["description"] = description
        if routing_configuration is not None:
            self._values["routing_configuration"] = routing_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_alias_name(self) -> builtins.str:
        '''The name of the alias of the agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agentalias.html#cfn-bedrock-agentalias-agentaliasname
        '''
        result = self._values.get("agent_alias_name")
        assert result is not None, "Required property 'agent_alias_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_id(self) -> builtins.str:
        '''The unique identifier of the agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agentalias.html#cfn-bedrock-agentalias-agentid
        '''
        result = self._values.get("agent_id")
        assert result is not None, "Required property 'agent_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the alias of the agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agentalias.html#cfn-bedrock-agentalias-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty]]]]:
        '''Contains details about the routing configuration of the alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agentalias.html#cfn-bedrock-agentalias-routingconfiguration
        '''
        result = self._values.get("routing_configuration")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata that you can assign to a resource as key-value pairs. For more information, see the following resources:.

        - `Tag naming limits and requirements <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-conventions>`_
        - `Tagging best practices <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-best-practices>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agentalias.html#cfn-bedrock-agentalias-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAgentAliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_bedrock.CfnAgentProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_name": "agentName",
        "action_groups": "actionGroups",
        "agent_resource_role_arn": "agentResourceRoleArn",
        "auto_prepare": "autoPrepare",
        "customer_encryption_key_arn": "customerEncryptionKeyArn",
        "description": "description",
        "foundation_model": "foundationModel",
        "idle_session_ttl_in_seconds": "idleSessionTtlInSeconds",
        "instruction": "instruction",
        "knowledge_bases": "knowledgeBases",
        "prompt_override_configuration": "promptOverrideConfiguration",
        "skip_resource_in_use_check_on_delete": "skipResourceInUseCheckOnDelete",
        "tags": "tags",
    },
)
class CfnAgentProps:
    def __init__(
        self,
        *,
        agent_name: builtins.str,
        action_groups: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgent.AgentActionGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        agent_resource_role_arn: typing.Optional[builtins.str] = None,
        auto_prepare: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        customer_encryption_key_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        foundation_model: typing.Optional[builtins.str] = None,
        idle_session_ttl_in_seconds: typing.Optional[jsii.Number] = None,
        instruction: typing.Optional[builtins.str] = None,
        knowledge_bases: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgent.AgentKnowledgeBaseProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        prompt_override_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgent.PromptOverrideConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        skip_resource_in_use_check_on_delete: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAgent``.

        :param agent_name: The name of the agent.
        :param action_groups: The action groups that belong to an agent.
        :param agent_resource_role_arn: The Amazon Resource Name (ARN) of the IAM role with permissions to invoke API operations on the agent.
        :param auto_prepare: Specifies whether to automatically update the ``DRAFT`` version of the agent after making changes to the agent. The ``DRAFT`` version can be continually iterated upon during internal development. By default, this value is ``false`` . Default: - false
        :param customer_encryption_key_arn: The Amazon Resource Name (ARN) of the AWS KMS key that encrypts the agent.
        :param description: The description of the agent.
        :param foundation_model: The foundation model used for orchestration by the agent.
        :param idle_session_ttl_in_seconds: The number of seconds for which Amazon Bedrock keeps information about a user's conversation with the agent. A user interaction remains active for the amount of time specified. If no conversation occurs during this time, the session expires and Amazon Bedrock deletes any data provided before the timeout.
        :param instruction: Instructions that tell the agent what it should do and how it should interact with users.
        :param knowledge_bases: The knowledge bases associated with the agent.
        :param prompt_override_configuration: Contains configurations to override prompt templates in different parts of an agent sequence. For more information, see `Advanced prompts <https://docs.aws.amazon.com/bedrock/latest/userguide/advanced-prompts.html>`_ .
        :param skip_resource_in_use_check_on_delete: Specifies whether to delete the resource even if it's in use. By default, this value is ``false`` . Default: - false
        :param tags: Metadata that you can assign to a resource as key-value pairs. For more information, see the following resources:. - `Tag naming limits and requirements <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-conventions>`_ - `Tagging best practices <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-best-practices>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_bedrock as bedrock
            
            cfn_agent_props = bedrock.CfnAgentProps(
                agent_name="agentName",
            
                # the properties below are optional
                action_groups=[bedrock.CfnAgent.AgentActionGroupProperty(
                    action_group_name="actionGroupName",
            
                    # the properties below are optional
                    action_group_executor=bedrock.CfnAgent.ActionGroupExecutorProperty(
                        lambda_="lambda"
                    ),
                    action_group_state="actionGroupState",
                    api_schema=bedrock.CfnAgent.APISchemaProperty(
                        payload="payload",
                        s3=bedrock.CfnAgent.S3IdentifierProperty(
                            s3_bucket_name="s3BucketName",
                            s3_object_key="s3ObjectKey"
                        )
                    ),
                    description="description",
                    parent_action_group_signature="parentActionGroupSignature",
                    skip_resource_in_use_check_on_delete=False
                )],
                agent_resource_role_arn="agentResourceRoleArn",
                auto_prepare=False,
                customer_encryption_key_arn="customerEncryptionKeyArn",
                description="description",
                foundation_model="foundationModel",
                idle_session_ttl_in_seconds=123,
                instruction="instruction",
                knowledge_bases=[bedrock.CfnAgent.AgentKnowledgeBaseProperty(
                    description="description",
                    knowledge_base_id="knowledgeBaseId",
            
                    # the properties below are optional
                    knowledge_base_state="knowledgeBaseState"
                )],
                prompt_override_configuration=bedrock.CfnAgent.PromptOverrideConfigurationProperty(
                    prompt_configurations=[bedrock.CfnAgent.PromptConfigurationProperty(
                        base_prompt_template="basePromptTemplate",
                        inference_configuration=bedrock.CfnAgent.InferenceConfigurationProperty(
                            maximum_length=123,
                            stop_sequences=["stopSequences"],
                            temperature=123,
                            top_k=123,
                            top_p=123
                        ),
                        parser_mode="parserMode",
                        prompt_creation_mode="promptCreationMode",
                        prompt_state="promptState",
                        prompt_type="promptType"
                    )],
            
                    # the properties below are optional
                    override_lambda="overrideLambda"
                ),
                skip_resource_in_use_check_on_delete=False,
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4f714080f6d4f9b0a3fe85a8425a8ba69698695e35d6fbd9d710ca5d99ba6e8)
            check_type(argname="argument agent_name", value=agent_name, expected_type=type_hints["agent_name"])
            check_type(argname="argument action_groups", value=action_groups, expected_type=type_hints["action_groups"])
            check_type(argname="argument agent_resource_role_arn", value=agent_resource_role_arn, expected_type=type_hints["agent_resource_role_arn"])
            check_type(argname="argument auto_prepare", value=auto_prepare, expected_type=type_hints["auto_prepare"])
            check_type(argname="argument customer_encryption_key_arn", value=customer_encryption_key_arn, expected_type=type_hints["customer_encryption_key_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument foundation_model", value=foundation_model, expected_type=type_hints["foundation_model"])
            check_type(argname="argument idle_session_ttl_in_seconds", value=idle_session_ttl_in_seconds, expected_type=type_hints["idle_session_ttl_in_seconds"])
            check_type(argname="argument instruction", value=instruction, expected_type=type_hints["instruction"])
            check_type(argname="argument knowledge_bases", value=knowledge_bases, expected_type=type_hints["knowledge_bases"])
            check_type(argname="argument prompt_override_configuration", value=prompt_override_configuration, expected_type=type_hints["prompt_override_configuration"])
            check_type(argname="argument skip_resource_in_use_check_on_delete", value=skip_resource_in_use_check_on_delete, expected_type=type_hints["skip_resource_in_use_check_on_delete"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_name": agent_name,
        }
        if action_groups is not None:
            self._values["action_groups"] = action_groups
        if agent_resource_role_arn is not None:
            self._values["agent_resource_role_arn"] = agent_resource_role_arn
        if auto_prepare is not None:
            self._values["auto_prepare"] = auto_prepare
        if customer_encryption_key_arn is not None:
            self._values["customer_encryption_key_arn"] = customer_encryption_key_arn
        if description is not None:
            self._values["description"] = description
        if foundation_model is not None:
            self._values["foundation_model"] = foundation_model
        if idle_session_ttl_in_seconds is not None:
            self._values["idle_session_ttl_in_seconds"] = idle_session_ttl_in_seconds
        if instruction is not None:
            self._values["instruction"] = instruction
        if knowledge_bases is not None:
            self._values["knowledge_bases"] = knowledge_bases
        if prompt_override_configuration is not None:
            self._values["prompt_override_configuration"] = prompt_override_configuration
        if skip_resource_in_use_check_on_delete is not None:
            self._values["skip_resource_in_use_check_on_delete"] = skip_resource_in_use_check_on_delete
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_name(self) -> builtins.str:
        '''The name of the agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html#cfn-bedrock-agent-agentname
        '''
        result = self._values.get("agent_name")
        assert result is not None, "Required property 'agent_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_groups(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, CfnAgent.AgentActionGroupProperty]]]]:
        '''The action groups that belong to an agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html#cfn-bedrock-agent-actiongroups
        '''
        result = self._values.get("action_groups")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, CfnAgent.AgentActionGroupProperty]]]], result)

    @builtins.property
    def agent_resource_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role with permissions to invoke API operations on the agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html#cfn-bedrock-agent-agentresourcerolearn
        '''
        result = self._values.get("agent_resource_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_prepare(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''Specifies whether to automatically update the ``DRAFT`` version of the agent after making changes to the agent.

        The ``DRAFT`` version can be continually iterated upon during internal development. By default, this value is ``false`` .

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html#cfn-bedrock-agent-autoprepare
        '''
        result = self._values.get("auto_prepare")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

    @builtins.property
    def customer_encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS KMS key that encrypts the agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html#cfn-bedrock-agent-customerencryptionkeyarn
        '''
        result = self._values.get("customer_encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html#cfn-bedrock-agent-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def foundation_model(self) -> typing.Optional[builtins.str]:
        '''The foundation model used for orchestration by the agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html#cfn-bedrock-agent-foundationmodel
        '''
        result = self._values.get("foundation_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_session_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds for which Amazon Bedrock keeps information about a user's conversation with the agent.

        A user interaction remains active for the amount of time specified. If no conversation occurs during this time, the session expires and Amazon Bedrock deletes any data provided before the timeout.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html#cfn-bedrock-agent-idlesessionttlinseconds
        '''
        result = self._values.get("idle_session_ttl_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instruction(self) -> typing.Optional[builtins.str]:
        '''Instructions that tell the agent what it should do and how it should interact with users.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html#cfn-bedrock-agent-instruction
        '''
        result = self._values.get("instruction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def knowledge_bases(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, CfnAgent.AgentKnowledgeBaseProperty]]]]:
        '''The knowledge bases associated with the agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html#cfn-bedrock-agent-knowledgebases
        '''
        result = self._values.get("knowledge_bases")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, CfnAgent.AgentKnowledgeBaseProperty]]]], result)

    @builtins.property
    def prompt_override_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, CfnAgent.PromptOverrideConfigurationProperty]]:
        '''Contains configurations to override prompt templates in different parts of an agent sequence.

        For more information, see `Advanced prompts <https://docs.aws.amazon.com/bedrock/latest/userguide/advanced-prompts.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html#cfn-bedrock-agent-promptoverrideconfiguration
        '''
        result = self._values.get("prompt_override_configuration")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, CfnAgent.PromptOverrideConfigurationProperty]], result)

    @builtins.property
    def skip_resource_in_use_check_on_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''Specifies whether to delete the resource even if it's in use.

        By default, this value is ``false`` .

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html#cfn-bedrock-agent-skipresourceinusecheckondelete
        '''
        result = self._values.get("skip_resource_in_use_check_on_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata that you can assign to a resource as key-value pairs. For more information, see the following resources:.

        - `Tag naming limits and requirements <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-conventions>`_
        - `Tagging best practices <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-best-practices>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-agent.html#cfn-bedrock-agent-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAgentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnDataSource(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_bedrock.CfnDataSource",
):
    '''Specifies a data source as a resource in a top-level template. Minimally, you must specify the following properties:.

    - Name – Specify a name for the data source.
    - KnowledgeBaseId – Specify the ID of the knowledge base for the data source to belong to.
    - DataSourceConfiguration – Specify information about the Amazon S3 bucket containing the data source. The following sub-properties are required:
    - Type – Specify the value ``S3`` .

    For more information about setting up data sources in Amazon Bedrock , see `Set up a data source for your knowledge base <https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-ds.html>`_ .

    See the *Properties* section below for descriptions of both the required and optional properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-datasource.html
    :cloudformationResource: AWS::Bedrock::DataSource
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_bedrock as bedrock
        
        cfn_data_source = bedrock.CfnDataSource(self, "MyCfnDataSource",
            data_source_configuration=bedrock.CfnDataSource.DataSourceConfigurationProperty(
                s3_configuration=bedrock.CfnDataSource.S3DataSourceConfigurationProperty(
                    bucket_arn="bucketArn",
        
                    # the properties below are optional
                    inclusion_prefixes=["inclusionPrefixes"]
                ),
                type="type"
            ),
            knowledge_base_id="knowledgeBaseId",
            name="name",
        
            # the properties below are optional
            description="description",
            server_side_encryption_configuration=bedrock.CfnDataSource.ServerSideEncryptionConfigurationProperty(
                kms_key_arn="kmsKeyArn"
            ),
            vector_ingestion_configuration=bedrock.CfnDataSource.VectorIngestionConfigurationProperty(
                chunking_configuration=bedrock.CfnDataSource.ChunkingConfigurationProperty(
                    chunking_strategy="chunkingStrategy",
        
                    # the properties below are optional
                    fixed_size_chunking_configuration=bedrock.CfnDataSource.FixedSizeChunkingConfigurationProperty(
                        max_tokens=123,
                        overlap_percentage=123
                    )
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        data_source_configuration: typing.Union[_IResolvable_da3f097b, typing.Union["CfnDataSource.DataSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        knowledge_base_id: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union["CfnDataSource.ServerSideEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        vector_ingestion_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union["CfnDataSource.VectorIngestionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param data_source_configuration: Contains details about how the data source is stored.
        :param knowledge_base_id: The unique identifier of the knowledge base to which the data source belongs.
        :param name: The name of the data source.
        :param description: The description of the data source.
        :param server_side_encryption_configuration: Contains details about the configuration of the server-side encryption.
        :param vector_ingestion_configuration: Contains details about how to ingest the documents in the data source.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6230da788965416b3262c41917eaab2193b3cfccf7a03f313a8c19186a6b75)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDataSourceProps(
            data_source_configuration=data_source_configuration,
            knowledge_base_id=knowledge_base_id,
            name=name,
            description=description,
            server_side_encryption_configuration=server_side_encryption_configuration,
            vector_ingestion_configuration=vector_ingestion_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e68a33df1c2e42bd5580cdec505e709cbe6a0663b8142f6fb3ba8e70911ceb85)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b23978dd788bb65ad2e2571764c987a4729f9d5c9d17c903f53a10cd4e3ad3e7)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The time at which the data source was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrDataSourceId")
    def attr_data_source_id(self) -> builtins.str:
        '''The unique identifier of the data source.

        :cloudformationAttribute: DataSourceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="attrDataSourceStatus")
    def attr_data_source_status(self) -> builtins.str:
        '''The status of the data source. The following statuses are possible:.

        - Available – The data source has been created and is ready for ingestion into the knowledge base.
        - Deleting – The data source is being deleted.

        :cloudformationAttribute: DataSourceStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDataSourceStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The time at which the data source was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceConfiguration")
    def data_source_configuration(
        self,
    ) -> typing.Union[_IResolvable_da3f097b, "CfnDataSource.DataSourceConfigurationProperty"]:
        '''Contains details about how the data source is stored.'''
        return typing.cast(typing.Union[_IResolvable_da3f097b, "CfnDataSource.DataSourceConfigurationProperty"], jsii.get(self, "dataSourceConfiguration"))

    @data_source_configuration.setter
    def data_source_configuration(
        self,
        value: typing.Union[_IResolvable_da3f097b, "CfnDataSource.DataSourceConfigurationProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a387108ccda2b96813f79478d4429abb297f766ce080c3bf9b77d03af3db534c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseId")
    def knowledge_base_id(self) -> builtins.str:
        '''The unique identifier of the knowledge base to which the data source belongs.'''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseId"))

    @knowledge_base_id.setter
    def knowledge_base_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d585d364d6684899cbce3ae80a62858e2f256e166c889705e2ecb2040e935d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "knowledgeBaseId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the data source.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99613771dd63beb77d047c2f17b9362e99ec38dd6fb89ec0c78f690f7847fc0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the data source.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc31b7620f239d59ff8a40cb711119c09cf659e115e22ba5d86a3d2a36aa17b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnDataSource.ServerSideEncryptionConfigurationProperty"]]:
        '''Contains details about the configuration of the server-side encryption.'''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnDataSource.ServerSideEncryptionConfigurationProperty"]], jsii.get(self, "serverSideEncryptionConfiguration"))

    @server_side_encryption_configuration.setter
    def server_side_encryption_configuration(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnDataSource.ServerSideEncryptionConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe19aafcbb9637979bddaf7a230433b26f791bb09744dabcf0e95496322565d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverSideEncryptionConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="vectorIngestionConfiguration")
    def vector_ingestion_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnDataSource.VectorIngestionConfigurationProperty"]]:
        '''Contains details about how to ingest the documents in the data source.'''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnDataSource.VectorIngestionConfigurationProperty"]], jsii.get(self, "vectorIngestionConfiguration"))

    @vector_ingestion_configuration.setter
    def vector_ingestion_configuration(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnDataSource.VectorIngestionConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__033990e14b671fe96b02a12658cd4beadf8bae975b4e0c94984d3e41913522c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vectorIngestionConfiguration", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnDataSource.ChunkingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "chunking_strategy": "chunkingStrategy",
            "fixed_size_chunking_configuration": "fixedSizeChunkingConfiguration",
        },
    )
    class ChunkingConfigurationProperty:
        def __init__(
            self,
            *,
            chunking_strategy: builtins.str,
            fixed_size_chunking_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union["CfnDataSource.FixedSizeChunkingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Details about how to chunk the documents in the data source.

            A *chunk* refers to an excerpt from a data source that is returned when the knowledge base that it belongs to is queried.

            :param chunking_strategy: Knowledge base can split your source data into chunks. A *chunk* refers to an excerpt from a data source that is returned when the knowledge base that it belongs to is queried. You have the following options for chunking your data. If you opt for ``NONE`` , then you may want to pre-process your files by splitting them up such that each file corresponds to a chunk. - ``FIXED_SIZE`` – Amazon Bedrock splits your source data into chunks of the approximate size that you set in the ``fixedSizeChunkingConfiguration`` . - ``NONE`` – Amazon Bedrock treats each file as one chunk. If you choose this option, you may want to pre-process your documents by splitting them into separate files.
            :param fixed_size_chunking_configuration: Configurations for when you choose fixed-size chunking. If you set the ``chunkingStrategy`` as ``NONE`` , exclude this field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-chunkingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                chunking_configuration_property = bedrock.CfnDataSource.ChunkingConfigurationProperty(
                    chunking_strategy="chunkingStrategy",
                
                    # the properties below are optional
                    fixed_size_chunking_configuration=bedrock.CfnDataSource.FixedSizeChunkingConfigurationProperty(
                        max_tokens=123,
                        overlap_percentage=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8beec747a0f57f641fd4bd3b03f73b678c8e286785d948f80998682f0c0a40e5)
                check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
                check_type(argname="argument fixed_size_chunking_configuration", value=fixed_size_chunking_configuration, expected_type=type_hints["fixed_size_chunking_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "chunking_strategy": chunking_strategy,
            }
            if fixed_size_chunking_configuration is not None:
                self._values["fixed_size_chunking_configuration"] = fixed_size_chunking_configuration

        @builtins.property
        def chunking_strategy(self) -> builtins.str:
            '''Knowledge base can split your source data into chunks.

            A *chunk* refers to an excerpt from a data source that is returned when the knowledge base that it belongs to is queried. You have the following options for chunking your data. If you opt for ``NONE`` , then you may want to pre-process your files by splitting them up such that each file corresponds to a chunk.

            - ``FIXED_SIZE`` – Amazon Bedrock splits your source data into chunks of the approximate size that you set in the ``fixedSizeChunkingConfiguration`` .
            - ``NONE`` – Amazon Bedrock treats each file as one chunk. If you choose this option, you may want to pre-process your documents by splitting them into separate files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-chunkingconfiguration.html#cfn-bedrock-datasource-chunkingconfiguration-chunkingstrategy
            '''
            result = self._values.get("chunking_strategy")
            assert result is not None, "Required property 'chunking_strategy' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def fixed_size_chunking_configuration(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnDataSource.FixedSizeChunkingConfigurationProperty"]]:
            '''Configurations for when you choose fixed-size chunking.

            If you set the ``chunkingStrategy`` as ``NONE`` , exclude this field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-chunkingconfiguration.html#cfn-bedrock-datasource-chunkingconfiguration-fixedsizechunkingconfiguration
            '''
            result = self._values.get("fixed_size_chunking_configuration")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnDataSource.FixedSizeChunkingConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChunkingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnDataSource.DataSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_configuration": "s3Configuration", "type": "type"},
    )
    class DataSourceConfigurationProperty:
        def __init__(
            self,
            *,
            s3_configuration: typing.Union[_IResolvable_da3f097b, typing.Union["CfnDataSource.S3DataSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
            type: builtins.str,
        ) -> None:
            '''Contains details about how a data source is stored.

            :param s3_configuration: Contains details about the configuration of the S3 object containing the data source.
            :param type: The type of storage for the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-datasourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                data_source_configuration_property = bedrock.CfnDataSource.DataSourceConfigurationProperty(
                    s3_configuration=bedrock.CfnDataSource.S3DataSourceConfigurationProperty(
                        bucket_arn="bucketArn",
                
                        # the properties below are optional
                        inclusion_prefixes=["inclusionPrefixes"]
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2e1b0c807d6904904c91cc13a2f47ee5db24090758446e26a864b57b3d36117)
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_configuration": s3_configuration,
                "type": type,
            }

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Union[_IResolvable_da3f097b, "CfnDataSource.S3DataSourceConfigurationProperty"]:
            '''Contains details about the configuration of the S3 object containing the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-datasourceconfiguration.html#cfn-bedrock-datasource-datasourceconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            assert result is not None, "Required property 's3_configuration' is missing"
            return typing.cast(typing.Union[_IResolvable_da3f097b, "CfnDataSource.S3DataSourceConfigurationProperty"], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of storage for the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-datasourceconfiguration.html#cfn-bedrock-datasource-datasourceconfiguration-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnDataSource.FixedSizeChunkingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_tokens": "maxTokens",
            "overlap_percentage": "overlapPercentage",
        },
    )
    class FixedSizeChunkingConfigurationProperty:
        def __init__(
            self,
            *,
            max_tokens: jsii.Number,
            overlap_percentage: jsii.Number,
        ) -> None:
            '''Configurations for when you choose fixed-size chunking.

            If you set the ``chunkingStrategy`` as ``NONE`` , exclude this field.

            :param max_tokens: The maximum number of tokens to include in a chunk.
            :param overlap_percentage: The percentage of overlap between adjacent chunks of a data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-fixedsizechunkingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                fixed_size_chunking_configuration_property = bedrock.CfnDataSource.FixedSizeChunkingConfigurationProperty(
                    max_tokens=123,
                    overlap_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7b9e8054cbf79d2292e738f1061947914954b89440b15bf572c87c9695aaf7bc)
                check_type(argname="argument max_tokens", value=max_tokens, expected_type=type_hints["max_tokens"])
                check_type(argname="argument overlap_percentage", value=overlap_percentage, expected_type=type_hints["overlap_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "max_tokens": max_tokens,
                "overlap_percentage": overlap_percentage,
            }

        @builtins.property
        def max_tokens(self) -> jsii.Number:
            '''The maximum number of tokens to include in a chunk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-fixedsizechunkingconfiguration.html#cfn-bedrock-datasource-fixedsizechunkingconfiguration-maxtokens
            '''
            result = self._values.get("max_tokens")
            assert result is not None, "Required property 'max_tokens' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def overlap_percentage(self) -> jsii.Number:
            '''The percentage of overlap between adjacent chunks of a data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-fixedsizechunkingconfiguration.html#cfn-bedrock-datasource-fixedsizechunkingconfiguration-overlappercentage
            '''
            result = self._values.get("overlap_percentage")
            assert result is not None, "Required property 'overlap_percentage' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FixedSizeChunkingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnDataSource.S3DataSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_arn": "bucketArn",
            "inclusion_prefixes": "inclusionPrefixes",
        },
    )
    class S3DataSourceConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_arn: builtins.str,
            inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Contains information about the S3 configuration of the data source.

            :param bucket_arn: The Amazon Resource Name (ARN) of the bucket that contains the data source.
            :param inclusion_prefixes: A list of S3 prefixes that define the object containing the data sources. For more information, see `Organizing objects using prefixes <https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-s3datasourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                s3_data_source_configuration_property = bedrock.CfnDataSource.S3DataSourceConfigurationProperty(
                    bucket_arn="bucketArn",
                
                    # the properties below are optional
                    inclusion_prefixes=["inclusionPrefixes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b4929296343a5ea55bce5d28d11b34fa10885df35596a08102658f8bcbc8c5b)
                check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
                check_type(argname="argument inclusion_prefixes", value=inclusion_prefixes, expected_type=type_hints["inclusion_prefixes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_arn": bucket_arn,
            }
            if inclusion_prefixes is not None:
                self._values["inclusion_prefixes"] = inclusion_prefixes

        @builtins.property
        def bucket_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the bucket that contains the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-s3datasourceconfiguration.html#cfn-bedrock-datasource-s3datasourceconfiguration-bucketarn
            '''
            result = self._values.get("bucket_arn")
            assert result is not None, "Required property 'bucket_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def inclusion_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of S3 prefixes that define the object containing the data sources.

            For more information, see `Organizing objects using prefixes <https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-s3datasourceconfiguration.html#cfn-bedrock-datasource-s3datasourceconfiguration-inclusionprefixes
            '''
            result = self._values.get("inclusion_prefixes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DataSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnDataSource.ServerSideEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_arn": "kmsKeyArn"},
    )
    class ServerSideEncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the configuration for server-side encryption.

            :param kms_key_arn: The Amazon Resource Name (ARN) of the AWS KMS key used to encrypt the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-serversideencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                server_side_encryption_configuration_property = bedrock.CfnDataSource.ServerSideEncryptionConfigurationProperty(
                    kms_key_arn="kmsKeyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7bf662e3d628b0671b547dd26face3c322a93684b4b5578ec4cda1099b30e6a)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS KMS key used to encrypt the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-serversideencryptionconfiguration.html#cfn-bedrock-datasource-serversideencryptionconfiguration-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnDataSource.VectorIngestionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"chunking_configuration": "chunkingConfiguration"},
    )
    class VectorIngestionConfigurationProperty:
        def __init__(
            self,
            *,
            chunking_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union["CfnDataSource.ChunkingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains details about how to ingest the documents in a data source.

            :param chunking_configuration: Details about how to chunk the documents in the data source. A *chunk* refers to an excerpt from a data source that is returned when the knowledge base that it belongs to is queried.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-vectoringestionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                vector_ingestion_configuration_property = bedrock.CfnDataSource.VectorIngestionConfigurationProperty(
                    chunking_configuration=bedrock.CfnDataSource.ChunkingConfigurationProperty(
                        chunking_strategy="chunkingStrategy",
                
                        # the properties below are optional
                        fixed_size_chunking_configuration=bedrock.CfnDataSource.FixedSizeChunkingConfigurationProperty(
                            max_tokens=123,
                            overlap_percentage=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__37255db3e7cacfdeadc2d28bfe7938fd13ab4a2cd72190024a531eddf1fd9ec0)
                check_type(argname="argument chunking_configuration", value=chunking_configuration, expected_type=type_hints["chunking_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if chunking_configuration is not None:
                self._values["chunking_configuration"] = chunking_configuration

        @builtins.property
        def chunking_configuration(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnDataSource.ChunkingConfigurationProperty"]]:
            '''Details about how to chunk the documents in the data source.

            A *chunk* refers to an excerpt from a data source that is returned when the knowledge base that it belongs to is queried.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-datasource-vectoringestionconfiguration.html#cfn-bedrock-datasource-vectoringestionconfiguration-chunkingconfiguration
            '''
            result = self._values.get("chunking_configuration")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, "CfnDataSource.ChunkingConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VectorIngestionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_bedrock.CfnDataSourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_source_configuration": "dataSourceConfiguration",
        "knowledge_base_id": "knowledgeBaseId",
        "name": "name",
        "description": "description",
        "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        "vector_ingestion_configuration": "vectorIngestionConfiguration",
    },
)
class CfnDataSourceProps:
    def __init__(
        self,
        *,
        data_source_configuration: typing.Union[_IResolvable_da3f097b, typing.Union[CfnDataSource.DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
        knowledge_base_id: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnDataSource.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        vector_ingestion_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnDataSource.VectorIngestionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDataSource``.

        :param data_source_configuration: Contains details about how the data source is stored.
        :param knowledge_base_id: The unique identifier of the knowledge base to which the data source belongs.
        :param name: The name of the data source.
        :param description: The description of the data source.
        :param server_side_encryption_configuration: Contains details about the configuration of the server-side encryption.
        :param vector_ingestion_configuration: Contains details about how to ingest the documents in the data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-datasource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_bedrock as bedrock
            
            cfn_data_source_props = bedrock.CfnDataSourceProps(
                data_source_configuration=bedrock.CfnDataSource.DataSourceConfigurationProperty(
                    s3_configuration=bedrock.CfnDataSource.S3DataSourceConfigurationProperty(
                        bucket_arn="bucketArn",
            
                        # the properties below are optional
                        inclusion_prefixes=["inclusionPrefixes"]
                    ),
                    type="type"
                ),
                knowledge_base_id="knowledgeBaseId",
                name="name",
            
                # the properties below are optional
                description="description",
                server_side_encryption_configuration=bedrock.CfnDataSource.ServerSideEncryptionConfigurationProperty(
                    kms_key_arn="kmsKeyArn"
                ),
                vector_ingestion_configuration=bedrock.CfnDataSource.VectorIngestionConfigurationProperty(
                    chunking_configuration=bedrock.CfnDataSource.ChunkingConfigurationProperty(
                        chunking_strategy="chunkingStrategy",
            
                        # the properties below are optional
                        fixed_size_chunking_configuration=bedrock.CfnDataSource.FixedSizeChunkingConfigurationProperty(
                            max_tokens=123,
                            overlap_percentage=123
                        )
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4beca3e3b31c91619a3fa9da2bf185ffd738124b7965f1c90a191b43c7b62664)
            check_type(argname="argument data_source_configuration", value=data_source_configuration, expected_type=type_hints["data_source_configuration"])
            check_type(argname="argument knowledge_base_id", value=knowledge_base_id, expected_type=type_hints["knowledge_base_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument server_side_encryption_configuration", value=server_side_encryption_configuration, expected_type=type_hints["server_side_encryption_configuration"])
            check_type(argname="argument vector_ingestion_configuration", value=vector_ingestion_configuration, expected_type=type_hints["vector_ingestion_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source_configuration": data_source_configuration,
            "knowledge_base_id": knowledge_base_id,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if server_side_encryption_configuration is not None:
            self._values["server_side_encryption_configuration"] = server_side_encryption_configuration
        if vector_ingestion_configuration is not None:
            self._values["vector_ingestion_configuration"] = vector_ingestion_configuration

    @builtins.property
    def data_source_configuration(
        self,
    ) -> typing.Union[_IResolvable_da3f097b, CfnDataSource.DataSourceConfigurationProperty]:
        '''Contains details about how the data source is stored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-datasource.html#cfn-bedrock-datasource-datasourceconfiguration
        '''
        result = self._values.get("data_source_configuration")
        assert result is not None, "Required property 'data_source_configuration' is missing"
        return typing.cast(typing.Union[_IResolvable_da3f097b, CfnDataSource.DataSourceConfigurationProperty], result)

    @builtins.property
    def knowledge_base_id(self) -> builtins.str:
        '''The unique identifier of the knowledge base to which the data source belongs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-datasource.html#cfn-bedrock-datasource-knowledgebaseid
        '''
        result = self._values.get("knowledge_base_id")
        assert result is not None, "Required property 'knowledge_base_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-datasource.html#cfn-bedrock-datasource-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-datasource.html#cfn-bedrock-datasource-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, CfnDataSource.ServerSideEncryptionConfigurationProperty]]:
        '''Contains details about the configuration of the server-side encryption.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-datasource.html#cfn-bedrock-datasource-serversideencryptionconfiguration
        '''
        result = self._values.get("server_side_encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, CfnDataSource.ServerSideEncryptionConfigurationProperty]], result)

    @builtins.property
    def vector_ingestion_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, CfnDataSource.VectorIngestionConfigurationProperty]]:
        '''Contains details about how to ingest the documents in the data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-datasource.html#cfn-bedrock-datasource-vectoringestionconfiguration
        '''
        result = self._values.get("vector_ingestion_configuration")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, CfnDataSource.VectorIngestionConfigurationProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556, _ITaggableV2_4e6798f8)
class CfnKnowledgeBase(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_bedrock.CfnKnowledgeBase",
):
    '''Specifies a knowledge base as a resource in a top-level template. Minimally, you must specify the following properties:.

    - Name – Specify a name for the knowledge base.
    - RoleArn – Specify the Amazon Resource Name (ARN) of the IAM role with permissions to invoke API operations on the knowledge base. For more information, see `Create a service role for Knowledge base for Amazon Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/kb-permissions.html>`_ .
    - KnowledgeBaseConfiguration – Specify the embeddings configuration of the knowledge base. The following sub-properties are required:
    - Type – Specify the value ``VECTOR`` .
    - StorageConfiguration – Specify information about the vector store in which the data source is stored. The following sub-properties are required:
    - Type – Specify the vector store service that you are using.

    .. epigraph::

       Redis Enterprise Cloud vector stores are currently unsupported in AWS CloudFormation .

    For more information about using knowledge bases in Amazon Bedrock , see `Knowledge base for Amazon Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html>`_ .

    See the *Properties* section below for descriptions of both the required and optional properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-knowledgebase.html
    :cloudformationResource: AWS::Bedrock::KnowledgeBase
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_bedrock as bedrock
        
        cfn_knowledge_base = bedrock.CfnKnowledgeBase(self, "MyCfnKnowledgeBase",
            knowledge_base_configuration=bedrock.CfnKnowledgeBase.KnowledgeBaseConfigurationProperty(
                type="type",
                vector_knowledge_base_configuration=bedrock.CfnKnowledgeBase.VectorKnowledgeBaseConfigurationProperty(
                    embedding_model_arn="embeddingModelArn"
                )
            ),
            name="name",
            role_arn="roleArn",
        
            # the properties below are optional
            description="description",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        knowledge_base_configuration: typing.Union[_IResolvable_da3f097b, typing.Union["CfnKnowledgeBase.KnowledgeBaseConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        name: builtins.str,
        role_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param knowledge_base_configuration: Contains details about the embeddings configuration of the knowledge base.
        :param name: The name of the knowledge base.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role with permissions to invoke API operations on the knowledge base.
        :param description: The description of the knowledge base.
        :param tags: Metadata that you can assign to a resource as key-value pairs. For more information, see the following resources:. - `Tag naming limits and requirements <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-conventions>`_ - `Tagging best practices <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-best-practices>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ef81b8dcbedbd76b5a39a6fd5a967ba49aa887b63aad45e2bc246c96c7abcec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnKnowledgeBaseProps(
            knowledge_base_configuration=knowledge_base_configuration,
            name=name,
            role_arn=role_arn,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4bc276c76fa89d7e7e13dc3bbd6542bf9248bddf93da183855dfef109357e1)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3c6a8c48301959ccf4c8e325f203936e57edbf8199458a5d3f47355924370f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The time at which the knowledge base was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrFailureReasons")
    def attr_failure_reasons(self) -> typing.List[builtins.str]:
        '''A list of reasons that the API operation on the knowledge base failed.

        :cloudformationAttribute: FailureReasons
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrFailureReasons"))

    @builtins.property
    @jsii.member(jsii_name="attrKnowledgeBaseArn")
    def attr_knowledge_base_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the knowledge base.

        :cloudformationAttribute: KnowledgeBaseArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrKnowledgeBaseArn"))

    @builtins.property
    @jsii.member(jsii_name="attrKnowledgeBaseId")
    def attr_knowledge_base_id(self) -> builtins.str:
        '''The unique identifier of the knowledge base.

        :cloudformationAttribute: KnowledgeBaseId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrKnowledgeBaseId"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the knowledge base.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The time at which the knowledge base was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> _TagManager_0a598cb3:
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseConfiguration")
    def knowledge_base_configuration(
        self,
    ) -> typing.Union[_IResolvable_da3f097b, "CfnKnowledgeBase.KnowledgeBaseConfigurationProperty"]:
        '''Contains details about the embeddings configuration of the knowledge base.'''
        return typing.cast(typing.Union[_IResolvable_da3f097b, "CfnKnowledgeBase.KnowledgeBaseConfigurationProperty"], jsii.get(self, "knowledgeBaseConfiguration"))

    @knowledge_base_configuration.setter
    def knowledge_base_configuration(
        self,
        value: typing.Union[_IResolvable_da3f097b, "CfnKnowledgeBase.KnowledgeBaseConfigurationProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc53309d6eb9442404b7a33330dfd3740f0c9d24afff9f19814de1a0a0e51d32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "knowledgeBaseConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the knowledge base.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ce011ed3a47084236afba28b5e5d0da34db483b792c0f0dd621b409474b6fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM role with permissions to invoke API operations on the knowledge base.'''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6281f2d1ed9a2f71b02754159fe6b2d8c70d3527e97d2d060434dc3483f2ad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the knowledge base.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fef7f262d2bad58c7f37c90b8756dd028b772a93aa036a4caf0c9565a7fff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata that you can assign to a resource as key-value pairs.

        For more information, see the following resources:.
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aaa5f9544be44cbc2ddb7d96026222438266e370aa05113a01af8f251b7286f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnKnowledgeBase.KnowledgeBaseConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "vector_knowledge_base_configuration": "vectorKnowledgeBaseConfiguration",
        },
    )
    class KnowledgeBaseConfigurationProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            vector_knowledge_base_configuration: typing.Union[_IResolvable_da3f097b, typing.Union["CfnKnowledgeBase.VectorKnowledgeBaseConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Contains details about the embeddings configuration of the knowledge base.

            :param type: The type of data that the data source is converted into for the knowledge base.
            :param vector_knowledge_base_configuration: Contains details about the embeddings model that'sused to convert the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-knowledgebase-knowledgebaseconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                knowledge_base_configuration_property = bedrock.CfnKnowledgeBase.KnowledgeBaseConfigurationProperty(
                    type="type",
                    vector_knowledge_base_configuration=bedrock.CfnKnowledgeBase.VectorKnowledgeBaseConfigurationProperty(
                        embedding_model_arn="embeddingModelArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f2ca26f28cc4cf3a289e62f58643faf6a7d98ea3e55e7ff4f0f77530fa0294b4)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument vector_knowledge_base_configuration", value=vector_knowledge_base_configuration, expected_type=type_hints["vector_knowledge_base_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
                "vector_knowledge_base_configuration": vector_knowledge_base_configuration,
            }

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of data that the data source is converted into for the knowledge base.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-knowledgebase-knowledgebaseconfiguration.html#cfn-bedrock-knowledgebase-knowledgebaseconfiguration-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def vector_knowledge_base_configuration(
            self,
        ) -> typing.Union[_IResolvable_da3f097b, "CfnKnowledgeBase.VectorKnowledgeBaseConfigurationProperty"]:
            '''Contains details about the embeddings model that'sused to convert the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-knowledgebase-knowledgebaseconfiguration.html#cfn-bedrock-knowledgebase-knowledgebaseconfiguration-vectorknowledgebaseconfiguration
            '''
            result = self._values.get("vector_knowledge_base_configuration")
            assert result is not None, "Required property 'vector_knowledge_base_configuration' is missing"
            return typing.cast(typing.Union[_IResolvable_da3f097b, "CfnKnowledgeBase.VectorKnowledgeBaseConfigurationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KnowledgeBaseConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_bedrock.CfnKnowledgeBase.VectorKnowledgeBaseConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"embedding_model_arn": "embeddingModelArn"},
    )
    class VectorKnowledgeBaseConfigurationProperty:
        def __init__(self, *, embedding_model_arn: builtins.str) -> None:
            '''Contains details about the model used to create vector embeddings for the knowledge base.

            :param embedding_model_arn: The Amazon Resource Name (ARN) of the model used to create vector embeddings for the knowledge base.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-knowledgebase-vectorknowledgebaseconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_bedrock as bedrock
                
                vector_knowledge_base_configuration_property = bedrock.CfnKnowledgeBase.VectorKnowledgeBaseConfigurationProperty(
                    embedding_model_arn="embeddingModelArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__53b08e209954b21c35b746e5eee517d51370af30630f5f17b3e5435150898236)
                check_type(argname="argument embedding_model_arn", value=embedding_model_arn, expected_type=type_hints["embedding_model_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "embedding_model_arn": embedding_model_arn,
            }

        @builtins.property
        def embedding_model_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the model used to create vector embeddings for the knowledge base.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bedrock-knowledgebase-vectorknowledgebaseconfiguration.html#cfn-bedrock-knowledgebase-vectorknowledgebaseconfiguration-embeddingmodelarn
            '''
            result = self._values.get("embedding_model_arn")
            assert result is not None, "Required property 'embedding_model_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VectorKnowledgeBaseConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_bedrock.CfnKnowledgeBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "knowledge_base_configuration": "knowledgeBaseConfiguration",
        "name": "name",
        "role_arn": "roleArn",
        "description": "description",
        "tags": "tags",
    },
)
class CfnKnowledgeBaseProps:
    def __init__(
        self,
        *,
        knowledge_base_configuration: typing.Union[_IResolvable_da3f097b, typing.Union[CfnKnowledgeBase.KnowledgeBaseConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
        name: builtins.str,
        role_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnKnowledgeBase``.

        :param knowledge_base_configuration: Contains details about the embeddings configuration of the knowledge base.
        :param name: The name of the knowledge base.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role with permissions to invoke API operations on the knowledge base.
        :param description: The description of the knowledge base.
        :param tags: Metadata that you can assign to a resource as key-value pairs. For more information, see the following resources:. - `Tag naming limits and requirements <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-conventions>`_ - `Tagging best practices <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-best-practices>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-knowledgebase.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_bedrock as bedrock
            
            cfn_knowledge_base_props = bedrock.CfnKnowledgeBaseProps(
                knowledge_base_configuration=bedrock.CfnKnowledgeBase.KnowledgeBaseConfigurationProperty(
                    type="type",
                    vector_knowledge_base_configuration=bedrock.CfnKnowledgeBase.VectorKnowledgeBaseConfigurationProperty(
                        embedding_model_arn="embeddingModelArn"
                    )
                ),
                name="name",
                role_arn="roleArn",
            
                # the properties below are optional
                description="description",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f6560ff734e79a877ac4cd934408cd79b9c6a6c1dac195972f27ac455fce2f)
            check_type(argname="argument knowledge_base_configuration", value=knowledge_base_configuration, expected_type=type_hints["knowledge_base_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "knowledge_base_configuration": knowledge_base_configuration,
            "name": name,
            "role_arn": role_arn,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def knowledge_base_configuration(
        self,
    ) -> typing.Union[_IResolvable_da3f097b, CfnKnowledgeBase.KnowledgeBaseConfigurationProperty]:
        '''Contains details about the embeddings configuration of the knowledge base.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-knowledgebase.html#cfn-bedrock-knowledgebase-knowledgebaseconfiguration
        '''
        result = self._values.get("knowledge_base_configuration")
        assert result is not None, "Required property 'knowledge_base_configuration' is missing"
        return typing.cast(typing.Union[_IResolvable_da3f097b, CfnKnowledgeBase.KnowledgeBaseConfigurationProperty], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the knowledge base.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-knowledgebase.html#cfn-bedrock-knowledgebase-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM role with permissions to invoke API operations on the knowledge base.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-knowledgebase.html#cfn-bedrock-knowledgebase-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the knowledge base.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-knowledgebase.html#cfn-bedrock-knowledgebase-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata that you can assign to a resource as key-value pairs. For more information, see the following resources:.

        - `Tag naming limits and requirements <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-conventions>`_
        - `Tagging best practices <https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html#tag-best-practices>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bedrock-knowledgebase.html#cfn-bedrock-knowledgebase-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnKnowledgeBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FoundationModelIdentifier(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_bedrock.FoundationModelIdentifier",
):
    '''The model identifiers for the Bedrock base foundation models.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_bedrock as bedrock
        
        
        bedrock.FoundationModel.from_foundation_model_id(self, "Model", bedrock.FoundationModelIdentifier.ANTHROPIC_CLAUDE_V2)
    '''

    def __init__(self, model_id: builtins.str) -> None:
        '''Constructor for foundation model identifier.

        :param model_id: the model identifier.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f232d69e34e8936af6b25fbb89b759790a47e68b671d931582f63554dd4bae52)
            check_type(argname="argument model_id", value=model_id, expected_type=type_hints["model_id"])
        jsii.create(self.__class__, self, [model_id])

    @jsii.python.classproperty
    @jsii.member(jsii_name="AI21_J2_GRANDE_INSTRUCT")
    def AI21_J2_GRANDE_INSTRUCT(cls) -> "FoundationModelIdentifier":
        '''Base model "ai21.j2-grande-instruct".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AI21_J2_GRANDE_INSTRUCT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AI21_J2_JUMBO_INSTRUCT")
    def AI21_J2_JUMBO_INSTRUCT(cls) -> "FoundationModelIdentifier":
        '''Base model "ai21.j2-jumbo-instruct".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AI21_J2_JUMBO_INSTRUCT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AI21_J2_MID")
    def AI21_J2_MID(cls) -> "FoundationModelIdentifier":
        '''Base model "ai21.j2-mid".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AI21_J2_MID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AI21_J2_ULTRA")
    def AI21_J2_ULTRA(cls) -> "FoundationModelIdentifier":
        '''Base model "ai21.j2-ultra".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AI21_J2_ULTRA"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AI21_LABS_JURASSIC_2_MID_V1")
    def AI21_LABS_JURASSIC_2_MID_V1(cls) -> "FoundationModelIdentifier":
        '''Base model "ai21.j2-mid-v1".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AI21_LABS_JURASSIC_2_MID_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AI21_LABS_JURASSIC_2_ULTRA_V1")
    def AI21_LABS_JURASSIC_2_ULTRA_V1(cls) -> "FoundationModelIdentifier":
        '''Base model "ai21.j2-ultra-v1".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AI21_LABS_JURASSIC_2_ULTRA_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_EMBED_G1_TEXT_02")
    def AMAZON_TITAN_EMBED_G1_TEXT_02(cls) -> "FoundationModelIdentifier":
        '''Base model "amazon.titan-embed-g1-text-02".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AMAZON_TITAN_EMBED_G1_TEXT_02"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_EMBED_IMAGE_V1_0")
    def AMAZON_TITAN_EMBED_IMAGE_V1_0(cls) -> "FoundationModelIdentifier":
        '''Base model "amazon.titan-embed-image-v1:0".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AMAZON_TITAN_EMBED_IMAGE_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_EMBED_TEXT_V1_2_8K")
    def AMAZON_TITAN_EMBED_TEXT_V1_2_8_K(cls) -> "FoundationModelIdentifier":
        '''Base model "amazon.titan-embed-text-v1:2:8k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AMAZON_TITAN_EMBED_TEXT_V1_2_8K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_EMBEDDINGS_G1_TEXT_V1")
    def AMAZON_TITAN_EMBEDDINGS_G1_TEXT_V1(cls) -> "FoundationModelIdentifier":
        '''Base model "amazon.titan-embed-text-v1".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AMAZON_TITAN_EMBEDDINGS_G1_TEXT_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_IMAGE_GENERATOR_G1_V1")
    def AMAZON_TITAN_IMAGE_GENERATOR_G1_V1(cls) -> "FoundationModelIdentifier":
        '''Base model "amazon.titan-image-generator-v1".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AMAZON_TITAN_IMAGE_GENERATOR_G1_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_IMAGE_GENERATOR_V1_0")
    def AMAZON_TITAN_IMAGE_GENERATOR_V1_0(cls) -> "FoundationModelIdentifier":
        '''Base model "amazon.titan-image-generator-v1:0".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AMAZON_TITAN_IMAGE_GENERATOR_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_MULTIMODAL_EMBEDDINGS_G1_V1")
    def AMAZON_TITAN_MULTIMODAL_EMBEDDINGS_G1_V1(cls) -> "FoundationModelIdentifier":
        '''Base model "amazon.titan-embed-image-v1".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AMAZON_TITAN_MULTIMODAL_EMBEDDINGS_G1_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_TEXT_EXPRESS_V1_0_8K")
    def AMAZON_TITAN_TEXT_EXPRESS_V1_0_8_K(cls) -> "FoundationModelIdentifier":
        '''Base model "amazon.titan-text-express-v1:0:8k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AMAZON_TITAN_TEXT_EXPRESS_V1_0_8K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_TEXT_G1_EXPRESS_V1")
    def AMAZON_TITAN_TEXT_G1_EXPRESS_V1(cls) -> "FoundationModelIdentifier":
        '''Base model "amazon.titan-text-express-v1".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AMAZON_TITAN_TEXT_G1_EXPRESS_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_TEXT_LITE_V1")
    def AMAZON_TITAN_TEXT_LITE_V1(cls) -> "FoundationModelIdentifier":
        '''Base model "amazon.titan-text-lite-v1".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AMAZON_TITAN_TEXT_LITE_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_TEXT_LITE_V1_0_4K")
    def AMAZON_TITAN_TEXT_LITE_V1_0_4_K(cls) -> "FoundationModelIdentifier":
        '''Base model "amazon.titan-text-lite-v1:0:4k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AMAZON_TITAN_TEXT_LITE_V1_0_4K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_TG1_LARGE")
    def AMAZON_TITAN_TG1_LARGE(cls) -> "FoundationModelIdentifier":
        '''Base model "amazon.titan-tg1-large".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "AMAZON_TITAN_TG1_LARGE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_HAIKU_20240307_V1_0")
    def ANTHROPIC_CLAUDE_3_HAIKU_20240307_V1_0(cls) -> "FoundationModelIdentifier":
        '''Base model "anthropic.claude-3-haiku-20240307-v1:0".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_3_HAIKU_20240307_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_HAIKU_20240307_V1_0_200K")
    def ANTHROPIC_CLAUDE_3_HAIKU_20240307_V1_0_200_K(
        cls,
    ) -> "FoundationModelIdentifier":
        '''Base model "anthropic.claude-3-haiku-20240307-v1:0:200k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_3_HAIKU_20240307_V1_0_200K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_HAIKU_20240307_V1_0_48K")
    def ANTHROPIC_CLAUDE_3_HAIKU_20240307_V1_0_48_K(cls) -> "FoundationModelIdentifier":
        '''Base model "anthropic.claude-3-haiku-20240307-v1:0:48k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_3_HAIKU_20240307_V1_0_48K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_OPUS_20240229_V1_0")
    def ANTHROPIC_CLAUDE_3_OPUS_20240229_V1_0(cls) -> "FoundationModelIdentifier":
        '''Base model "anthropic.claude-3-opus-20240229-v1:0".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_3_OPUS_20240229_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_SONNET_20240229_V1_0")
    def ANTHROPIC_CLAUDE_3_SONNET_20240229_V1_0(cls) -> "FoundationModelIdentifier":
        '''Base model "anthropic.claude-3-sonnet-20240229-v1:0".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_3_SONNET_20240229_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_SONNET_20240229_V1_0_200K")
    def ANTHROPIC_CLAUDE_3_SONNET_20240229_V1_0_200_K(
        cls,
    ) -> "FoundationModelIdentifier":
        '''Base model "anthropic.claude-3-sonnet-20240229-v1:0:200k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_3_SONNET_20240229_V1_0_200K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_3_SONNET_20240229_V1_0_28K")
    def ANTHROPIC_CLAUDE_3_SONNET_20240229_V1_0_28_K(
        cls,
    ) -> "FoundationModelIdentifier":
        '''Base model "anthropic.claude-3-sonnet-20240229-v1:0:28k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_3_SONNET_20240229_V1_0_28K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_INSTANT_V1")
    def ANTHROPIC_CLAUDE_INSTANT_V1(cls) -> "FoundationModelIdentifier":
        '''Base model "anthropic.claude-instant-v1".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_INSTANT_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_INSTANT_V1_2_100K")
    def ANTHROPIC_CLAUDE_INSTANT_V1_2_100_K(cls) -> "FoundationModelIdentifier":
        '''Base model "anthropic.claude-instant-v1:2:100k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_INSTANT_V1_2_100K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_V1")
    def ANTHROPIC_CLAUDE_V1(cls) -> "FoundationModelIdentifier":
        '''(deprecated) Base model "anthropic.claude-v1".

        :deprecated: use latest version of the model

        :stability: deprecated
        '''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_V2")
    def ANTHROPIC_CLAUDE_V2(cls) -> "FoundationModelIdentifier":
        '''Base model "anthropic.claude-v2".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_V2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_V2_0_100K")
    def ANTHROPIC_CLAUDE_V2_0_100_K(cls) -> "FoundationModelIdentifier":
        '''Base model "anthropic.claude-v2:0:100k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_V2_0_100K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_V2_0_18K")
    def ANTHROPIC_CLAUDE_V2_0_18_K(cls) -> "FoundationModelIdentifier":
        '''Base model "anthropic.claude-v2:0:18k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_V2_0_18K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_V2_1")
    def ANTHROPIC_CLAUDE_V2_1(cls) -> "FoundationModelIdentifier":
        '''Base model "anthropic.claude-v2:1".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_V2_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_V2_1_18K")
    def ANTHROPIC_CLAUDE_V2_1_18_K(cls) -> "FoundationModelIdentifier":
        '''Base model "anthropic.claude-v2:1:18k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_V2_1_18K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_V2_1_200K")
    def ANTHROPIC_CLAUDE_V2_1_200_K(cls) -> "FoundationModelIdentifier":
        '''Base model "anthropic.claude-v2:1:200k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "ANTHROPIC_CLAUDE_V2_1_200K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="COHERE_COMMAND_LIGHT_TEXT_V14_7_4K")
    def COHERE_COMMAND_LIGHT_TEXT_V14_7_4_K(cls) -> "FoundationModelIdentifier":
        '''Base model "cohere.command-light-text-v14:7:4k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "COHERE_COMMAND_LIGHT_TEXT_V14_7_4K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="COHERE_COMMAND_LIGHT_V14")
    def COHERE_COMMAND_LIGHT_V14(cls) -> "FoundationModelIdentifier":
        '''Base model "cohere.command-light-text-v14".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "COHERE_COMMAND_LIGHT_V14"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="COHERE_COMMAND_TEXT_V14_7_4K")
    def COHERE_COMMAND_TEXT_V14_7_4_K(cls) -> "FoundationModelIdentifier":
        '''Base model "cohere.command-text-v14:7:4k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "COHERE_COMMAND_TEXT_V14_7_4K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="COHERE_COMMAND_V14")
    def COHERE_COMMAND_V14(cls) -> "FoundationModelIdentifier":
        '''Base model "cohere.command-text-v14".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "COHERE_COMMAND_V14"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="COHERE_EMBED_ENGLISH_V3")
    def COHERE_EMBED_ENGLISH_V3(cls) -> "FoundationModelIdentifier":
        '''Base model "cohere.embed-english-v3".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "COHERE_EMBED_ENGLISH_V3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="COHERE_EMBED_MULTILINGUAL_V3")
    def COHERE_EMBED_MULTILINGUAL_V3(cls) -> "FoundationModelIdentifier":
        '''Base model "cohere.embed-multilingual-v3".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "COHERE_EMBED_MULTILINGUAL_V3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_2_13B_CHAT_V1_0_4K")
    def META_LLAMA_2_13_B_CHAT_V1_0_4_K(cls) -> "FoundationModelIdentifier":
        '''Base model "meta.llama2-13b-chat-v1:0:4k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "META_LLAMA_2_13B_CHAT_V1_0_4K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_2_13B_V1")
    def META_LLAMA_2_13_B_V1(cls) -> "FoundationModelIdentifier":
        '''Base model "meta.llama2-13b-v1".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "META_LLAMA_2_13B_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_2_13B_V1_0_4K")
    def META_LLAMA_2_13_B_V1_0_4_K(cls) -> "FoundationModelIdentifier":
        '''Base model "meta.llama2-13b-v1:0:4k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "META_LLAMA_2_13B_V1_0_4K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_2_70B_CHAT_V1_0_4K")
    def META_LLAMA_2_70_B_CHAT_V1_0_4_K(cls) -> "FoundationModelIdentifier":
        '''Base model "meta.llama2-70b-chat-v1:0:4k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "META_LLAMA_2_70B_CHAT_V1_0_4K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_2_70B_V1")
    def META_LLAMA_2_70_B_V1(cls) -> "FoundationModelIdentifier":
        '''Base model "meta.llama2-70b-v1".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "META_LLAMA_2_70B_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_2_70B_V1_0_4K")
    def META_LLAMA_2_70_B_V1_0_4_K(cls) -> "FoundationModelIdentifier":
        '''Base model "meta.llama2-70b-v1:0:4k".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "META_LLAMA_2_70B_V1_0_4K"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_2_CHAT_13B_V1")
    def META_LLAMA_2_CHAT_13_B_V1(cls) -> "FoundationModelIdentifier":
        '''Base model "meta.llama2-13b-chat-v1".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "META_LLAMA_2_CHAT_13B_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="META_LLAMA_2_CHAT_70B_V1")
    def META_LLAMA_2_CHAT_70_B_V1(cls) -> "FoundationModelIdentifier":
        '''Base model "meta.llama2-70b-chat-v1".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "META_LLAMA_2_CHAT_70B_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MISTRAL_MISTRAL_7B_INSTRUCT_V0_2")
    def MISTRAL_MISTRAL_7_B_INSTRUCT_V0_2(cls) -> "FoundationModelIdentifier":
        '''Base model "mistral.mistral-7b-instruct-v0:2".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "MISTRAL_MISTRAL_7B_INSTRUCT_V0_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MISTRAL_MIXTRAL_8X7B_INSTRUCT_V0_1")
    def MISTRAL_MIXTRAL_8_X7_B_INSTRUCT_V0_1(cls) -> "FoundationModelIdentifier":
        '''Base model "mistral.mixtral-8x7b-instruct-v0:1".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "MISTRAL_MIXTRAL_8X7B_INSTRUCT_V0_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="STABILITY_STABLE_DIFFUSION_XL")
    def STABILITY_STABLE_DIFFUSION_XL(cls) -> "FoundationModelIdentifier":
        '''(deprecated) Base model "stability.stable-diffusion-xl".

        :deprecated: use latest version of the model

        :stability: deprecated
        '''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "STABILITY_STABLE_DIFFUSION_XL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="STABILITY_STABLE_DIFFUSION_XL_V0")
    def STABILITY_STABLE_DIFFUSION_XL_V0(cls) -> "FoundationModelIdentifier":
        '''(deprecated) Base model "stability.stable-diffusion-xl-v0".

        :deprecated: use latest version of the model

        :stability: deprecated
        '''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "STABILITY_STABLE_DIFFUSION_XL_V0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="STABILITY_STABLE_DIFFUSION_XL_V1")
    def STABILITY_STABLE_DIFFUSION_XL_V1(cls) -> "FoundationModelIdentifier":
        '''Base model "stability.stable-diffusion-xl-v1".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "STABILITY_STABLE_DIFFUSION_XL_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="STABILITY_STABLE_DIFFUSION_XL_V1_0")
    def STABILITY_STABLE_DIFFUSION_XL_V1_0(cls) -> "FoundationModelIdentifier":
        '''Base model "stability.stable-diffusion-xl-v1:0".'''
        return typing.cast("FoundationModelIdentifier", jsii.sget(cls, "STABILITY_STABLE_DIFFUSION_XL_V1_0"))

    @builtins.property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> builtins.str:
        '''the model identifier.'''
        return typing.cast(builtins.str, jsii.get(self, "modelId"))


@jsii.interface(jsii_type="aws-cdk-lib.aws_bedrock.IModel")
class IModel(typing_extensions.Protocol):
    '''Represents a Bedrock model.

    The model could be a foundation model, a custom model, or a provisioned model.
    '''

    @builtins.property
    @jsii.member(jsii_name="modelArn")
    def model_arn(self) -> builtins.str:
        '''The ARN of the model.

        :see: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-actions-as-permissions
        '''
        ...


class _IModelProxy:
    '''Represents a Bedrock model.

    The model could be a foundation model, a custom model, or a provisioned model.
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_bedrock.IModel"

    @builtins.property
    @jsii.member(jsii_name="modelArn")
    def model_arn(self) -> builtins.str:
        '''The ARN of the model.

        :see: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrock.html#amazonbedrock-actions-as-permissions
        '''
        return typing.cast(builtins.str, jsii.get(self, "modelArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IModel).__jsii_proxy_class__ = lambda : _IModelProxy


@jsii.implements(IModel)
class ProvisionedModel(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_bedrock.ProvisionedModel",
):
    '''A Bedrock provisioned model.

    Note: CloudFormation does not currently support creating Bedrock Provisioned Throughput
    resources outside of a custom resource. You can import provisioned models created by
    provisioning throughput in Bedrock outside the CDK or via a custom resource with
    {@link ProvisionedModel#fromProvisionedModelArn }.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_bedrock as bedrock
        
        
        bedrock.ProvisionedModel.from_provisioned_model_arn(self, "Model", "arn:aws:bedrock:us-east-2:123456789012:provisioned-model/abc-123")
    '''

    @jsii.member(jsii_name="fromProvisionedModelArn")
    @builtins.classmethod
    def from_provisioned_model_arn(
        cls,
        _scope: _constructs_77d1e7e8.Construct,
        _id: builtins.str,
        provisioned_model_arn: builtins.str,
    ) -> IModel:
        '''Import an provisioned model given an ARN.

        :param _scope: -
        :param _id: -
        :param provisioned_model_arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__729a89649bbbe97643ef676e5c7a3debb583fa04ca31db203a85e9e6631bd8eb)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _id", value=_id, expected_type=type_hints["_id"])
            check_type(argname="argument provisioned_model_arn", value=provisioned_model_arn, expected_type=type_hints["provisioned_model_arn"])
        return typing.cast(IModel, jsii.sinvoke(cls, "fromProvisionedModelArn", [_scope, _id, provisioned_model_arn]))

    @builtins.property
    @jsii.member(jsii_name="modelArn")
    def model_arn(self) -> builtins.str:
        '''The ARN of the provisioned model.'''
        return typing.cast(builtins.str, jsii.get(self, "modelArn"))


@jsii.implements(IModel)
class FoundationModel(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_bedrock.FoundationModel",
):
    '''A Bedrock base foundation model.

    :see: https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_bedrock as bedrock
        
        
        bedrock.FoundationModel.from_foundation_model_id(self, "Model", bedrock.FoundationModelIdentifier.ANTHROPIC_CLAUDE_V2)
    '''

    @jsii.member(jsii_name="fromFoundationModelId")
    @builtins.classmethod
    def from_foundation_model_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        _id: builtins.str,
        foundation_model_id: FoundationModelIdentifier,
    ) -> "FoundationModel":
        '''Construct a Bedrock base foundation model given the model identifier.

        :param scope: The parent construct.
        :param _id: The name of the model construct.
        :param foundation_model_id: The model identifier such as 'amazon.titan-text-express-v1'.

        :return: A Bedrock base foundation model.

        :see: https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids-arns.html
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64541c2daf01636476388a49436a79864b7cc8c00bbbf47f4d0f84ccbf0ec56)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument _id", value=_id, expected_type=type_hints["_id"])
            check_type(argname="argument foundation_model_id", value=foundation_model_id, expected_type=type_hints["foundation_model_id"])
        return typing.cast("FoundationModel", jsii.sinvoke(cls, "fromFoundationModelId", [scope, _id, foundation_model_id]))

    @builtins.property
    @jsii.member(jsii_name="modelArn")
    def model_arn(self) -> builtins.str:
        '''The foundation model ARN.'''
        return typing.cast(builtins.str, jsii.get(self, "modelArn"))

    @builtins.property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> builtins.str:
        '''The foundation model ID.

        Example::

            "amazon.titan-text-express-v1"
        '''
        return typing.cast(builtins.str, jsii.get(self, "modelId"))


__all__ = [
    "CfnAgent",
    "CfnAgentAlias",
    "CfnAgentAliasProps",
    "CfnAgentProps",
    "CfnDataSource",
    "CfnDataSourceProps",
    "CfnKnowledgeBase",
    "CfnKnowledgeBaseProps",
    "FoundationModel",
    "FoundationModelIdentifier",
    "IModel",
    "ProvisionedModel",
]

publication.publish()

def _typecheckingstub__facaad57ffe16da42f099d2b7997f3e6fd3b9eba46fd226d8fb5afe286371e74(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    agent_name: builtins.str,
    action_groups: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgent.AgentActionGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    agent_resource_role_arn: typing.Optional[builtins.str] = None,
    auto_prepare: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    customer_encryption_key_arn: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    foundation_model: typing.Optional[builtins.str] = None,
    idle_session_ttl_in_seconds: typing.Optional[jsii.Number] = None,
    instruction: typing.Optional[builtins.str] = None,
    knowledge_bases: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgent.AgentKnowledgeBaseProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    prompt_override_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgent.PromptOverrideConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    skip_resource_in_use_check_on_delete: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c671dddc0216853bf62cdd51e6c2889b8dfe0d7819a455df2ad71c5b8d67daba(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0633cd876f44b7c72e1346d6b26f361a0d1afbb01604add4ba48210303ccc35c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c19306b2dfaafb18e03ff6cb134d14ba6e0563e4a2c79c53886ba8207714cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f670733e4a574d57292a648f4a8ad68ef64492d8f6667729aee160997a190e16(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, CfnAgent.AgentActionGroupProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b021046f759c8bbfbfb02bceb7d337926c83d3e866d3dcd420bb7819e254ca(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc98d7cbd7435359b362ef11a9b384386d54f878814d4c596d3dfa290281e67(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea763219d3fed10a3841f0a137399ddf8f575abf9b1691273415e66f4f0763c2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd6874957339badfe5e02e7733947f3ba0b1fdc8c597003bfe10fc7ff96c537(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75110aa6cf6cc2a463a78a36e9a6327c59875b1ef94d53da3047b8ec62c79fd4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29f42af6a8bf7aee6adb6b35e7809da69175082446368854bd402491896a71f(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c531a159f9cc0e23a07b5bc12cf53006e4207dd460e3ce580c57fa76109e86(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8842d93181ada69f14f22e8ff6855e528b858dd0baf705a1ae228b3d96ef38d6(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, CfnAgent.AgentKnowledgeBaseProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d115c78c31e0cc4b4828b953c3afd44f4b9271c4e3aaad46777846216d6e9b8(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, CfnAgent.PromptOverrideConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f4401bf1c7d6b30870233c265d99a973b05e80ad9e53ab7945a82208a3bf49(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e79489cae3525b40539f62fddb8a1f8b194bc0b1d166146c12f85a52d978be(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__537a89983eef4dfdf436d52865dbd27f462f778f0de6c8ec6162918153faf331(
    *,
    payload: typing.Optional[builtins.str] = None,
    s3: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgent.S3IdentifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e0c43d5a1e3dda92d710404aea51beb5f30a149322d9ec3e8d354b889735eb(
    *,
    lambda_: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb9c2568194cbbe9c081f2a8339eaee9966d82b8c5c5ffbc732275ef4a1b76a(
    *,
    action_group_name: builtins.str,
    action_group_executor: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgent.ActionGroupExecutorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    action_group_state: typing.Optional[builtins.str] = None,
    api_schema: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgent.APISchemaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    parent_action_group_signature: typing.Optional[builtins.str] = None,
    skip_resource_in_use_check_on_delete: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f582a007ade3e95453c6c5cd09673a7089ab2673014cc97bc0c1eee1d85391(
    *,
    description: builtins.str,
    knowledge_base_id: builtins.str,
    knowledge_base_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8b0e306d1a46c4fdcedd77b9e6caf3ca221fe8133fe3ce29c1e5e779cc3189(
    *,
    maximum_length: typing.Optional[jsii.Number] = None,
    stop_sequences: typing.Optional[typing.Sequence[builtins.str]] = None,
    temperature: typing.Optional[jsii.Number] = None,
    top_k: typing.Optional[jsii.Number] = None,
    top_p: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072678823f2b5bb708860fe2f54d37c6a24153ba05ec6c798f1cbb1222e7cd7b(
    *,
    base_prompt_template: typing.Optional[builtins.str] = None,
    inference_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgent.InferenceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parser_mode: typing.Optional[builtins.str] = None,
    prompt_creation_mode: typing.Optional[builtins.str] = None,
    prompt_state: typing.Optional[builtins.str] = None,
    prompt_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a38248b49cbea1e103efe955cc12c1bd5e500b242bd9490c1c81253830d77d(
    *,
    prompt_configurations: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgent.PromptConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]],
    override_lambda: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9a91ab9025dd36217ed95088c50220259ce5115620391445737700490cba60(
    *,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    s3_object_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8230a990c5fac91dc09e3de4211aa6f82fce95537f199a7987ca92f4722ee0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    agent_alias_name: builtins.str,
    agent_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    routing_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881be8885c059b078e3110beb1aed396db2ce3f0505bec32be8cedeba399356d(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7100eb19771c4ffaea3a7323fe3cb5fcb6702a3fa7fdaf66bc8a4db1eae875c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4929f9d1fe1c750108b588135fd2420ee93abad44713bd60a4f90bf0bab64e78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10c310fa33a8cb7b52c456850e88b42ea1b312acb49b915241cc6f52ef15136(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ab6386ae765e3eaf37d16d7a5314cdca1d8b60ea095a4fa303d13c84722e78(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca75abf30c6951a069bde3673588677ff723ad86067bf5365bb584482bed50a8(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[_IResolvable_da3f097b, CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf90503b3b2050ab4f0f6ba0bf057a037193369214d4f027b567d3062bda19b8(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4220f7b3bb12c49a75057af394368ca2d4de63c53d832e73767eb01f3bccb2ce(
    *,
    end_date: typing.Optional[builtins.str] = None,
    routing_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    start_date: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846d3bcc8614fd45d175f992a20505b220910c107392df0930556bb43637fc79(
    *,
    agent_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3144a1c66c11b4a2b15be859f361c848648aefb3df04b8fce2befe94f215c68(
    *,
    agent_alias_name: builtins.str,
    agent_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    routing_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgentAlias.AgentAliasRoutingConfigurationListItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4f714080f6d4f9b0a3fe85a8425a8ba69698695e35d6fbd9d710ca5d99ba6e8(
    *,
    agent_name: builtins.str,
    action_groups: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgent.AgentActionGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    agent_resource_role_arn: typing.Optional[builtins.str] = None,
    auto_prepare: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    customer_encryption_key_arn: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    foundation_model: typing.Optional[builtins.str] = None,
    idle_session_ttl_in_seconds: typing.Optional[jsii.Number] = None,
    instruction: typing.Optional[builtins.str] = None,
    knowledge_bases: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgent.AgentKnowledgeBaseProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    prompt_override_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnAgent.PromptOverrideConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    skip_resource_in_use_check_on_delete: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6230da788965416b3262c41917eaab2193b3cfccf7a03f313a8c19186a6b75(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    data_source_configuration: typing.Union[_IResolvable_da3f097b, typing.Union[CfnDataSource.DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    knowledge_base_id: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnDataSource.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vector_ingestion_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnDataSource.VectorIngestionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68a33df1c2e42bd5580cdec505e709cbe6a0663b8142f6fb3ba8e70911ceb85(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b23978dd788bb65ad2e2571764c987a4729f9d5c9d17c903f53a10cd4e3ad3e7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a387108ccda2b96813f79478d4429abb297f766ce080c3bf9b77d03af3db534c(
    value: typing.Union[_IResolvable_da3f097b, CfnDataSource.DataSourceConfigurationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d585d364d6684899cbce3ae80a62858e2f256e166c889705e2ecb2040e935d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99613771dd63beb77d047c2f17b9362e99ec38dd6fb89ec0c78f690f7847fc0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc31b7620f239d59ff8a40cb711119c09cf659e115e22ba5d86a3d2a36aa17b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe19aafcbb9637979bddaf7a230433b26f791bb09744dabcf0e95496322565d(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, CfnDataSource.ServerSideEncryptionConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__033990e14b671fe96b02a12658cd4beadf8bae975b4e0c94984d3e41913522c8(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, CfnDataSource.VectorIngestionConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8beec747a0f57f641fd4bd3b03f73b678c8e286785d948f80998682f0c0a40e5(
    *,
    chunking_strategy: builtins.str,
    fixed_size_chunking_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnDataSource.FixedSizeChunkingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e1b0c807d6904904c91cc13a2f47ee5db24090758446e26a864b57b3d36117(
    *,
    s3_configuration: typing.Union[_IResolvable_da3f097b, typing.Union[CfnDataSource.S3DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b9e8054cbf79d2292e738f1061947914954b89440b15bf572c87c9695aaf7bc(
    *,
    max_tokens: jsii.Number,
    overlap_percentage: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4929296343a5ea55bce5d28d11b34fa10885df35596a08102658f8bcbc8c5b(
    *,
    bucket_arn: builtins.str,
    inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7bf662e3d628b0671b547dd26face3c322a93684b4b5578ec4cda1099b30e6a(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37255db3e7cacfdeadc2d28bfe7938fd13ab4a2cd72190024a531eddf1fd9ec0(
    *,
    chunking_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnDataSource.ChunkingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4beca3e3b31c91619a3fa9da2bf185ffd738124b7965f1c90a191b43c7b62664(
    *,
    data_source_configuration: typing.Union[_IResolvable_da3f097b, typing.Union[CfnDataSource.DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    knowledge_base_id: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnDataSource.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vector_ingestion_configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Union[CfnDataSource.VectorIngestionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef81b8dcbedbd76b5a39a6fd5a967ba49aa887b63aad45e2bc246c96c7abcec(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    knowledge_base_configuration: typing.Union[_IResolvable_da3f097b, typing.Union[CfnKnowledgeBase.KnowledgeBaseConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    name: builtins.str,
    role_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4bc276c76fa89d7e7e13dc3bbd6542bf9248bddf93da183855dfef109357e1(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3c6a8c48301959ccf4c8e325f203936e57edbf8199458a5d3f47355924370f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc53309d6eb9442404b7a33330dfd3740f0c9d24afff9f19814de1a0a0e51d32(
    value: typing.Union[_IResolvable_da3f097b, CfnKnowledgeBase.KnowledgeBaseConfigurationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ce011ed3a47084236afba28b5e5d0da34db483b792c0f0dd621b409474b6fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6281f2d1ed9a2f71b02754159fe6b2d8c70d3527e97d2d060434dc3483f2ad5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fef7f262d2bad58c7f37c90b8756dd028b772a93aa036a4caf0c9565a7fff1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aaa5f9544be44cbc2ddb7d96026222438266e370aa05113a01af8f251b7286f(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ca26f28cc4cf3a289e62f58643faf6a7d98ea3e55e7ff4f0f77530fa0294b4(
    *,
    type: builtins.str,
    vector_knowledge_base_configuration: typing.Union[_IResolvable_da3f097b, typing.Union[CfnKnowledgeBase.VectorKnowledgeBaseConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b08e209954b21c35b746e5eee517d51370af30630f5f17b3e5435150898236(
    *,
    embedding_model_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f6560ff734e79a877ac4cd934408cd79b9c6a6c1dac195972f27ac455fce2f(
    *,
    knowledge_base_configuration: typing.Union[_IResolvable_da3f097b, typing.Union[CfnKnowledgeBase.KnowledgeBaseConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    name: builtins.str,
    role_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f232d69e34e8936af6b25fbb89b759790a47e68b671d931582f63554dd4bae52(
    model_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729a89649bbbe97643ef676e5c7a3debb583fa04ca31db203a85e9e6631bd8eb(
    _scope: _constructs_77d1e7e8.Construct,
    _id: builtins.str,
    provisioned_model_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64541c2daf01636476388a49436a79864b7cc8c00bbbf47f4d0f84ccbf0ec56(
    scope: _constructs_77d1e7e8.Construct,
    _id: builtins.str,
    foundation_model_id: FoundationModelIdentifier,
) -> None:
    """Type checking stubs"""
    pass
