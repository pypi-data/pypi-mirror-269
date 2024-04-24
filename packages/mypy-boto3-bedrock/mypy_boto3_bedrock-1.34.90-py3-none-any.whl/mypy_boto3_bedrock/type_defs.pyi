"""
Type annotations for bedrock service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock/type_defs/)

Usage::

    ```python
    from mypy_boto3_bedrock.type_defs import S3ConfigTypeDef

    data: S3ConfigTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    CommitmentDurationType,
    CustomizationTypeType,
    EvaluationJobStatusType,
    EvaluationJobTypeType,
    EvaluationTaskTypeType,
    FineTuningJobStatusType,
    FoundationModelLifecycleStatusType,
    GuardrailContentFilterTypeType,
    GuardrailFilterStrengthType,
    GuardrailPiiEntityTypeType,
    GuardrailSensitiveInformationActionType,
    GuardrailStatusType,
    InferenceTypeType,
    ModelCustomizationJobStatusType,
    ModelCustomizationType,
    ModelModalityType,
    ProvisionedModelStatusType,
    SortOrderType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "S3ConfigTypeDef",
    "EvaluationOutputDataConfigTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "CreateGuardrailVersionRequestRequestTypeDef",
    "OutputDataConfigTypeDef",
    "TrainingDataConfigTypeDef",
    "VpcConfigTypeDef",
    "CustomModelSummaryTypeDef",
    "DeleteCustomModelRequestRequestTypeDef",
    "DeleteGuardrailRequestRequestTypeDef",
    "DeleteProvisionedModelThroughputRequestRequestTypeDef",
    "EvaluationBedrockModelTypeDef",
    "EvaluationDatasetLocationTypeDef",
    "EvaluationSummaryTypeDef",
    "FoundationModelLifecycleTypeDef",
    "GetCustomModelRequestRequestTypeDef",
    "TrainingMetricsTypeDef",
    "ValidatorMetricTypeDef",
    "GetEvaluationJobRequestRequestTypeDef",
    "GetFoundationModelRequestRequestTypeDef",
    "GetGuardrailRequestRequestTypeDef",
    "GetModelCustomizationJobRequestRequestTypeDef",
    "GetProvisionedModelThroughputRequestRequestTypeDef",
    "GuardrailContentFilterConfigTypeDef",
    "GuardrailContentFilterTypeDef",
    "GuardrailManagedWordsConfigTypeDef",
    "GuardrailManagedWordsTypeDef",
    "GuardrailPiiEntityConfigTypeDef",
    "GuardrailPiiEntityTypeDef",
    "GuardrailRegexConfigTypeDef",
    "GuardrailRegexTypeDef",
    "GuardrailSummaryTypeDef",
    "GuardrailTopicConfigTypeDef",
    "GuardrailTopicTypeDef",
    "GuardrailWordConfigTypeDef",
    "GuardrailWordTypeDef",
    "HumanEvaluationCustomMetricTypeDef",
    "HumanWorkflowConfigTypeDef",
    "PaginatorConfigTypeDef",
    "TimestampTypeDef",
    "ListFoundationModelsRequestRequestTypeDef",
    "ListGuardrailsRequestRequestTypeDef",
    "ModelCustomizationJobSummaryTypeDef",
    "ProvisionedModelSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "StopEvaluationJobRequestRequestTypeDef",
    "StopModelCustomizationJobRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateProvisionedModelThroughputRequestRequestTypeDef",
    "ValidatorTypeDef",
    "CloudWatchConfigTypeDef",
    "CreateProvisionedModelThroughputRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateEvaluationJobResponseTypeDef",
    "CreateGuardrailResponseTypeDef",
    "CreateGuardrailVersionResponseTypeDef",
    "CreateModelCustomizationJobResponseTypeDef",
    "CreateProvisionedModelThroughputResponseTypeDef",
    "GetProvisionedModelThroughputResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateGuardrailResponseTypeDef",
    "ListCustomModelsResponseTypeDef",
    "EvaluationModelConfigTypeDef",
    "EvaluationDatasetTypeDef",
    "ListEvaluationJobsResponseTypeDef",
    "FoundationModelDetailsTypeDef",
    "FoundationModelSummaryTypeDef",
    "GuardrailContentPolicyConfigTypeDef",
    "GuardrailContentPolicyTypeDef",
    "GuardrailSensitiveInformationPolicyConfigTypeDef",
    "GuardrailSensitiveInformationPolicyTypeDef",
    "ListGuardrailsResponseTypeDef",
    "GuardrailTopicPolicyConfigTypeDef",
    "GuardrailTopicPolicyTypeDef",
    "GuardrailWordPolicyConfigTypeDef",
    "GuardrailWordPolicyTypeDef",
    "ListGuardrailsRequestListGuardrailsPaginateTypeDef",
    "ListCustomModelsRequestListCustomModelsPaginateTypeDef",
    "ListCustomModelsRequestRequestTypeDef",
    "ListEvaluationJobsRequestListEvaluationJobsPaginateTypeDef",
    "ListEvaluationJobsRequestRequestTypeDef",
    "ListModelCustomizationJobsRequestListModelCustomizationJobsPaginateTypeDef",
    "ListModelCustomizationJobsRequestRequestTypeDef",
    "ListProvisionedModelThroughputsRequestListProvisionedModelThroughputsPaginateTypeDef",
    "ListProvisionedModelThroughputsRequestRequestTypeDef",
    "ListModelCustomizationJobsResponseTypeDef",
    "ListProvisionedModelThroughputsResponseTypeDef",
    "ValidationDataConfigTypeDef",
    "LoggingConfigTypeDef",
    "EvaluationInferenceConfigTypeDef",
    "EvaluationDatasetMetricConfigTypeDef",
    "GetFoundationModelResponseTypeDef",
    "ListFoundationModelsResponseTypeDef",
    "CreateGuardrailRequestRequestTypeDef",
    "UpdateGuardrailRequestRequestTypeDef",
    "GetGuardrailResponseTypeDef",
    "CreateModelCustomizationJobRequestRequestTypeDef",
    "GetCustomModelResponseTypeDef",
    "GetModelCustomizationJobResponseTypeDef",
    "GetModelInvocationLoggingConfigurationResponseTypeDef",
    "PutModelInvocationLoggingConfigurationRequestRequestTypeDef",
    "AutomatedEvaluationConfigTypeDef",
    "HumanEvaluationConfigTypeDef",
    "EvaluationConfigTypeDef",
    "CreateEvaluationJobRequestRequestTypeDef",
    "GetEvaluationJobResponseTypeDef",
)

S3ConfigTypeDef = TypedDict(
    "S3ConfigTypeDef",
    {
        "bucketName": str,
        "keyPrefix": NotRequired[str],
    },
)
EvaluationOutputDataConfigTypeDef = TypedDict(
    "EvaluationOutputDataConfigTypeDef",
    {
        "s3Uri": str,
    },
)
TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
CreateGuardrailVersionRequestRequestTypeDef = TypedDict(
    "CreateGuardrailVersionRequestRequestTypeDef",
    {
        "guardrailIdentifier": str,
        "description": NotRequired[str],
        "clientRequestToken": NotRequired[str],
    },
)
OutputDataConfigTypeDef = TypedDict(
    "OutputDataConfigTypeDef",
    {
        "s3Uri": str,
    },
)
TrainingDataConfigTypeDef = TypedDict(
    "TrainingDataConfigTypeDef",
    {
        "s3Uri": str,
    },
)
VpcConfigTypeDef = TypedDict(
    "VpcConfigTypeDef",
    {
        "subnetIds": Sequence[str],
        "securityGroupIds": Sequence[str],
    },
)
CustomModelSummaryTypeDef = TypedDict(
    "CustomModelSummaryTypeDef",
    {
        "modelArn": str,
        "modelName": str,
        "creationTime": datetime,
        "baseModelArn": str,
        "baseModelName": str,
        "customizationType": NotRequired[CustomizationTypeType],
    },
)
DeleteCustomModelRequestRequestTypeDef = TypedDict(
    "DeleteCustomModelRequestRequestTypeDef",
    {
        "modelIdentifier": str,
    },
)
DeleteGuardrailRequestRequestTypeDef = TypedDict(
    "DeleteGuardrailRequestRequestTypeDef",
    {
        "guardrailIdentifier": str,
        "guardrailVersion": NotRequired[str],
    },
)
DeleteProvisionedModelThroughputRequestRequestTypeDef = TypedDict(
    "DeleteProvisionedModelThroughputRequestRequestTypeDef",
    {
        "provisionedModelId": str,
    },
)
EvaluationBedrockModelTypeDef = TypedDict(
    "EvaluationBedrockModelTypeDef",
    {
        "modelIdentifier": str,
        "inferenceParams": str,
    },
)
EvaluationDatasetLocationTypeDef = TypedDict(
    "EvaluationDatasetLocationTypeDef",
    {
        "s3Uri": NotRequired[str],
    },
)
EvaluationSummaryTypeDef = TypedDict(
    "EvaluationSummaryTypeDef",
    {
        "jobArn": str,
        "jobName": str,
        "status": EvaluationJobStatusType,
        "creationTime": datetime,
        "jobType": EvaluationJobTypeType,
        "evaluationTaskTypes": List[EvaluationTaskTypeType],
        "modelIdentifiers": List[str],
    },
)
FoundationModelLifecycleTypeDef = TypedDict(
    "FoundationModelLifecycleTypeDef",
    {
        "status": FoundationModelLifecycleStatusType,
    },
)
GetCustomModelRequestRequestTypeDef = TypedDict(
    "GetCustomModelRequestRequestTypeDef",
    {
        "modelIdentifier": str,
    },
)
TrainingMetricsTypeDef = TypedDict(
    "TrainingMetricsTypeDef",
    {
        "trainingLoss": NotRequired[float],
    },
)
ValidatorMetricTypeDef = TypedDict(
    "ValidatorMetricTypeDef",
    {
        "validationLoss": NotRequired[float],
    },
)
GetEvaluationJobRequestRequestTypeDef = TypedDict(
    "GetEvaluationJobRequestRequestTypeDef",
    {
        "jobIdentifier": str,
    },
)
GetFoundationModelRequestRequestTypeDef = TypedDict(
    "GetFoundationModelRequestRequestTypeDef",
    {
        "modelIdentifier": str,
    },
)
GetGuardrailRequestRequestTypeDef = TypedDict(
    "GetGuardrailRequestRequestTypeDef",
    {
        "guardrailIdentifier": str,
        "guardrailVersion": NotRequired[str],
    },
)
GetModelCustomizationJobRequestRequestTypeDef = TypedDict(
    "GetModelCustomizationJobRequestRequestTypeDef",
    {
        "jobIdentifier": str,
    },
)
GetProvisionedModelThroughputRequestRequestTypeDef = TypedDict(
    "GetProvisionedModelThroughputRequestRequestTypeDef",
    {
        "provisionedModelId": str,
    },
)
GuardrailContentFilterConfigTypeDef = TypedDict(
    "GuardrailContentFilterConfigTypeDef",
    {
        "type": GuardrailContentFilterTypeType,
        "inputStrength": GuardrailFilterStrengthType,
        "outputStrength": GuardrailFilterStrengthType,
    },
)
GuardrailContentFilterTypeDef = TypedDict(
    "GuardrailContentFilterTypeDef",
    {
        "type": GuardrailContentFilterTypeType,
        "inputStrength": GuardrailFilterStrengthType,
        "outputStrength": GuardrailFilterStrengthType,
    },
)
GuardrailManagedWordsConfigTypeDef = TypedDict(
    "GuardrailManagedWordsConfigTypeDef",
    {
        "type": Literal["PROFANITY"],
    },
)
GuardrailManagedWordsTypeDef = TypedDict(
    "GuardrailManagedWordsTypeDef",
    {
        "type": Literal["PROFANITY"],
    },
)
GuardrailPiiEntityConfigTypeDef = TypedDict(
    "GuardrailPiiEntityConfigTypeDef",
    {
        "type": GuardrailPiiEntityTypeType,
        "action": GuardrailSensitiveInformationActionType,
    },
)
GuardrailPiiEntityTypeDef = TypedDict(
    "GuardrailPiiEntityTypeDef",
    {
        "type": GuardrailPiiEntityTypeType,
        "action": GuardrailSensitiveInformationActionType,
    },
)
GuardrailRegexConfigTypeDef = TypedDict(
    "GuardrailRegexConfigTypeDef",
    {
        "name": str,
        "pattern": str,
        "action": GuardrailSensitiveInformationActionType,
        "description": NotRequired[str],
    },
)
GuardrailRegexTypeDef = TypedDict(
    "GuardrailRegexTypeDef",
    {
        "name": str,
        "pattern": str,
        "action": GuardrailSensitiveInformationActionType,
        "description": NotRequired[str],
    },
)
GuardrailSummaryTypeDef = TypedDict(
    "GuardrailSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "status": GuardrailStatusType,
        "name": str,
        "version": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "description": NotRequired[str],
    },
)
GuardrailTopicConfigTypeDef = TypedDict(
    "GuardrailTopicConfigTypeDef",
    {
        "name": str,
        "definition": str,
        "type": Literal["DENY"],
        "examples": NotRequired[Sequence[str]],
    },
)
GuardrailTopicTypeDef = TypedDict(
    "GuardrailTopicTypeDef",
    {
        "name": str,
        "definition": str,
        "examples": NotRequired[List[str]],
        "type": NotRequired[Literal["DENY"]],
    },
)
GuardrailWordConfigTypeDef = TypedDict(
    "GuardrailWordConfigTypeDef",
    {
        "text": str,
    },
)
GuardrailWordTypeDef = TypedDict(
    "GuardrailWordTypeDef",
    {
        "text": str,
    },
)
HumanEvaluationCustomMetricTypeDef = TypedDict(
    "HumanEvaluationCustomMetricTypeDef",
    {
        "name": str,
        "ratingMethod": str,
        "description": NotRequired[str],
    },
)
HumanWorkflowConfigTypeDef = TypedDict(
    "HumanWorkflowConfigTypeDef",
    {
        "flowDefinitionArn": str,
        "instructions": NotRequired[str],
    },
)
PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)
TimestampTypeDef = Union[datetime, str]
ListFoundationModelsRequestRequestTypeDef = TypedDict(
    "ListFoundationModelsRequestRequestTypeDef",
    {
        "byProvider": NotRequired[str],
        "byCustomizationType": NotRequired[ModelCustomizationType],
        "byOutputModality": NotRequired[ModelModalityType],
        "byInferenceType": NotRequired[InferenceTypeType],
    },
)
ListGuardrailsRequestRequestTypeDef = TypedDict(
    "ListGuardrailsRequestRequestTypeDef",
    {
        "guardrailIdentifier": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ModelCustomizationJobSummaryTypeDef = TypedDict(
    "ModelCustomizationJobSummaryTypeDef",
    {
        "jobArn": str,
        "baseModelArn": str,
        "jobName": str,
        "status": ModelCustomizationJobStatusType,
        "creationTime": datetime,
        "lastModifiedTime": NotRequired[datetime],
        "endTime": NotRequired[datetime],
        "customModelArn": NotRequired[str],
        "customModelName": NotRequired[str],
        "customizationType": NotRequired[CustomizationTypeType],
    },
)
ProvisionedModelSummaryTypeDef = TypedDict(
    "ProvisionedModelSummaryTypeDef",
    {
        "provisionedModelName": str,
        "provisionedModelArn": str,
        "modelArn": str,
        "desiredModelArn": str,
        "foundationModelArn": str,
        "modelUnits": int,
        "desiredModelUnits": int,
        "status": ProvisionedModelStatusType,
        "creationTime": datetime,
        "lastModifiedTime": datetime,
        "commitmentDuration": NotRequired[CommitmentDurationType],
        "commitmentExpirationTime": NotRequired[datetime],
    },
)
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceARN": str,
    },
)
StopEvaluationJobRequestRequestTypeDef = TypedDict(
    "StopEvaluationJobRequestRequestTypeDef",
    {
        "jobIdentifier": str,
    },
)
StopModelCustomizationJobRequestRequestTypeDef = TypedDict(
    "StopModelCustomizationJobRequestRequestTypeDef",
    {
        "jobIdentifier": str,
    },
)
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceARN": str,
        "tagKeys": Sequence[str],
    },
)
UpdateProvisionedModelThroughputRequestRequestTypeDef = TypedDict(
    "UpdateProvisionedModelThroughputRequestRequestTypeDef",
    {
        "provisionedModelId": str,
        "desiredProvisionedModelName": NotRequired[str],
        "desiredModelId": NotRequired[str],
    },
)
ValidatorTypeDef = TypedDict(
    "ValidatorTypeDef",
    {
        "s3Uri": str,
    },
)
CloudWatchConfigTypeDef = TypedDict(
    "CloudWatchConfigTypeDef",
    {
        "logGroupName": str,
        "roleArn": str,
        "largeDataDeliveryS3Config": NotRequired[S3ConfigTypeDef],
    },
)
CreateProvisionedModelThroughputRequestRequestTypeDef = TypedDict(
    "CreateProvisionedModelThroughputRequestRequestTypeDef",
    {
        "modelUnits": int,
        "provisionedModelName": str,
        "modelId": str,
        "clientRequestToken": NotRequired[str],
        "commitmentDuration": NotRequired[CommitmentDurationType],
        "tags": NotRequired[Sequence[TagTypeDef]],
    },
)
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceARN": str,
        "tags": Sequence[TagTypeDef],
    },
)
CreateEvaluationJobResponseTypeDef = TypedDict(
    "CreateEvaluationJobResponseTypeDef",
    {
        "jobArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateGuardrailResponseTypeDef = TypedDict(
    "CreateGuardrailResponseTypeDef",
    {
        "guardrailId": str,
        "guardrailArn": str,
        "version": str,
        "createdAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateGuardrailVersionResponseTypeDef = TypedDict(
    "CreateGuardrailVersionResponseTypeDef",
    {
        "guardrailId": str,
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateModelCustomizationJobResponseTypeDef = TypedDict(
    "CreateModelCustomizationJobResponseTypeDef",
    {
        "jobArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateProvisionedModelThroughputResponseTypeDef = TypedDict(
    "CreateProvisionedModelThroughputResponseTypeDef",
    {
        "provisionedModelArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetProvisionedModelThroughputResponseTypeDef = TypedDict(
    "GetProvisionedModelThroughputResponseTypeDef",
    {
        "modelUnits": int,
        "desiredModelUnits": int,
        "provisionedModelName": str,
        "provisionedModelArn": str,
        "modelArn": str,
        "desiredModelArn": str,
        "foundationModelArn": str,
        "status": ProvisionedModelStatusType,
        "creationTime": datetime,
        "lastModifiedTime": datetime,
        "failureMessage": str,
        "commitmentDuration": CommitmentDurationType,
        "commitmentExpirationTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateGuardrailResponseTypeDef = TypedDict(
    "UpdateGuardrailResponseTypeDef",
    {
        "guardrailId": str,
        "guardrailArn": str,
        "version": str,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListCustomModelsResponseTypeDef = TypedDict(
    "ListCustomModelsResponseTypeDef",
    {
        "nextToken": str,
        "modelSummaries": List[CustomModelSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EvaluationModelConfigTypeDef = TypedDict(
    "EvaluationModelConfigTypeDef",
    {
        "bedrockModel": NotRequired[EvaluationBedrockModelTypeDef],
    },
)
EvaluationDatasetTypeDef = TypedDict(
    "EvaluationDatasetTypeDef",
    {
        "name": str,
        "datasetLocation": NotRequired[EvaluationDatasetLocationTypeDef],
    },
)
ListEvaluationJobsResponseTypeDef = TypedDict(
    "ListEvaluationJobsResponseTypeDef",
    {
        "nextToken": str,
        "jobSummaries": List[EvaluationSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FoundationModelDetailsTypeDef = TypedDict(
    "FoundationModelDetailsTypeDef",
    {
        "modelArn": str,
        "modelId": str,
        "modelName": NotRequired[str],
        "providerName": NotRequired[str],
        "inputModalities": NotRequired[List[ModelModalityType]],
        "outputModalities": NotRequired[List[ModelModalityType]],
        "responseStreamingSupported": NotRequired[bool],
        "customizationsSupported": NotRequired[List[ModelCustomizationType]],
        "inferenceTypesSupported": NotRequired[List[InferenceTypeType]],
        "modelLifecycle": NotRequired[FoundationModelLifecycleTypeDef],
    },
)
FoundationModelSummaryTypeDef = TypedDict(
    "FoundationModelSummaryTypeDef",
    {
        "modelArn": str,
        "modelId": str,
        "modelName": NotRequired[str],
        "providerName": NotRequired[str],
        "inputModalities": NotRequired[List[ModelModalityType]],
        "outputModalities": NotRequired[List[ModelModalityType]],
        "responseStreamingSupported": NotRequired[bool],
        "customizationsSupported": NotRequired[List[ModelCustomizationType]],
        "inferenceTypesSupported": NotRequired[List[InferenceTypeType]],
        "modelLifecycle": NotRequired[FoundationModelLifecycleTypeDef],
    },
)
GuardrailContentPolicyConfigTypeDef = TypedDict(
    "GuardrailContentPolicyConfigTypeDef",
    {
        "filtersConfig": Sequence[GuardrailContentFilterConfigTypeDef],
    },
)
GuardrailContentPolicyTypeDef = TypedDict(
    "GuardrailContentPolicyTypeDef",
    {
        "filters": NotRequired[List[GuardrailContentFilterTypeDef]],
    },
)
GuardrailSensitiveInformationPolicyConfigTypeDef = TypedDict(
    "GuardrailSensitiveInformationPolicyConfigTypeDef",
    {
        "piiEntitiesConfig": NotRequired[Sequence[GuardrailPiiEntityConfigTypeDef]],
        "regexesConfig": NotRequired[Sequence[GuardrailRegexConfigTypeDef]],
    },
)
GuardrailSensitiveInformationPolicyTypeDef = TypedDict(
    "GuardrailSensitiveInformationPolicyTypeDef",
    {
        "piiEntities": NotRequired[List[GuardrailPiiEntityTypeDef]],
        "regexes": NotRequired[List[GuardrailRegexTypeDef]],
    },
)
ListGuardrailsResponseTypeDef = TypedDict(
    "ListGuardrailsResponseTypeDef",
    {
        "guardrails": List[GuardrailSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GuardrailTopicPolicyConfigTypeDef = TypedDict(
    "GuardrailTopicPolicyConfigTypeDef",
    {
        "topicsConfig": Sequence[GuardrailTopicConfigTypeDef],
    },
)
GuardrailTopicPolicyTypeDef = TypedDict(
    "GuardrailTopicPolicyTypeDef",
    {
        "topics": List[GuardrailTopicTypeDef],
    },
)
GuardrailWordPolicyConfigTypeDef = TypedDict(
    "GuardrailWordPolicyConfigTypeDef",
    {
        "wordsConfig": NotRequired[Sequence[GuardrailWordConfigTypeDef]],
        "managedWordListsConfig": NotRequired[Sequence[GuardrailManagedWordsConfigTypeDef]],
    },
)
GuardrailWordPolicyTypeDef = TypedDict(
    "GuardrailWordPolicyTypeDef",
    {
        "words": NotRequired[List[GuardrailWordTypeDef]],
        "managedWordLists": NotRequired[List[GuardrailManagedWordsTypeDef]],
    },
)
ListGuardrailsRequestListGuardrailsPaginateTypeDef = TypedDict(
    "ListGuardrailsRequestListGuardrailsPaginateTypeDef",
    {
        "guardrailIdentifier": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListCustomModelsRequestListCustomModelsPaginateTypeDef = TypedDict(
    "ListCustomModelsRequestListCustomModelsPaginateTypeDef",
    {
        "creationTimeBefore": NotRequired[TimestampTypeDef],
        "creationTimeAfter": NotRequired[TimestampTypeDef],
        "nameContains": NotRequired[str],
        "baseModelArnEquals": NotRequired[str],
        "foundationModelArnEquals": NotRequired[str],
        "sortBy": NotRequired[Literal["CreationTime"]],
        "sortOrder": NotRequired[SortOrderType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListCustomModelsRequestRequestTypeDef = TypedDict(
    "ListCustomModelsRequestRequestTypeDef",
    {
        "creationTimeBefore": NotRequired[TimestampTypeDef],
        "creationTimeAfter": NotRequired[TimestampTypeDef],
        "nameContains": NotRequired[str],
        "baseModelArnEquals": NotRequired[str],
        "foundationModelArnEquals": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "sortBy": NotRequired[Literal["CreationTime"]],
        "sortOrder": NotRequired[SortOrderType],
    },
)
ListEvaluationJobsRequestListEvaluationJobsPaginateTypeDef = TypedDict(
    "ListEvaluationJobsRequestListEvaluationJobsPaginateTypeDef",
    {
        "creationTimeAfter": NotRequired[TimestampTypeDef],
        "creationTimeBefore": NotRequired[TimestampTypeDef],
        "statusEquals": NotRequired[EvaluationJobStatusType],
        "nameContains": NotRequired[str],
        "sortBy": NotRequired[Literal["CreationTime"]],
        "sortOrder": NotRequired[SortOrderType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListEvaluationJobsRequestRequestTypeDef = TypedDict(
    "ListEvaluationJobsRequestRequestTypeDef",
    {
        "creationTimeAfter": NotRequired[TimestampTypeDef],
        "creationTimeBefore": NotRequired[TimestampTypeDef],
        "statusEquals": NotRequired[EvaluationJobStatusType],
        "nameContains": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "sortBy": NotRequired[Literal["CreationTime"]],
        "sortOrder": NotRequired[SortOrderType],
    },
)
ListModelCustomizationJobsRequestListModelCustomizationJobsPaginateTypeDef = TypedDict(
    "ListModelCustomizationJobsRequestListModelCustomizationJobsPaginateTypeDef",
    {
        "creationTimeAfter": NotRequired[TimestampTypeDef],
        "creationTimeBefore": NotRequired[TimestampTypeDef],
        "statusEquals": NotRequired[FineTuningJobStatusType],
        "nameContains": NotRequired[str],
        "sortBy": NotRequired[Literal["CreationTime"]],
        "sortOrder": NotRequired[SortOrderType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListModelCustomizationJobsRequestRequestTypeDef = TypedDict(
    "ListModelCustomizationJobsRequestRequestTypeDef",
    {
        "creationTimeAfter": NotRequired[TimestampTypeDef],
        "creationTimeBefore": NotRequired[TimestampTypeDef],
        "statusEquals": NotRequired[FineTuningJobStatusType],
        "nameContains": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "sortBy": NotRequired[Literal["CreationTime"]],
        "sortOrder": NotRequired[SortOrderType],
    },
)
ListProvisionedModelThroughputsRequestListProvisionedModelThroughputsPaginateTypeDef = TypedDict(
    "ListProvisionedModelThroughputsRequestListProvisionedModelThroughputsPaginateTypeDef",
    {
        "creationTimeAfter": NotRequired[TimestampTypeDef],
        "creationTimeBefore": NotRequired[TimestampTypeDef],
        "statusEquals": NotRequired[ProvisionedModelStatusType],
        "modelArnEquals": NotRequired[str],
        "nameContains": NotRequired[str],
        "sortBy": NotRequired[Literal["CreationTime"]],
        "sortOrder": NotRequired[SortOrderType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListProvisionedModelThroughputsRequestRequestTypeDef = TypedDict(
    "ListProvisionedModelThroughputsRequestRequestTypeDef",
    {
        "creationTimeAfter": NotRequired[TimestampTypeDef],
        "creationTimeBefore": NotRequired[TimestampTypeDef],
        "statusEquals": NotRequired[ProvisionedModelStatusType],
        "modelArnEquals": NotRequired[str],
        "nameContains": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "sortBy": NotRequired[Literal["CreationTime"]],
        "sortOrder": NotRequired[SortOrderType],
    },
)
ListModelCustomizationJobsResponseTypeDef = TypedDict(
    "ListModelCustomizationJobsResponseTypeDef",
    {
        "nextToken": str,
        "modelCustomizationJobSummaries": List[ModelCustomizationJobSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListProvisionedModelThroughputsResponseTypeDef = TypedDict(
    "ListProvisionedModelThroughputsResponseTypeDef",
    {
        "nextToken": str,
        "provisionedModelSummaries": List[ProvisionedModelSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ValidationDataConfigTypeDef = TypedDict(
    "ValidationDataConfigTypeDef",
    {
        "validators": Sequence[ValidatorTypeDef],
    },
)
LoggingConfigTypeDef = TypedDict(
    "LoggingConfigTypeDef",
    {
        "cloudWatchConfig": NotRequired[CloudWatchConfigTypeDef],
        "s3Config": NotRequired[S3ConfigTypeDef],
        "textDataDeliveryEnabled": NotRequired[bool],
        "imageDataDeliveryEnabled": NotRequired[bool],
        "embeddingDataDeliveryEnabled": NotRequired[bool],
    },
)
EvaluationInferenceConfigTypeDef = TypedDict(
    "EvaluationInferenceConfigTypeDef",
    {
        "models": NotRequired[Sequence[EvaluationModelConfigTypeDef]],
    },
)
EvaluationDatasetMetricConfigTypeDef = TypedDict(
    "EvaluationDatasetMetricConfigTypeDef",
    {
        "taskType": EvaluationTaskTypeType,
        "dataset": EvaluationDatasetTypeDef,
        "metricNames": Sequence[str],
    },
)
GetFoundationModelResponseTypeDef = TypedDict(
    "GetFoundationModelResponseTypeDef",
    {
        "modelDetails": FoundationModelDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListFoundationModelsResponseTypeDef = TypedDict(
    "ListFoundationModelsResponseTypeDef",
    {
        "modelSummaries": List[FoundationModelSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateGuardrailRequestRequestTypeDef = TypedDict(
    "CreateGuardrailRequestRequestTypeDef",
    {
        "name": str,
        "blockedInputMessaging": str,
        "blockedOutputsMessaging": str,
        "description": NotRequired[str],
        "topicPolicyConfig": NotRequired[GuardrailTopicPolicyConfigTypeDef],
        "contentPolicyConfig": NotRequired[GuardrailContentPolicyConfigTypeDef],
        "wordPolicyConfig": NotRequired[GuardrailWordPolicyConfigTypeDef],
        "sensitiveInformationPolicyConfig": NotRequired[
            GuardrailSensitiveInformationPolicyConfigTypeDef
        ],
        "kmsKeyId": NotRequired[str],
        "tags": NotRequired[Sequence[TagTypeDef]],
        "clientRequestToken": NotRequired[str],
    },
)
UpdateGuardrailRequestRequestTypeDef = TypedDict(
    "UpdateGuardrailRequestRequestTypeDef",
    {
        "guardrailIdentifier": str,
        "name": str,
        "blockedInputMessaging": str,
        "blockedOutputsMessaging": str,
        "description": NotRequired[str],
        "topicPolicyConfig": NotRequired[GuardrailTopicPolicyConfigTypeDef],
        "contentPolicyConfig": NotRequired[GuardrailContentPolicyConfigTypeDef],
        "wordPolicyConfig": NotRequired[GuardrailWordPolicyConfigTypeDef],
        "sensitiveInformationPolicyConfig": NotRequired[
            GuardrailSensitiveInformationPolicyConfigTypeDef
        ],
        "kmsKeyId": NotRequired[str],
    },
)
GetGuardrailResponseTypeDef = TypedDict(
    "GetGuardrailResponseTypeDef",
    {
        "name": str,
        "description": str,
        "guardrailId": str,
        "guardrailArn": str,
        "version": str,
        "status": GuardrailStatusType,
        "topicPolicy": GuardrailTopicPolicyTypeDef,
        "contentPolicy": GuardrailContentPolicyTypeDef,
        "wordPolicy": GuardrailWordPolicyTypeDef,
        "sensitiveInformationPolicy": GuardrailSensitiveInformationPolicyTypeDef,
        "createdAt": datetime,
        "updatedAt": datetime,
        "statusReasons": List[str],
        "failureRecommendations": List[str],
        "blockedInputMessaging": str,
        "blockedOutputsMessaging": str,
        "kmsKeyArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateModelCustomizationJobRequestRequestTypeDef = TypedDict(
    "CreateModelCustomizationJobRequestRequestTypeDef",
    {
        "jobName": str,
        "customModelName": str,
        "roleArn": str,
        "baseModelIdentifier": str,
        "trainingDataConfig": TrainingDataConfigTypeDef,
        "outputDataConfig": OutputDataConfigTypeDef,
        "hyperParameters": Mapping[str, str],
        "clientRequestToken": NotRequired[str],
        "customizationType": NotRequired[CustomizationTypeType],
        "customModelKmsKeyId": NotRequired[str],
        "jobTags": NotRequired[Sequence[TagTypeDef]],
        "customModelTags": NotRequired[Sequence[TagTypeDef]],
        "validationDataConfig": NotRequired[ValidationDataConfigTypeDef],
        "vpcConfig": NotRequired[VpcConfigTypeDef],
    },
)
GetCustomModelResponseTypeDef = TypedDict(
    "GetCustomModelResponseTypeDef",
    {
        "modelArn": str,
        "modelName": str,
        "jobName": str,
        "jobArn": str,
        "baseModelArn": str,
        "customizationType": CustomizationTypeType,
        "modelKmsKeyArn": str,
        "hyperParameters": Dict[str, str],
        "trainingDataConfig": TrainingDataConfigTypeDef,
        "validationDataConfig": ValidationDataConfigTypeDef,
        "outputDataConfig": OutputDataConfigTypeDef,
        "trainingMetrics": TrainingMetricsTypeDef,
        "validationMetrics": List[ValidatorMetricTypeDef],
        "creationTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetModelCustomizationJobResponseTypeDef = TypedDict(
    "GetModelCustomizationJobResponseTypeDef",
    {
        "jobArn": str,
        "jobName": str,
        "outputModelName": str,
        "outputModelArn": str,
        "clientRequestToken": str,
        "roleArn": str,
        "status": ModelCustomizationJobStatusType,
        "failureMessage": str,
        "creationTime": datetime,
        "lastModifiedTime": datetime,
        "endTime": datetime,
        "baseModelArn": str,
        "hyperParameters": Dict[str, str],
        "trainingDataConfig": TrainingDataConfigTypeDef,
        "validationDataConfig": ValidationDataConfigTypeDef,
        "outputDataConfig": OutputDataConfigTypeDef,
        "customizationType": CustomizationTypeType,
        "outputModelKmsKeyArn": str,
        "trainingMetrics": TrainingMetricsTypeDef,
        "validationMetrics": List[ValidatorMetricTypeDef],
        "vpcConfig": VpcConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetModelInvocationLoggingConfigurationResponseTypeDef = TypedDict(
    "GetModelInvocationLoggingConfigurationResponseTypeDef",
    {
        "loggingConfig": LoggingConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutModelInvocationLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "PutModelInvocationLoggingConfigurationRequestRequestTypeDef",
    {
        "loggingConfig": LoggingConfigTypeDef,
    },
)
AutomatedEvaluationConfigTypeDef = TypedDict(
    "AutomatedEvaluationConfigTypeDef",
    {
        "datasetMetricConfigs": Sequence[EvaluationDatasetMetricConfigTypeDef],
    },
)
HumanEvaluationConfigTypeDef = TypedDict(
    "HumanEvaluationConfigTypeDef",
    {
        "datasetMetricConfigs": Sequence[EvaluationDatasetMetricConfigTypeDef],
        "humanWorkflowConfig": NotRequired[HumanWorkflowConfigTypeDef],
        "customMetrics": NotRequired[Sequence[HumanEvaluationCustomMetricTypeDef]],
    },
)
EvaluationConfigTypeDef = TypedDict(
    "EvaluationConfigTypeDef",
    {
        "automated": NotRequired[AutomatedEvaluationConfigTypeDef],
        "human": NotRequired[HumanEvaluationConfigTypeDef],
    },
)
CreateEvaluationJobRequestRequestTypeDef = TypedDict(
    "CreateEvaluationJobRequestRequestTypeDef",
    {
        "jobName": str,
        "roleArn": str,
        "evaluationConfig": EvaluationConfigTypeDef,
        "inferenceConfig": EvaluationInferenceConfigTypeDef,
        "outputDataConfig": EvaluationOutputDataConfigTypeDef,
        "jobDescription": NotRequired[str],
        "clientRequestToken": NotRequired[str],
        "customerEncryptionKeyId": NotRequired[str],
        "jobTags": NotRequired[Sequence[TagTypeDef]],
    },
)
GetEvaluationJobResponseTypeDef = TypedDict(
    "GetEvaluationJobResponseTypeDef",
    {
        "jobName": str,
        "status": EvaluationJobStatusType,
        "jobArn": str,
        "jobDescription": str,
        "roleArn": str,
        "customerEncryptionKeyId": str,
        "jobType": EvaluationJobTypeType,
        "evaluationConfig": EvaluationConfigTypeDef,
        "inferenceConfig": EvaluationInferenceConfigTypeDef,
        "outputDataConfig": EvaluationOutputDataConfigTypeDef,
        "creationTime": datetime,
        "lastModifiedTime": datetime,
        "failureMessages": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
