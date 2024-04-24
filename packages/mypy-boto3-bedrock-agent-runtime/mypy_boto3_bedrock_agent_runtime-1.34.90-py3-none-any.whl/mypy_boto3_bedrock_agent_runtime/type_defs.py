"""
Type annotations for bedrock-agent-runtime service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/type_defs/)

Usage::

    ```python
    from mypy_boto3_bedrock_agent_runtime.type_defs import AccessDeniedExceptionTypeDef

    data: AccessDeniedExceptionTypeDef = ...
    ```
"""

import sys
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.eventstream import EventStream
from botocore.response import StreamingBody

from .literals import (
    CreationModeType,
    ExternalSourceTypeType,
    InvocationTypeType,
    PromptTypeType,
    ResponseStateType,
    RetrieveAndGenerateTypeType,
    SearchTypeType,
    SourceType,
    TypeType,
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
    "AccessDeniedExceptionTypeDef",
    "ParameterTypeDef",
    "ActionGroupInvocationOutputTypeDef",
    "ApiParameterTypeDef",
    "ContentBodyTypeDef",
    "BadGatewayExceptionTypeDef",
    "BlobTypeDef",
    "ConflictExceptionTypeDef",
    "DependencyFailedExceptionTypeDef",
    "S3ObjectDocTypeDef",
    "PromptTemplateTypeDef",
    "FailureTraceTypeDef",
    "FilterAttributeTypeDef",
    "FinalResponseTypeDef",
    "FunctionParameterTypeDef",
    "InferenceConfigurationTypeDef",
    "InternalServerExceptionTypeDef",
    "KnowledgeBaseLookupInputTypeDef",
    "ResponseMetadataTypeDef",
    "KnowledgeBaseQueryTypeDef",
    "KnowledgeBaseVectorSearchConfigurationTypeDef",
    "RetrievalResultContentTypeDef",
    "RepromptResponseTypeDef",
    "RationaleTypeDef",
    "PaginatorConfigTypeDef",
    "PostProcessingParsedResponseTypeDef",
    "PreProcessingParsedResponseTypeDef",
    "ResourceNotFoundExceptionTypeDef",
    "ServiceQuotaExceededExceptionTypeDef",
    "ThrottlingExceptionTypeDef",
    "ValidationExceptionTypeDef",
    "RetrievalResultS3LocationTypeDef",
    "RetrieveAndGenerateInputTypeDef",
    "RetrieveAndGenerateOutputTypeDef",
    "RetrieveAndGenerateSessionConfigurationTypeDef",
    "SpanTypeDef",
    "PropertyParametersTypeDef",
    "RequestBodyTypeDef",
    "ApiResultTypeDef",
    "FunctionResultTypeDef",
    "ByteContentDocTypeDef",
    "ExternalSourcesGenerationConfigurationTypeDef",
    "GenerationConfigurationTypeDef",
    "RetrievalFilterTypeDef",
    "FunctionInvocationInputTypeDef",
    "ModelInvocationInputTypeDef",
    "KnowledgeBaseRetrievalConfigurationTypeDef",
    "PostProcessingModelInvocationOutputTypeDef",
    "PreProcessingModelInvocationOutputTypeDef",
    "RetrievalResultLocationTypeDef",
    "TextResponsePartTypeDef",
    "ApiRequestBodyTypeDef",
    "ActionGroupInvocationInputTypeDef",
    "InvocationResultMemberTypeDef",
    "ExternalSourceTypeDef",
    "KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef",
    "RetrieveRequestRequestTypeDef",
    "RetrieveRequestRetrievePaginateTypeDef",
    "PostProcessingTraceTypeDef",
    "PreProcessingTraceTypeDef",
    "KnowledgeBaseRetrievalResultTypeDef",
    "RetrievedReferenceTypeDef",
    "GeneratedResponsePartTypeDef",
    "ApiInvocationInputTypeDef",
    "InvocationInputTypeDef",
    "SessionStateTypeDef",
    "ExternalSourcesRetrieveAndGenerateConfigurationTypeDef",
    "RetrieveResponseTypeDef",
    "KnowledgeBaseLookupOutputTypeDef",
    "CitationTypeDef",
    "InvocationInputMemberTypeDef",
    "InvokeAgentRequestRequestTypeDef",
    "RetrieveAndGenerateConfigurationTypeDef",
    "ObservationTypeDef",
    "AttributionTypeDef",
    "RetrieveAndGenerateResponseTypeDef",
    "ReturnControlPayloadTypeDef",
    "RetrieveAndGenerateRequestRequestTypeDef",
    "OrchestrationTraceTypeDef",
    "PayloadPartTypeDef",
    "TraceTypeDef",
    "TracePartTypeDef",
    "ResponseStreamTypeDef",
    "InvokeAgentResponseTypeDef",
)

AccessDeniedExceptionTypeDef = TypedDict(
    "AccessDeniedExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
ParameterTypeDef = TypedDict(
    "ParameterTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
    },
)
ActionGroupInvocationOutputTypeDef = TypedDict(
    "ActionGroupInvocationOutputTypeDef",
    {
        "text": NotRequired[str],
    },
)
ApiParameterTypeDef = TypedDict(
    "ApiParameterTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
    },
)
ContentBodyTypeDef = TypedDict(
    "ContentBodyTypeDef",
    {
        "body": NotRequired[str],
    },
)
BadGatewayExceptionTypeDef = TypedDict(
    "BadGatewayExceptionTypeDef",
    {
        "message": NotRequired[str],
        "resourceName": NotRequired[str],
    },
)
BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
ConflictExceptionTypeDef = TypedDict(
    "ConflictExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
DependencyFailedExceptionTypeDef = TypedDict(
    "DependencyFailedExceptionTypeDef",
    {
        "message": NotRequired[str],
        "resourceName": NotRequired[str],
    },
)
S3ObjectDocTypeDef = TypedDict(
    "S3ObjectDocTypeDef",
    {
        "uri": str,
    },
)
PromptTemplateTypeDef = TypedDict(
    "PromptTemplateTypeDef",
    {
        "textPromptTemplate": NotRequired[str],
    },
)
FailureTraceTypeDef = TypedDict(
    "FailureTraceTypeDef",
    {
        "failureReason": NotRequired[str],
        "traceId": NotRequired[str],
    },
)
FilterAttributeTypeDef = TypedDict(
    "FilterAttributeTypeDef",
    {
        "key": str,
        "value": Mapping[str, Any],
    },
)
FinalResponseTypeDef = TypedDict(
    "FinalResponseTypeDef",
    {
        "text": NotRequired[str],
    },
)
FunctionParameterTypeDef = TypedDict(
    "FunctionParameterTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
    },
)
InferenceConfigurationTypeDef = TypedDict(
    "InferenceConfigurationTypeDef",
    {
        "maximumLength": NotRequired[int],
        "stopSequences": NotRequired[List[str]],
        "temperature": NotRequired[float],
        "topK": NotRequired[int],
        "topP": NotRequired[float],
    },
)
InternalServerExceptionTypeDef = TypedDict(
    "InternalServerExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
KnowledgeBaseLookupInputTypeDef = TypedDict(
    "KnowledgeBaseLookupInputTypeDef",
    {
        "knowledgeBaseId": NotRequired[str],
        "text": NotRequired[str],
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
KnowledgeBaseQueryTypeDef = TypedDict(
    "KnowledgeBaseQueryTypeDef",
    {
        "text": str,
    },
)
KnowledgeBaseVectorSearchConfigurationTypeDef = TypedDict(
    "KnowledgeBaseVectorSearchConfigurationTypeDef",
    {
        "filter": NotRequired["RetrievalFilterTypeDef"],
        "numberOfResults": NotRequired[int],
        "overrideSearchType": NotRequired[SearchTypeType],
    },
)
RetrievalResultContentTypeDef = TypedDict(
    "RetrievalResultContentTypeDef",
    {
        "text": str,
    },
)
RepromptResponseTypeDef = TypedDict(
    "RepromptResponseTypeDef",
    {
        "source": NotRequired[SourceType],
        "text": NotRequired[str],
    },
)
RationaleTypeDef = TypedDict(
    "RationaleTypeDef",
    {
        "text": NotRequired[str],
        "traceId": NotRequired[str],
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
PostProcessingParsedResponseTypeDef = TypedDict(
    "PostProcessingParsedResponseTypeDef",
    {
        "text": NotRequired[str],
    },
)
PreProcessingParsedResponseTypeDef = TypedDict(
    "PreProcessingParsedResponseTypeDef",
    {
        "isValid": NotRequired[bool],
        "rationale": NotRequired[str],
    },
)
ResourceNotFoundExceptionTypeDef = TypedDict(
    "ResourceNotFoundExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
ServiceQuotaExceededExceptionTypeDef = TypedDict(
    "ServiceQuotaExceededExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
ThrottlingExceptionTypeDef = TypedDict(
    "ThrottlingExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
ValidationExceptionTypeDef = TypedDict(
    "ValidationExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
RetrievalResultS3LocationTypeDef = TypedDict(
    "RetrievalResultS3LocationTypeDef",
    {
        "uri": NotRequired[str],
    },
)
RetrieveAndGenerateInputTypeDef = TypedDict(
    "RetrieveAndGenerateInputTypeDef",
    {
        "text": str,
    },
)
RetrieveAndGenerateOutputTypeDef = TypedDict(
    "RetrieveAndGenerateOutputTypeDef",
    {
        "text": str,
    },
)
RetrieveAndGenerateSessionConfigurationTypeDef = TypedDict(
    "RetrieveAndGenerateSessionConfigurationTypeDef",
    {
        "kmsKeyArn": str,
    },
)
SpanTypeDef = TypedDict(
    "SpanTypeDef",
    {
        "end": NotRequired[int],
        "start": NotRequired[int],
    },
)
PropertyParametersTypeDef = TypedDict(
    "PropertyParametersTypeDef",
    {
        "properties": NotRequired[List[ParameterTypeDef]],
    },
)
RequestBodyTypeDef = TypedDict(
    "RequestBodyTypeDef",
    {
        "content": NotRequired[Dict[str, List[ParameterTypeDef]]],
    },
)
ApiResultTypeDef = TypedDict(
    "ApiResultTypeDef",
    {
        "actionGroup": str,
        "apiPath": NotRequired[str],
        "httpMethod": NotRequired[str],
        "httpStatusCode": NotRequired[int],
        "responseBody": NotRequired[Mapping[str, ContentBodyTypeDef]],
        "responseState": NotRequired[ResponseStateType],
    },
)
FunctionResultTypeDef = TypedDict(
    "FunctionResultTypeDef",
    {
        "actionGroup": str,
        "function": NotRequired[str],
        "responseBody": NotRequired[Mapping[str, ContentBodyTypeDef]],
        "responseState": NotRequired[ResponseStateType],
    },
)
ByteContentDocTypeDef = TypedDict(
    "ByteContentDocTypeDef",
    {
        "contentType": str,
        "data": BlobTypeDef,
        "identifier": str,
    },
)
ExternalSourcesGenerationConfigurationTypeDef = TypedDict(
    "ExternalSourcesGenerationConfigurationTypeDef",
    {
        "promptTemplate": NotRequired[PromptTemplateTypeDef],
    },
)
GenerationConfigurationTypeDef = TypedDict(
    "GenerationConfigurationTypeDef",
    {
        "promptTemplate": NotRequired[PromptTemplateTypeDef],
    },
)
RetrievalFilterTypeDef = TypedDict(
    "RetrievalFilterTypeDef",
    {
        "andAll": NotRequired[Sequence[Dict[str, Any]]],
        "equals": NotRequired[FilterAttributeTypeDef],
        "greaterThan": NotRequired[FilterAttributeTypeDef],
        "greaterThanOrEquals": NotRequired[FilterAttributeTypeDef],
        "in": NotRequired[FilterAttributeTypeDef],
        "lessThan": NotRequired[FilterAttributeTypeDef],
        "lessThanOrEquals": NotRequired[FilterAttributeTypeDef],
        "notEquals": NotRequired[FilterAttributeTypeDef],
        "notIn": NotRequired[FilterAttributeTypeDef],
        "orAll": NotRequired[Sequence[Dict[str, Any]]],
        "startsWith": NotRequired[FilterAttributeTypeDef],
    },
)
FunctionInvocationInputTypeDef = TypedDict(
    "FunctionInvocationInputTypeDef",
    {
        "actionGroup": str,
        "function": NotRequired[str],
        "parameters": NotRequired[List[FunctionParameterTypeDef]],
    },
)
ModelInvocationInputTypeDef = TypedDict(
    "ModelInvocationInputTypeDef",
    {
        "inferenceConfiguration": NotRequired[InferenceConfigurationTypeDef],
        "overrideLambda": NotRequired[str],
        "parserMode": NotRequired[CreationModeType],
        "promptCreationMode": NotRequired[CreationModeType],
        "text": NotRequired[str],
        "traceId": NotRequired[str],
        "type": NotRequired[PromptTypeType],
    },
)
KnowledgeBaseRetrievalConfigurationTypeDef = TypedDict(
    "KnowledgeBaseRetrievalConfigurationTypeDef",
    {
        "vectorSearchConfiguration": KnowledgeBaseVectorSearchConfigurationTypeDef,
    },
)
PostProcessingModelInvocationOutputTypeDef = TypedDict(
    "PostProcessingModelInvocationOutputTypeDef",
    {
        "parsedResponse": NotRequired[PostProcessingParsedResponseTypeDef],
        "traceId": NotRequired[str],
    },
)
PreProcessingModelInvocationOutputTypeDef = TypedDict(
    "PreProcessingModelInvocationOutputTypeDef",
    {
        "parsedResponse": NotRequired[PreProcessingParsedResponseTypeDef],
        "traceId": NotRequired[str],
    },
)
RetrievalResultLocationTypeDef = TypedDict(
    "RetrievalResultLocationTypeDef",
    {
        "type": Literal["S3"],
        "s3Location": NotRequired[RetrievalResultS3LocationTypeDef],
    },
)
TextResponsePartTypeDef = TypedDict(
    "TextResponsePartTypeDef",
    {
        "span": NotRequired[SpanTypeDef],
        "text": NotRequired[str],
    },
)
ApiRequestBodyTypeDef = TypedDict(
    "ApiRequestBodyTypeDef",
    {
        "content": NotRequired[Dict[str, PropertyParametersTypeDef]],
    },
)
ActionGroupInvocationInputTypeDef = TypedDict(
    "ActionGroupInvocationInputTypeDef",
    {
        "actionGroupName": NotRequired[str],
        "apiPath": NotRequired[str],
        "function": NotRequired[str],
        "parameters": NotRequired[List[ParameterTypeDef]],
        "requestBody": NotRequired[RequestBodyTypeDef],
        "verb": NotRequired[str],
    },
)
InvocationResultMemberTypeDef = TypedDict(
    "InvocationResultMemberTypeDef",
    {
        "apiResult": NotRequired[ApiResultTypeDef],
        "functionResult": NotRequired[FunctionResultTypeDef],
    },
)
ExternalSourceTypeDef = TypedDict(
    "ExternalSourceTypeDef",
    {
        "sourceType": ExternalSourceTypeType,
        "byteContent": NotRequired[ByteContentDocTypeDef],
        "s3Location": NotRequired[S3ObjectDocTypeDef],
    },
)
KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef = TypedDict(
    "KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef",
    {
        "knowledgeBaseId": str,
        "modelArn": str,
        "generationConfiguration": NotRequired[GenerationConfigurationTypeDef],
        "retrievalConfiguration": NotRequired[KnowledgeBaseRetrievalConfigurationTypeDef],
    },
)
RetrieveRequestRequestTypeDef = TypedDict(
    "RetrieveRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "retrievalQuery": KnowledgeBaseQueryTypeDef,
        "nextToken": NotRequired[str],
        "retrievalConfiguration": NotRequired[KnowledgeBaseRetrievalConfigurationTypeDef],
    },
)
RetrieveRequestRetrievePaginateTypeDef = TypedDict(
    "RetrieveRequestRetrievePaginateTypeDef",
    {
        "knowledgeBaseId": str,
        "retrievalQuery": KnowledgeBaseQueryTypeDef,
        "retrievalConfiguration": NotRequired[KnowledgeBaseRetrievalConfigurationTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
PostProcessingTraceTypeDef = TypedDict(
    "PostProcessingTraceTypeDef",
    {
        "modelInvocationInput": NotRequired[ModelInvocationInputTypeDef],
        "modelInvocationOutput": NotRequired[PostProcessingModelInvocationOutputTypeDef],
    },
)
PreProcessingTraceTypeDef = TypedDict(
    "PreProcessingTraceTypeDef",
    {
        "modelInvocationInput": NotRequired[ModelInvocationInputTypeDef],
        "modelInvocationOutput": NotRequired[PreProcessingModelInvocationOutputTypeDef],
    },
)
KnowledgeBaseRetrievalResultTypeDef = TypedDict(
    "KnowledgeBaseRetrievalResultTypeDef",
    {
        "content": RetrievalResultContentTypeDef,
        "location": NotRequired[RetrievalResultLocationTypeDef],
        "metadata": NotRequired[Dict[str, Dict[str, Any]]],
        "score": NotRequired[float],
    },
)
RetrievedReferenceTypeDef = TypedDict(
    "RetrievedReferenceTypeDef",
    {
        "content": NotRequired[RetrievalResultContentTypeDef],
        "location": NotRequired[RetrievalResultLocationTypeDef],
        "metadata": NotRequired[Dict[str, Dict[str, Any]]],
    },
)
GeneratedResponsePartTypeDef = TypedDict(
    "GeneratedResponsePartTypeDef",
    {
        "textResponsePart": NotRequired[TextResponsePartTypeDef],
    },
)
ApiInvocationInputTypeDef = TypedDict(
    "ApiInvocationInputTypeDef",
    {
        "actionGroup": str,
        "apiPath": NotRequired[str],
        "httpMethod": NotRequired[str],
        "parameters": NotRequired[List[ApiParameterTypeDef]],
        "requestBody": NotRequired[ApiRequestBodyTypeDef],
    },
)
InvocationInputTypeDef = TypedDict(
    "InvocationInputTypeDef",
    {
        "actionGroupInvocationInput": NotRequired[ActionGroupInvocationInputTypeDef],
        "invocationType": NotRequired[InvocationTypeType],
        "knowledgeBaseLookupInput": NotRequired[KnowledgeBaseLookupInputTypeDef],
        "traceId": NotRequired[str],
    },
)
SessionStateTypeDef = TypedDict(
    "SessionStateTypeDef",
    {
        "invocationId": NotRequired[str],
        "promptSessionAttributes": NotRequired[Mapping[str, str]],
        "returnControlInvocationResults": NotRequired[Sequence[InvocationResultMemberTypeDef]],
        "sessionAttributes": NotRequired[Mapping[str, str]],
    },
)
ExternalSourcesRetrieveAndGenerateConfigurationTypeDef = TypedDict(
    "ExternalSourcesRetrieveAndGenerateConfigurationTypeDef",
    {
        "modelArn": str,
        "sources": Sequence[ExternalSourceTypeDef],
        "generationConfiguration": NotRequired[ExternalSourcesGenerationConfigurationTypeDef],
    },
)
RetrieveResponseTypeDef = TypedDict(
    "RetrieveResponseTypeDef",
    {
        "nextToken": str,
        "retrievalResults": List[KnowledgeBaseRetrievalResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
KnowledgeBaseLookupOutputTypeDef = TypedDict(
    "KnowledgeBaseLookupOutputTypeDef",
    {
        "retrievedReferences": NotRequired[List[RetrievedReferenceTypeDef]],
    },
)
CitationTypeDef = TypedDict(
    "CitationTypeDef",
    {
        "generatedResponsePart": NotRequired[GeneratedResponsePartTypeDef],
        "retrievedReferences": NotRequired[List[RetrievedReferenceTypeDef]],
    },
)
InvocationInputMemberTypeDef = TypedDict(
    "InvocationInputMemberTypeDef",
    {
        "apiInvocationInput": NotRequired[ApiInvocationInputTypeDef],
        "functionInvocationInput": NotRequired[FunctionInvocationInputTypeDef],
    },
)
InvokeAgentRequestRequestTypeDef = TypedDict(
    "InvokeAgentRequestRequestTypeDef",
    {
        "agentAliasId": str,
        "agentId": str,
        "sessionId": str,
        "enableTrace": NotRequired[bool],
        "endSession": NotRequired[bool],
        "inputText": NotRequired[str],
        "sessionState": NotRequired[SessionStateTypeDef],
    },
)
RetrieveAndGenerateConfigurationTypeDef = TypedDict(
    "RetrieveAndGenerateConfigurationTypeDef",
    {
        "type": RetrieveAndGenerateTypeType,
        "externalSourcesConfiguration": NotRequired[
            ExternalSourcesRetrieveAndGenerateConfigurationTypeDef
        ],
        "knowledgeBaseConfiguration": NotRequired[
            KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef
        ],
    },
)
ObservationTypeDef = TypedDict(
    "ObservationTypeDef",
    {
        "actionGroupInvocationOutput": NotRequired[ActionGroupInvocationOutputTypeDef],
        "finalResponse": NotRequired[FinalResponseTypeDef],
        "knowledgeBaseLookupOutput": NotRequired[KnowledgeBaseLookupOutputTypeDef],
        "repromptResponse": NotRequired[RepromptResponseTypeDef],
        "traceId": NotRequired[str],
        "type": NotRequired[TypeType],
    },
)
AttributionTypeDef = TypedDict(
    "AttributionTypeDef",
    {
        "citations": NotRequired[List[CitationTypeDef]],
    },
)
RetrieveAndGenerateResponseTypeDef = TypedDict(
    "RetrieveAndGenerateResponseTypeDef",
    {
        "citations": List[CitationTypeDef],
        "output": RetrieveAndGenerateOutputTypeDef,
        "sessionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ReturnControlPayloadTypeDef = TypedDict(
    "ReturnControlPayloadTypeDef",
    {
        "invocationId": NotRequired[str],
        "invocationInputs": NotRequired[List[InvocationInputMemberTypeDef]],
    },
)
RetrieveAndGenerateRequestRequestTypeDef = TypedDict(
    "RetrieveAndGenerateRequestRequestTypeDef",
    {
        "input": RetrieveAndGenerateInputTypeDef,
        "retrieveAndGenerateConfiguration": NotRequired[RetrieveAndGenerateConfigurationTypeDef],
        "sessionConfiguration": NotRequired[RetrieveAndGenerateSessionConfigurationTypeDef],
        "sessionId": NotRequired[str],
    },
)
OrchestrationTraceTypeDef = TypedDict(
    "OrchestrationTraceTypeDef",
    {
        "invocationInput": NotRequired[InvocationInputTypeDef],
        "modelInvocationInput": NotRequired[ModelInvocationInputTypeDef],
        "observation": NotRequired[ObservationTypeDef],
        "rationale": NotRequired[RationaleTypeDef],
    },
)
PayloadPartTypeDef = TypedDict(
    "PayloadPartTypeDef",
    {
        "attribution": NotRequired[AttributionTypeDef],
        "bytes": NotRequired[bytes],
    },
)
TraceTypeDef = TypedDict(
    "TraceTypeDef",
    {
        "failureTrace": NotRequired[FailureTraceTypeDef],
        "orchestrationTrace": NotRequired[OrchestrationTraceTypeDef],
        "postProcessingTrace": NotRequired[PostProcessingTraceTypeDef],
        "preProcessingTrace": NotRequired[PreProcessingTraceTypeDef],
    },
)
TracePartTypeDef = TypedDict(
    "TracePartTypeDef",
    {
        "agentAliasId": NotRequired[str],
        "agentId": NotRequired[str],
        "agentVersion": NotRequired[str],
        "sessionId": NotRequired[str],
        "trace": NotRequired[TraceTypeDef],
    },
)
ResponseStreamTypeDef = TypedDict(
    "ResponseStreamTypeDef",
    {
        "accessDeniedException": NotRequired[AccessDeniedExceptionTypeDef],
        "badGatewayException": NotRequired[BadGatewayExceptionTypeDef],
        "chunk": NotRequired[PayloadPartTypeDef],
        "conflictException": NotRequired[ConflictExceptionTypeDef],
        "dependencyFailedException": NotRequired[DependencyFailedExceptionTypeDef],
        "internalServerException": NotRequired[InternalServerExceptionTypeDef],
        "resourceNotFoundException": NotRequired[ResourceNotFoundExceptionTypeDef],
        "returnControl": NotRequired[ReturnControlPayloadTypeDef],
        "serviceQuotaExceededException": NotRequired[ServiceQuotaExceededExceptionTypeDef],
        "throttlingException": NotRequired[ThrottlingExceptionTypeDef],
        "trace": NotRequired[TracePartTypeDef],
        "validationException": NotRequired[ValidationExceptionTypeDef],
    },
)
InvokeAgentResponseTypeDef = TypedDict(
    "InvokeAgentResponseTypeDef",
    {
        "completion": "EventStream[ResponseStreamTypeDef]",
        "contentType": str,
        "sessionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
