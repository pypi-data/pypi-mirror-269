from dataclasses import dataclass


@dataclass(frozen=True)
class WebAPIsTemplate:
    """A class containing constants for commonly used web API endpoints."""

    JOBS = "/api/v1/jobs"
    JOBS_INFO = "/api/v1/jobs/{job_id}"
    JOBS_CANCEL = "/api/v1/jobs/{job_id}/cancel"
    JOBS_DELETE = "/api/v1/jobs/{job_id}/delete"
    WORK_ITEMS = "/api/v1/jobs/{job_id}/workitems"
    WORK_ITEM_PROPERTIES_FOR_JOB = "/api/v1/jobs/{job_id}/workitemproperties"
    WORK_ITEM_PROPERTIES = "/api/v1/jobs/{job_id}/workitemproperties/{workitem_id}"
    WORK_ITEM_RESULTS = "/api/v1/jobs/{job_id}/workitemresults"
    WORK_ITEM_RESULT = "/api/v1/jobs/{job_id}/workitemresults/{workitem_id}"
    WORK_ITEM_STORAGE_INFO = "/api/v1/jobs/job/{job_id}/container/{container_name}"
    WORK_ITEM_STORAGE_CONTAINER_URI = (
        "/api/v1/jobs/{job_id}/{workitem_id}/{container_name}"
    )
    BLOBS = "/api/v1/blobs/{container_name}"
    CONTAINERS = "/api/v1/containers"
    CONTAINER_URI = "/api/v1/containers/{container_name}/{days}"

    @staticmethod
    def work_item_properties(job_id: str, workitem_id: str) -> str:
        """Returns the API endpoint for retrieving properties of a work item.

        If workitem_id is provided and not empty, the endpoint for the specified
        work item is returned. Otherwise, the endpoint for retrieving properties
        of all work items in the specified job is returned.

        Args:
            job_id (str): The ID of the job containing the work item(s).
            workitem_id (str): The ID of the work item to retrieve properties for,
                or an empty string to retrieve properties for all work items in the job.

        Returns:
            str: The API endpoint for retrieving work item properties.
        """
        return (
            WebAPIsTemplate.WORK_ITEM_PROPERTIES.format(
                job_id=job_id, workitem_id=workitem_id
            )
            if workitem_id and workitem_id.strip()
            else WebAPIsTemplate.WORK_ITEM_PROPERTIES_FOR_JOB.format(job_id=job_id)
        )
