from dataclasses import dataclass
from .work_status import WorkStatus


@dataclass
class JobInfo:
    JobId: str = ""
    JobName: str = ""
    UserId: str = ""
    ServiceName: str = ""
    PoolId: str = ""
    EnvironmentId: str = ""
    Progress: float = 0.0
    Status: WorkStatus = WorkStatus.Unknown
    Message: str = ""
    StartTime: str = ""
    CompletionTime: str = ""
    TotalComputeSeconds: int = 0
    ClientReference: str = ""
