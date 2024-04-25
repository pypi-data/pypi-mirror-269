from collections import defaultdict
from dataclasses import dataclass, field
from enum import IntEnum, unique
from typing import Any


@unique
class ResultStorageTypes(IntEnum):
    """Result storage types"""

    # The storage of results from the work item is unknown.
    Unknown = 0
    # Results from the work item is stored in the user's container.
    UserContainer = 1
    # Results from the work item is stored in the Result Lake.
    ResultLake = 2


@dataclass
class WorkItemProperties:
    JobId: str = ""
    Id: str = ""
    Tag: str = ""
    ParentId: str = ""
    BatchNumber: int = 0
    ResultStorageType: ResultStorageTypes = ResultStorageTypes.Unknown
    WorkItemDirectory: str = ""
    Properties: dict[str, Any] = field(default_factory=lambda: defaultdict(dict))
