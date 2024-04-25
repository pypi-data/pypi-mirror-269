from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Any, Optional


@unique
class TaskRoles(int, Enum):
    """
    Enum for representing the different task roles.

    This enum is used to represent the different roles that a task can have in a job.

    Attributes:
        Normal: Represents a normal task.
        ReductionTask: Represents a reduction task.
        JobPreparationTask: Represents a job preparation task.
        JobReleaseTask: Represents a job release task.
    """

    Normal = 0
    ReductionTask = 1
    JobPreparationTask = 2
    JobReleaseTask = 3


@unique
class FailureStrategy(int, Enum):
    """
    An enumeration of failure strategies for a process.

    Attributes:
        FailOnError: A strategy where the work unit will fail immediately on encountering an error.
        ContinueOnError: A strategy where the work unit will continue despite encountering errors.
    """

    FailOnError = 1
    ContinueOnError = 2


class Encode(ABC):
    """
    Abstract Base Class for encoding objects.

    This class provides a blueprint for encoding objects into dictionaries.
    Concrete subclasses are expected to implement the `encode` method.

    Attributes:
        None

    Methods:
        encode: Encodes an object into a dictionary.
    """

    @abstractmethod
    def encode(self) -> dict[str, Any]:
        """
        Encode an object into a dictionary.

        This method must be implemented by concrete subclasses.

        Returns:
            A dictionary representation of the object.
        """


class TypeMeta(Encode):
    """
    Class for encoding objects with type information.

    This class extends the `Encode` abstract base class and adds type information to the encoded
    dictionary. Concrete subclasses are expected to implement the `type` property.

    Attributes:
        None

    Methods:
        __init__: Initializes the object and adds type information to the encoded dictionary.
        __str__: Returns the string representation of the encoded dictionary.
        encode: Encodes an object into a dictionary and filters properties that are 'None'.
        type: Abstract property to retrieve the type of the object.
    """

    def __init__(self):
        """
        Initializes the object and adds type information to the encoded dictionary.
        """
        if self.type.strip():
            self.__dict__["$type"] = self.type

    def __str__(self) -> str:
        """
        Returns the string representation of the encoded dictionary.

        Returns:
            A string representation of the encoded dictionary.
        """
        return str(self.encode())

    def encode(self) -> dict[str, Any]:
        """
        Encodes an object into a dictionary and filters properties that are 'None'.

        Returns:
            A dictionary representation of the object without properties that are 'None'.
        """
        filtered: dict[str, Any] = {
            k: v for k, v in self.__dict__.items() if v is not None and not k[0] == "_"
        }
        return filtered

    @property
    @abstractmethod
    def type(self) -> str:
        """
        Abstract property to retrieve the type of the object.

        Returns:
            The type of the object as a string.
        """


class SchedulingOptions(TypeMeta):
    """
    A data class representing scheduling options for a process.
    """

    def __init__(
        self,
        failure_strategy: FailureStrategy = FailureStrategy.FailOnError,
        max_task_retry_count: int = 0,
        work_unit_batch_size: int = 1,
    ):
        """
        Initializes a new instance of the SchedulingOptions class.

        Args:
            max_task_retry_count (int): The maximum number of times to retry a failed task.
                It controls the number of retries for the task executable due to a nonzero exit
                code. The Batch service will try the task once, and may then retry up to this
                limit. For example, if the maximum retry count is 3, Batch tries the task up to
                4 times (one initial try and 3 retries). If the maximum retry count is 0, the Batch
                service does not retry the task after the first attempt. If the maximum retry count
                is -1, the Batch service retries the task without limit. Resource files and
                application packages are only downloaded again if the task is retried on a new
                compute node.
            failure_strategy (FailureStrategy): The strategy to use when encountering failures.
            work_unit_batch_size (int): It is the proposed number of work units that each worker
                will be assigned. Default is 1.
        """
        super().__init__()
        self.FailureStrategy: FailureStrategy = failure_strategy
        self.MaxTaskRetryCount: int = max_task_retry_count
        self.WorkUnitBatchSize: int = work_unit_batch_size

    @property
    def type(self) -> str:
        return (
            "DNVGL.One.Compute.Core.FlowModel.SchedulingOptions, DNVGL.One.Compute.Core"
        )


@dataclass
class FileSelectionOptions:
    """A class for selecting and filtering files within a folder.

    Attributes:
        directory (str): A string representing the directory where files will be searched.
        include_files (list[str]): A list of strings representing file patterns to include in the
            search. Defaults to ["**/*.*"].
        exclude_files ([list[str]]): A list of strings representing file patterns to exclude from
            the search. Defaults to [].
    """

    directory: str
    include_files: list[str] = field(default_factory=lambda: ["**/*.*"])
    exclude_files: list[str] = field(default_factory=lambda: [])


class DataContainer(TypeMeta):
    def __init__(self, data: object = None):
        super().__init__()
        self.Version = 1
        self.Content = data

    @property
    def type(self) -> str:
        return ""

    @property
    def content(self) -> object:
        return self.Content

    @content.setter
    def content(self, value: object):
        self.Content = value

    @property
    def version(self) -> int:
        return self.Version

    @version.setter
    def version(self, value: int):
        self.Version = value


class StorageSpecification(TypeMeta):
    def __init__(self, directory: str = ""):
        super().__init__()
        self.Directory = directory

    @property
    def directory(self) -> str:
        return self.Directory

    @directory.setter
    def directory(self, value: str):
        self.Directory = value


class BlobDirectorySpecification(StorageSpecification):
    def __init__(self, container_url: str = "", directory: str = ""):
        super().__init__(directory=directory)
        self.ContainerUrl = container_url

    @property
    def type(self) -> str:
        return "DNVGL.One.Compute.Core.FlowModel.DataTransfer.BlobDirectorySpecification, DNVGL.One.Compute.Core"

    @property
    def container_url(self) -> str:
        return self.ContainerUrl

    @container_url.setter
    def container_url(self, value: str):
        self.ContainerUrl = value


class FileSystemDirectorySpecification(StorageSpecification):
    def __init__(self, directory: str = ""):
        super().__init__(directory=directory)

    @property
    def type(self) -> str:
        return "DNVGL.One.Compute.Core.FlowModel.DataTransfer.FileSystemDirectorySpecification, DNVGL.One.Compute.Core"


class ResultLakeStorageSpecification(StorageSpecification):
    @property
    def type(self) -> str:
        return "DNVGL.One.Compute.Core.FlowModel.DataTransfer.ResultLakeStorageSpecification, DNVGL.One.Compute.Core"


class FileTransferSpecification(TypeMeta):
    def __init__(
        self,
        source_specification: Optional[StorageSpecification] = None,
        destination_specification: Optional[StorageSpecification] = None,
        selected_files: Optional[list[str]] = None,
        excluded_files: Optional[list[str]] = None,
    ):
        super().__init__()
        self.SourceSpecification = source_specification
        self.DestinationSpecification = destination_specification
        self.SelectedFiles = selected_files or []
        self.ExcludedFiles = excluded_files or []

    @property
    def type(self) -> str:
        return "DNVGL.One.Compute.Core.FlowModel.DataTransfer.FileTransferSpecification, DNVGL.One.Compute.Core"

    @property
    def source_specification(self) -> StorageSpecification | None:
        return self.SourceSpecification

    @source_specification.setter
    def source_specification(self, value: StorageSpecification):
        self.SourceSpecification = value

    @property
    def destination_specification(self) -> StorageSpecification | None:
        return self.DestinationSpecification

    @destination_specification.setter
    def destination_specification(self, value: StorageSpecification):
        self.DestinationSpecification = value

    @property
    def selected_files(self) -> list[str]:
        return self.SelectedFiles

    @selected_files.setter
    def selected_files(self, value: list[str]):
        self.SelectedFiles = value

    @property
    def excluded_files(self) -> list[str]:
        return self.ExcludedFiles

    @excluded_files.setter
    def excluded_files(self, value: list[str]):
        self.ExcludedFiles = value


class FlowModelObject(TypeMeta):
    def __init__(self):
        super().__init__()
        self.properties: dict[str, Any] = {}

    @property
    def property_dictionary(self) -> dict[str, Any]:
        return self.properties

    @property_dictionary.setter
    def property_dictionary(self, value: dict[str, Any]):
        self.properties = value

    @property
    def batch_number(self) -> int:
        return self.BatchNumber

    @batch_number.setter
    def batch_number(self, value: int):
        self.BatchNumber = value


class WorkItem(FlowModelObject):
    def __init__(self, work_item_id: str = ""):
        super().__init__()
        self.Tag: Optional[str] = None
        self.JobId: Optional[str] = None
        self.ParentId: Optional[str] = None
        self.id = work_item_id or str(uuid.uuid4())

    @property
    def type(self) -> str:
        return ""

    @property
    def tag(self) -> Optional[str]:
        return self.Tag

    @tag.setter
    def tag(self, value: str):
        self.Tag = value

    @property
    def job_id(self) -> Optional[str]:
        return self.JobId

    @job_id.setter
    def job_id(self, value: str):
        self.JobId = value

    @property
    def parent_id(self) -> Optional[str]:
        return self.ParentId

    @parent_id.setter
    def parent_id(self, value: str):
        self.ParentId = value


class WorkUnit(WorkItem):
    def __init__(
        self,
        data: object = None,
        work_unit_id: str = "",
    ):
        super().__init__(work_unit_id)
        self.TaskRole = TaskRoles.Normal
        self.Data = DataContainer(data)
        self._input_file_selectors = list[FileSelectionOptions]()
        self._output_file_selectors = list[FileSelectionOptions]()

    @property
    def type(self) -> str:
        return "DNVGL.One.Compute.Core.FlowModel.WorkUnit, DNVGL.One.Compute.Core"

    @property
    def command(self) -> str:
        return self.Command

    @command.setter
    def command(self, value: str):
        self.Command = value

    @property
    def request(self) -> str:
        return self.Request

    @request.setter
    def request(self, value: str):
        self.Request = value

    @property
    def service_name(self) -> str:
        return self.ServiceName

    @service_name.setter
    def service_name(self, value: str):
        self.ServiceName = value

    @property
    def dependencies(self) -> list[str]:
        return self.Dependencies

    @dependencies.setter
    def dependencies(self, value: list[str]):
        self.Dependencies = value

    @property
    def input_files(self) -> list[str]:
        return self.InputFiles

    @input_files.setter
    def input_files(self, value: list[str]):
        self.InputFiles = value

    @property
    def input_file_specifications(self) -> list[FileTransferSpecification]:
        return self.InputFileSpecifications

    @input_file_specifications.setter
    def input_file_specifications(self, value: list[FileTransferSpecification]):
        self.InputFileSpecifications = value

    @property
    def output_file_specifications(self) -> list[FileTransferSpecification]:
        return self.OutputFileSpecifications

    @output_file_specifications.setter
    def output_file_specifications(self, value: list[FileTransferSpecification]):
        self.OutputFileSpecifications = value

    @property
    def task_role(self) -> TaskRoles:
        return self.TaskRole

    @task_role.setter
    def task_role(self, value: TaskRoles):
        self.TaskRole = value

    @property
    def worker_contract_name(self) -> str:
        return self.WorkerContractName

    @worker_contract_name.setter
    def worker_contract_name(self, value: str):
        self.WorkerContractName = value

    @property
    def worker_assembly_filename(self) -> str:
        return self.WorkerAssemblyFileName

    @worker_assembly_filename.setter
    def worker_assembly_filename(self, value: str):
        self.WorkerAssemblyFileName = value

    @property
    def data(self) -> DataContainer:
        return self.Data

    @data.setter
    def data(self, value: DataContainer):
        self.Data = value

    @property
    def input_file_selectors(self) -> list[FileSelectionOptions]:
        return self._input_file_selectors

    @property
    def output_file_selectors(self) -> list[FileSelectionOptions]:
        return self._output_file_selectors

    @property
    def working_directory(self) -> str:
        return self.workingDirectory

    @working_directory.setter
    def working_directory(self, value: str):
        self.workingDirectory = value

    def input_directory(
        self,
        directory: str,
        include_files: Optional[list[str]] = None,
        exclude_files: Optional[list[str]] = None,
    ) -> WorkUnit:
        include_files = include_files or ["**/*.*"]
        exclude_files = exclude_files or []
        self._input_file_selectors.append(
            FileSelectionOptions(directory, include_files, exclude_files)
        )
        return self

    def output_directory(
        self,
        directory: str,
        include_files: Optional[list[str]] = None,
        exclude_files: Optional[list[str]] = None,
    ) -> WorkUnit:
        include_files = include_files or ["**/*.*"]
        exclude_files = exclude_files or []
        self._output_file_selectors.append(
            FileSelectionOptions(directory, include_files, exclude_files)
        )
        return self


class CompositeWork(WorkItem):
    def __init__(self, parallel: bool, work_items: Optional[list[WorkItem]] = None):
        super().__init__()
        self.Parallel = parallel
        self.WorkItems = work_items or []

    @property
    def type(self) -> str:
        return "DNVGL.One.Compute.Core.FlowModel.CompositeWork, DNVGL.One.Compute.Core"

    @property
    def parallel(self) -> bool:
        return self.Parallel

    @parallel.setter
    def parallel(self, value: bool):
        self.Parallel = value

    @property
    def work_items(self) -> list[WorkItem]:
        return self.WorkItems

    @work_items.setter
    def work_items(self, value: list[WorkItem]):
        self.WorkItems = value


class ParallelWork(CompositeWork):
    def __init__(self, work_items: Optional[list[WorkItem] | list[WorkUnit]] = None):
        super().__init__(True, work_items)
        self.ReductionTask: Optional[WorkUnit] = None

    @property
    def type(self) -> str:
        return "DNVGL.One.Compute.Core.FlowModel.ParallelWork, DNVGL.One.Compute.Core"

    @property
    def reduction_task(self) -> Optional[WorkUnit]:
        return self.ReductionTask

    @reduction_task.setter
    def reduction_task(self, value: Optional[WorkUnit]):
        self.ReductionTask = value
        if self.ReductionTask:
            self.ReductionTask.TaskRole = TaskRoles.ReductionTask

    def add(
        self,
        item: list[TypeMeta] | TypeMeta,
        work_unit_id: str = "",
    ) -> WorkUnit:
        work_unit = WorkUnit(item, work_unit_id)
        self.WorkItems.append(work_unit)
        return work_unit


class Job(FlowModelObject):
    def __init__(self, job_id: str | None = None, user_id: str | None = None):
        super().__init__()
        self.UserId = user_id
        self.JobId = str(uuid.uuid4()) if job_id is None else job_id
        self.JobPreparationWork: Optional[WorkUnit] = None
        self.JobReleaseWork: Optional[WorkUnit] = None
        # Below item is there in the corresponding class of C# code
        # DeploymentModel

    @property
    def type(self) -> str:
        return "DNVGL.One.Compute.Core.FlowModel.Job, DNVGL.One.Compute.Core"

    @property
    def user_id(self) -> str | None:
        return self.UserId

    @user_id.setter
    def user_id(self, value: str):
        self.UserId = value

    @property
    def work(self) -> WorkItem:
        return self.Work

    @work.setter
    def work(self, value: WorkItem):
        self.Work = value

    @property
    def client_reference(self) -> str:
        return self.ClientReference

    @client_reference.setter
    def client_reference(self, value: str):
        self.ClientReference = value

    @property
    def name(self) -> str:
        return self.Name

    @name.setter
    def name(self, value: str):
        self.Name = value

    @property
    def service_name(self) -> str:
        return self.ServiceName

    @service_name.setter
    def service_name(self, value: str):
        self.ServiceName = value

    @property
    def tags(self) -> str:
        return self.Tags

    @tags.setter
    def tags(self, value: str):
        self.Tags = value

    @property
    def pool_id(self) -> Optional[str]:
        return self.PoolId

    @pool_id.setter
    def pool_id(self, value: Optional[str]):
        self.PoolId = value

    @property
    def timeout_seconds(self) -> Optional[str]:
        return self.TimeoutSeconds

    @timeout_seconds.setter
    def timeout_seconds(self, value: Optional[str]):
        self.TimeoutSeconds = value

    @property
    def message_queues(self) -> list[str]:
        return self.MessageQueues

    @message_queues.setter
    def message_queues(self, value: list[str]):
        self.MessageQueues = value

    @property
    def job_preparation_work(self) -> Optional[WorkUnit]:
        return self.JobPreparationWork

    @job_preparation_work.setter
    def job_preparation_work(self, value: Optional[WorkUnit]):
        self.JobPreparationWork = value
        if self.JobPreparationWork:
            self.JobPreparationWork.TaskRole = TaskRoles.JobPreparationTask

    @property
    def job_release_work(self) -> Optional[WorkUnit]:
        return self.JobReleaseWork

    @job_release_work.setter
    def job_release_work(self, value: Optional[WorkUnit]):
        self.JobReleaseWork = value
        if self.JobReleaseWork:
            self.JobReleaseWork.TaskRole = TaskRoles.JobReleaseTask

    @property
    def scheduling_options(self) -> Optional[SchedulingOptions]:
        return self.SchedulingOptions

    @scheduling_options.setter
    def scheduling_options(self, value: Optional[SchedulingOptions]):
        self.SchedulingOptions = value
