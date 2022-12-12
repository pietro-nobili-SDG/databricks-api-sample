"""Python version of the databricks API.

Extracted from the
[job API specification](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/api/latest/jobs).
"""
from typing import Any, Dict, List, Literal, Optional


class CronSchedule:
    """Schema of CronSchedule."""

    def __init__(
        self,
        quartz_cron_expression: str,
        timezone_id: str,
        pause_status: Optional[Literal["PAUSED", "UNPAUSED"]],
    ) -> None:
        """Build a CronSchedule.

        Args:
            quartz_cron_expression (str):
                A Cron expression using Quartz syntax that describes the
                schedule for a job. See
                [Cron Trigger](http://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html)
                for details.
            timezone_id (str):
                A Java timezone ID. The schedule for a job is resolved with
                respect to this timezone.
            pause_status (Optional[Literal['PAUSED', 'UNPAUSED']]):
                Indicate whether this schedule is paused or not.
        """
        self.quartz_cron_expression = quartz_cron_expression
        self.timezone_id = timezone_id
        if pause_status is not None:
            self.pause_status = pause_status


class JobEmailNotifications:
    """Schema of JobEmailNotifications."""

    def __init__(
        self,
        on_start: Optional[List[str]] = None,
        on_success: Optional[List[str]] = None,
        on_failure: Optional[List[str]] = None,
        no_alert_for_skipped_runs: Optional[bool] = None,
    ) -> None:
        if on_start is not None:
            self.on_start = on_start
        if on_success is not None:
            self.on_success = on_success
        if on_failure is not None:
            self.on_failure = on_failure
        if no_alert_for_skipped_runs is not None:
            self.no_alert_for_skipped_runs = no_alert_for_skipped_runs


class Library:
    """Schema of Library.

    Should be fancier, with pypi being a PythonPyPiLibrary.
    """

    def __init__(
        self,
        package: str,
    ) -> None:
        self.pypi = {"package": package}


class NotebookTask:
    """Schema of NotebookTask."""

    def __init__(
        self,
        notebook_path: str,
        source: Optional[str] = None,
        base_parameters: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Create a NotebookTask.

        Args:
            notebook_path (str):
                The path of the notebook to be run in the Azure Databricks
                workspace or remote repository. For notebooks stored in the
                Databricks workspace, the path must be absolute and begin with a
                slash. For notebooks stored in a remote repository, the path
                must be relative.
            source (Optional[str], optional):
                Optional location type of the notebook. When set to `WORKSPACE`,
                the notebook will be retrieved from the local Azure Databricks
                workspace. When set to `GIT`, the notebook will be retrieved
                from a Git repository defined in `git_source`. If the value is
                empty, the task will use `GIT` if `git_source` is defined and
                `WORKSPACE` otherwise.
            base_parameters (Optional[Dict[str, Any]], optional):
                Base parameters to be used for each run of this job.
                If the run is initiated by a call to
                [`run-now`](https://docs.microsoft.com/azure/databricks/dev-tools/api/latest/jobs#operation/JobsRunNow)
                with parameters specified, the two parameters maps are merged.
                If the same key is specified in `base_parameters`
                and in `run-now`, the value from `run-now` is used.

                Use
                [Task parameter variables](https://docs.microsoft.com/azure/databricks/jobs#parameter-variables)
                to set parameters containing information about job runs.

                If the notebook takes a parameter that is not specified in the job’s
                `base_parameters` or the `run-now` override parameters, the default
                value from the notebook is used.

                Retrieve these parameters in a notebook using
                [dbutils.widgets.get](https://docs.microsoft.com/azure/databricks/dev-tools/databricks-utils#dbutils-widgets).
        """
        self.notebook_path = notebook_path
        if source is not None:
            self.source = source
        if base_parameters is not None:
            self.base_parameters = base_parameters


class TaskDependency:
    """Schema of ``TaskDependencies``.

    ``TaskDependencies`` is actually an array of dependencies.
    But I don't know how to avoid having the name of the attribute as key

        self.dependencies = [ {'task_key': 'task00'}, ... ]

    Would produce in the json something like

        "dependencies": [ ... ]

    That is not part of the API, which wants, inside the ``JobTaskSettings``,
    directly the array at the key ``depends_on``.
    So we just pass a List[TaskDependency] to ``depends_on``.
    """

    def __init__(
        self,
        task_key: str,
    ) -> None:
        self.task_key = task_key


class JobTaskSettings:
    """Schema of JobTaskSettings."""

    def __init__(
        self,
        task_key: str,
        depends_on: Optional[List[TaskDependency]] = None,
        notebook_task: Optional[NotebookTask] = None,
        existing_cluster_id: Optional[str] = None,
        libraries: Optional[List[Library]] = None,
        max_retries: Optional[int] = None,
        min_retry_interval_millis: Optional[int] = None,
    ) -> None:
        """Initialize a JobTaskSettings.

        Args:
            task_key (str): This is the description for this task.
            depends_on (Optional[List[TaskDependency]], optional):
                An optional array of objects specifying the dependency graph of
                the task. All tasks specified in this field must complete
                successfully before executing this task.
            notebook_task (Optional[NotebookTask]): The notebook task to run.
            existing_cluster_id (Optional[str]): Cluster id to run the task on.
            libraries (Optional[List[Library]], optional):
                An optional list of libraries to be installed on the cluster
                that executes the task.
            max_retries (Optional[int]):
                An optional maximum number of times to retry an unsuccessful
                run. A run is considered to be unsuccessful if it completes with
                the `FAILED` result_state or `INTERNAL_ERROR` `life_cycle_state`.
                The value -1 means to retry indefinitely and the value 0 means
                to never retry. The default behavior is to never retry.
            min_retry_interval_millis (Optional[int]): 
                An optional minimal interval in milliseconds between the start
                of the failed run and the subsequent retry run. The default
                behavior is that unsuccessful runs are immediately retried.
        """
        self.task_key = task_key
        if depends_on is not None:
            self.depends_on = depends_on
        if notebook_task is not None:
            self.notebook_task = notebook_task
        if existing_cluster_id is not None:
            self.existing_cluster_id = existing_cluster_id
        if libraries is not None:
            self.libraries = libraries
        if max_retries is not None:
            self.max_retries = max_retries
        if min_retry_interval_millis is not None:
            self.min_retry_interval_millis = min_retry_interval_millis


class JobSettings:
    """Schema of JobSettings."""

    def __init__(
        self,
        name: Optional[str] = None,
        email_notifications: Optional[JobEmailNotifications] = None,
        timeout_seconds: Optional[int] = None,
        schedule: Optional[CronSchedule] = None,
        max_concurrent_runs: Optional[int] = None,
        tasks: Optional[List[JobTaskSettings]] = None,
    ) -> None:
        """Create a JobSettings.

        Args:
            name (Optional[str]): An optional name for the job.
            email_notifications (Optional[JobEmailNotifications]):
                An optional set of email addresses that is notified when runs of
                this job begin or complete as well as when this job is deleted.
            timeout_seconds (Optional[int]):
                An optional timeout applied to each run of this job.
            schedule (Optional[CronSchedule]):
                The cron schedule that triggered this run if it was triggered by
                the periodic scheduler.
            max_concurrent_runs (Optional[int]):
                An optional maximum allowed number of concurrent runs of the job.
            tasks (Optional[List[JobTaskSettings]]):
                The list of tasks performed by the run.
        """
        if name is not None:
            self.name = name
        if email_notifications is not None:
            self.email_notifications = email_notifications
        if timeout_seconds is not None:
            self.timeout_seconds = timeout_seconds
        if schedule is not None:
            self.schedule = schedule
        if max_concurrent_runs is not None:
            self.max_concurrent_runs = max_concurrent_runs
        if tasks is not None:
            self.tasks = tasks
