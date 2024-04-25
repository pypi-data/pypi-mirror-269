from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DataContainer:
    Version: int = 1
    Content: Optional[object] = None
    ContentType: Optional[str] = None


@dataclass
class Result:
    Id: str = ""
    JobId: str = ""
    Tag: str = ""
    ParentId: str = ""
    BatchNumber: int = 0
    Data: DataContainer = field(default_factory=DataContainer)

    @property
    def WorkItemId(self) -> str:
        return self.Id
