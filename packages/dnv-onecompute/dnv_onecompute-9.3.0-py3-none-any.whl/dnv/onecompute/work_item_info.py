# Include a __future__ import so that all annotations by default are forward-declared
from __future__ import annotations

from dataclasses import dataclass, field
from .work_status import WorkStatus


@dataclass
class WorkItemInfo:
    Id: str = ""
    ParentId: str = ""
    JobId: str = ""
    """Progress is defined as a fraction of 1 where 0 = no progress and 1 = complete."""
    Progress: float = 0.0
    Status: WorkStatus = WorkStatus.Unknown
    Message: str = ""
    """The duration of the work in milliseconds."""
    WorkDuration: int = 0
    WorkItemErrorInfo: list[WorkItemInfo] = field(default_factory=list)
