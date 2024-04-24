"""This module defines JSON models available in automation OpenFaaS lambdas."""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import sys
from typing import (Any, Callable, Dict, Generic, List, Literal, Optional, 
                    Sequence, TypeVar, Union)

if sys.version_info < (3, 11):
    from typing_extensions import NotRequired, TypeAlias, TypedDict
else:
    from typing import NotRequired, TypeAlias, TypedDict


##===================================================================
## Basic automation data types
##===================================================================


FileType: TypeAlias = Literal["REG", "DIR", "SYMLNK"]
ProtectionFlag: TypeAlias = Literal["data_protection", "metadata_protection"]
InheritancePath: TypeAlias = Literal["none", 
                                     "direct", 
                                     "ancestor", 
                                     "direct_and_ancestor"]


class AtmDataset(TypedDict):
    """
    JSON object describing dataset.

    Refer to the API specification for more information:
    https://onedata.org/#/home/api/latest/oneprovider?anchor=operation/get_dataset
    """

    state: Literal["attached", "detached"]
    datasetId: str
    parentId: Optional[str]
    rootFileId: str
    rootFileType: FileType
    rootFilePath: str
    rootFileDeleted: bool
    protectionFlags: List[ProtectionFlag]
    effectiveProtectionFlags: List[ProtectionFlag]
    creationTime: int
    archiveCount: int


class AtmFile(TypedDict, total=False):
    """
    JSON object describing a file in Onedata filesystem.

    Refer to the API specification for more information:
    https://onedata.org/#/home/api/latest/oneprovider?anchor=operation/get_attrs

    NOTE: dynamic fields like `xattr.*` are not typed due to limitations 
    of typing machinery.    
    """

    fileId: str
    index: str
    type: FileType
    activePermissionsType: Literal["posix", "acl"]
    posixPermissions: str
    acl: List[Dict]
    name: str
    conflictingName: Optional[str]
    path: str
    parentFileId: Optional[str] 
    displayGid: int
    displayUid: int
    atime: int
    mtime: int
    ctime: int
    size: Optional[int]
    isFullyReplicatedLocally: Optional[bool]
    localReplicationRate: float
    originProviderId: str
    directShareIds: List[str] 
    ownerUserId: str 
    hardlinkCount: int 
    symlinkValue: Optional[str]
    hasCustomMetadata: bool
    effProtectionFlags: List[ProtectionFlag]
    effDatasetProtectionFlags: List[ProtectionFlag]
    effDatasetInheritancePath: InheritancePath 
    effQosInheritancePath: InheritancePath 
    aggregateQosStatus: Literal["fulfilled", "pending", "impossible"]
    archiveRecallRootFileId: Optional[str]


class AtmGroup(TypedDict):
    """
    JSON object describing group.

    Refer to the API specification for more information:
    https://onedata.org/#/home/api/latest/onezone?anchor=operation/get_group
    """

    groupId: str
    name: str
    type: Literal["organization", "unit", "team", "role_holders"]


AtmObject: TypeAlias = Dict[str, Any]
"""
Generic JSON object
"""


class AtmRange(TypedDict):
    """
    JSON object describing a sequence of integers.

    AtmRange is a sequence of integers produced from the start to end by step.

    Fields
    --------
    end
        Value for which the sequence of integers will exclusively end.
        If step value is positive, end value must be higher than start value.
        Otherwise end value must be lower than start value.
    start
        Starting value for which the sequence of integers will inclusively start. 
        If step value is positive, start value must be lower than end value.
        Otherwise start value must be higher than end value.
        By default, it's set to: 0.
    step
        Value which specifies the size of incrementation or decremenation.
        It cannot be equal 0, and by default, it's set to: 1.

    Examples
    --------
    AtmRange(start=10, end=20, step=2) -> [10, 12, 14, 16, 18]
    AtmRange(start=10, end=-10, step=-4) -> [10, 6, 2, -2, -6]
    AtmRange(end=10, step=6) -> [0, 6]
    AtmRange(end=5) -> [0, 1, 2, 3, 4]
    AtmRange(start=4, end=-1, step=-1) -> [4, 3, 2, 1, 0]
    AtmRange(start=5, end=5, step=-2) -> []
    AtmRange(start=4, end=5, step=-2) -> Invalid!
    """

    end: int
    start: NotRequired[int]
    step: NotRequired[int]


class AtmTimeSeriesMeasurement(TypedDict):
    """
    JSON object describing time series measurement.

    Time series measurement is a named value-timestamp pair which expresses some property
    that can be dynamically changing (like file size, network speed, etc.).
    Such measurements can be aggregated within time series stores and
    serve as a data source for GUI charts.
    """

    tsName: str
    timestamp: int
    value: float


##===================================================================
## Job specific automation data types
##===================================================================


AtmHeartbeatCallback: TypeAlias = Callable[[], None]
LogLevel: TypeAlias = Literal["debug", 
                              "info", 
                              "notice", 
                              "warning", 
                              "error", 
                              "critical", 
                              "alert", 
                              "emergency"]


class AtmException(TypedDict):
    exception: Union[float, str, AtmObject]


C = TypeVar("C")


class AtmJobBatchRequestCtx(TypedDict, Generic[C]):
    """
    JSON object describing job batch request context.

    Fields
    --------
    userId
        Id of the scheduling user.
    spaceId
        Id of the space in context of which the workflow is executed.
    atmWorkflowExecutionId
        Workflow execution Id.
    oneproviderDomain
        Domain of job scheduling Oneprovider.
    oneproviderId
        Id of job scheduling Oneprovider.
    onezoneDomain
        The domain of the Onezone service that manages the Onedata environment.
    accessToken
        Token used to authorize operations in Onedata.

        Refer to the API specification for more information:
        https://onedata.org/#/home/documentation/latest/doc/using_onedata/tokens[access-tokens].html
    heartbeatUrl
        The target url for sending heartbeats (used, inter alia, by heartbeat_callback).
    timeoutSeconds
        The time interval from last heartbeat after which job batch is marked as failed.
    logLevel
        Level controling the amount of information recorded in audit logs as only logs 
        with severity equal or higher to this level will be stored. 
    config
        User defined task configuration.
    """

    userId: str
    spaceId: str
    atmWorkflowExecutionId: str
    oneproviderDomain: str
    oneproviderId: str
    onezoneDomain: str
    accessToken: str
    heartbeatUrl: str
    timeoutSeconds: int
    logLevel: LogLevel
    config: C


A = TypeVar("A")


class AtmJobBatchRequest(TypedDict, Generic[A, C]):
    """
    JSON object describing job batch request.

    Fields
    --------
    ctx
        Context of job batch request.
    argsBatch
        List of JSON objects, each carrying arguments 
        of a single job (lambda input).
    """

    ctx: AtmJobBatchRequestCtx[C]
    argsBatch: List[A]


R = TypeVar("R")


class AtmJobBatchResponse(TypedDict, Generic[R]):
    """
    JSON object describing job batch response.

    Fields
    --------
    resultsBatch
        List of JSON objects, each carrying results 
        of a single job (lambda output).
        Length of a list must be equal to length of corresponding
        The length of this list must be equal to the length of 
        the corresponding AtmJobBatchRequest.argsBatch.
        However, if the lambda returns empty results for each job, 
        the resultsBatch can be set to None.
    """

    resultsBatch: Optional[Sequence[Optional[Union[AtmException, R]]]]
