from enum import IntEnum, unique


@unique
class WorkStatus(IntEnum):
    """Unknown status."""

    Unknown = -1  # 0xFFFFFFFF
    """The work item has been created."""
    Created = 0
    """The work item has been scheduled for execution, but execution has not started."""
    Pending = 1
    """The work item is being processed."""
    Executing = 2
    """The processing of the work item has been suspended"""
    Suspended = 3
    """The processing of the work item has completed successfully and is terminated."""
    Completed = 4
    """The processing of the work item is failing."""
    Faulting = 5
    """The processing of the work item has faulted and is terminated."""
    Faulted = 6
    """The user has requested to abort the processing of the work item."""
    Aborting = 7
    """The processing of the work item has been aborted and is terminated."""
    Aborted = 8

    @staticmethod
    def is_terminal(val) -> bool:
        return (
            val == WorkStatus.Aborted
            or val == WorkStatus.Faulted
            or val == WorkStatus.Completed
        )
