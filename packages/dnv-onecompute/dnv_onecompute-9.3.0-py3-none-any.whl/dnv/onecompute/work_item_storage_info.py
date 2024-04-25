from dataclasses import dataclass


@dataclass
class WorkItemStorageInfo:
    """
    Represents storage information for a work item.

    Attributes:
        WorkItemId (str): The ID of the work item.
        ContainerUri (str): The URI of the container.
    """

    WorkItemId: str = ""
    ContainerUri: str = ""
