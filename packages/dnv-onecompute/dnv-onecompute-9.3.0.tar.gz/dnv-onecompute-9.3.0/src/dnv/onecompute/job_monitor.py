import asyncio
import contextlib

from abc import ABC, abstractmethod
from cancel_token import CancellationToken
from dataclasses import dataclass
from .event import Event
from .one_compute_client import OneComputeClient
from .job_info import JobInfo
from .work_status import WorkStatus
from .work_item_info import WorkItemInfo


@dataclass
class JobEventArgs:
    job_id: str = ""
    work_status: WorkStatus = WorkStatus.Unknown
    progress: float = 0.0
    message: str = ""


@dataclass
class WorkItemEventArgs:
    job_id: str = ""
    work_item_id: str = ""
    work_status: WorkStatus = WorkStatus.Unknown
    progress: float = 0.0
    message: str = ""


class IJobMonitor(ABC):
    @property
    @abstractmethod
    def job_status_changed(self) -> Event:
        pass

    @property
    @abstractmethod
    def job_progress_changed(self) -> Event:
        pass

    @property
    @abstractmethod
    def work_item_status_changed(self) -> Event:
        pass

    @property
    @abstractmethod
    def work_item_progress_changed(self) -> Event:
        pass

    @abstractmethod
    async def await_job_termination_async(
        self, cancellationToken: CancellationToken = None
    ) -> WorkStatus:
        pass


class JobMonitor(IJobMonitor):
    def __init__(self, one_compute_platform_client: OneComputeClient):
        super().__init__()

        self._job_termination_event = asyncio.Event()

        self._workitem_status_notified: dict[str, WorkItemInfo] = {}
        self._job_status_notified: dict[str, JobEventArgs] = {}

        self._job_status_changed = Event()
        self._job_progress_changed = Event()
        self._work_item_status_changed = Event()
        self._work_item_progress_changed = Event()

        self._one_compute_platform_client = one_compute_platform_client
        self._job_status = WorkStatus.Unknown
        self._job_status_changed += self.__job_status_changed

    @property
    def job_status_changed(self) -> Event:
        return self._job_status_changed

    @property
    def job_progress_changed(self) -> Event:
        return self._job_progress_changed

    @property
    def work_item_status_changed(self) -> Event:
        return self._work_item_status_changed

    @property
    def work_item_progress_changed(self) -> Event:
        return self._work_item_progress_changed

    async def await_job_termination_async(
        self, cancellationToken: CancellationToken = None
    ) -> WorkStatus:
        if WorkStatus.is_terminal(self._job_status):
            self._workitem_status_notified.clear()
            self._job_status_notified.clear()
            return self._job_status
        while not await self.__event_wait(self._job_termination_event, 1):
            pass
        self._workitem_status_notified.clear()
        self._job_status_notified.clear()
        return self._job_status

    async def begin_monitor_job(self, job_id: str, cancellationToken: object = None):
        async def wait():
            await asyncio.sleep(
                self._one_compute_platform_client.polling_interval_seconds * 1
            )

        await asyncio.sleep(1)
        while True:
            try:
                job_info = await self._one_compute_platform_client.get_job_status_async(
                    job_id
                )
                if job_info == None:
                    await wait()
                    continue

                work_items_info = (
                    await self._one_compute_platform_client.get_workitems_info_async(
                        job_id
                    )
                )
                if work_items_info == None or work_items_info == []:
                    await wait()
                    continue

                await self.__process_work_items_event(work_items_info)
                await self.__process_job_event(job_info)

                if WorkStatus.is_terminal(job_info.Status):
                    break
            except Exception as e:
                print(e)
                self._job_termination_event.set()
                break
            await wait()

    async def __process_work_items_event(self, workitems_info: list[WorkItemInfo]):
        for work_item in workitems_info:
            is_terminal = WorkStatus.is_terminal(work_item.Status)
            workitem_event_args = WorkItemEventArgs(
                job_id=work_item.JobId,
                work_item_id=work_item.Id,
                work_status=work_item.Status,
                message=work_item.Message,
                progress=1.0 if is_terminal else work_item.Progress,
            )
            if (
                work_item.Id in self._workitem_status_notified
                and self._workitem_status_notified[work_item.Id] == workitem_event_args
            ):
                continue
            self._workitem_status_notified[work_item.Id] = workitem_event_args
            if is_terminal:
                await self.work_item_status_changed(
                    self._one_compute_platform_client, workitem_event_args
                )
            else:
                await self.work_item_progress_changed(
                    self._one_compute_platform_client, workitem_event_args
                )

    async def __process_job_event(self, job_info: JobInfo):
        is_terminal = WorkStatus.is_terminal(job_info.Status)
        job_event_args = JobEventArgs(
            job_id=job_info.JobId,
            work_status=job_info.Status,
            message=job_info.Message,
            progress=1.0 if is_terminal else job_info.Progress,
        )
        if (
            job_info.JobId in self._job_status_notified
            and self._job_status_notified[job_info.JobId] == job_event_args
        ):
            return
        self._job_status_notified[job_info.JobId] = job_event_args
        if is_terminal:
            await self.job_status_changed(
                self._one_compute_platform_client, job_event_args
            )
        else:
            await self.job_progress_changed(
                self._one_compute_platform_client, job_event_args
            )

    async def __job_status_changed(self, sender: object, e: JobEventArgs):
        self._job_status = e.work_status
        if WorkStatus.is_terminal(self._job_status) is True:
            self._job_termination_event.set()

    async def __event_wait(self, evt: asyncio.Event, timeout: int):
        with contextlib.suppress(asyncio.TimeoutError):
            await asyncio.wait_for(evt.wait(), timeout)
        return evt.is_set()
