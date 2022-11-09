"""Sample interface with databricks API."""
from typing import List, Literal, Optional
import jsons
from loguru import logger as lg

from utils import jd


class CronSchedule:
    """Schema of CronSchedule.

    TODO: make optional fields Optional like JobSettings.
    """

    def __init__(
        self,
        quartz_cron_expression: str,
        timezone_id: str,
        pause_status: Literal["PAUSED", "UNPAUSED"] = "UNPAUSED",
    ) -> None:
        # A Cron expression using Quartz syntax that describes the schedule for a job.
        self.quartz_cron_expression = quartz_cron_expression
        # A Java timezone ID. The schedule for a job is resolved with respect to this timezone.
        self.timezone_id = timezone_id
        # Indicate whether this schedule is paused or not.
        self.pause_status = pause_status


class JobEmailNotifications:
    """Schema of JobEmailNotifications.

    TODO: make optional fields Optional like JobSettings.
    """

    def __init__(
        self,
        on_start: List[str] = [],
        on_success: List[str] = [],
        on_failure: List[str] = [],
        no_alert_for_skipped_runs: bool = False,
    ) -> None:
        self.on_start = on_start
        self.on_success = on_success
        self.on_failure = on_failure
        self.no_alert_for_skipped_runs = no_alert_for_skipped_runs


class JobSettings:
    """Schema of JobSettings."""

    def __init__(
        self,
        name: Optional[str] = None,
        email_notifications: Optional[JobEmailNotifications] = None,
        timeout_seconds: Optional[int] = None,
        schedule: Optional[CronSchedule] = None,
        max_concurrent_runs: Optional[int] = None,
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


def sample_create_job() -> None:
    """Create a job."""
    schedule = CronSchedule(
        quartz_cron_expression="0 0 7 * * ?",
        timezone_id="Europe/Amsterdam",
        pause_status="UNPAUSED",
    )
    email_notifications = JobEmailNotifications(
        on_start=["mail@s1.com"],
        on_success=["mail@s1.com", "mail@s2.com"],
        on_failure=["mail@s1.com", "mail@s2.com"],
    )
    job = JobSettings(
        name="job_name",
        email_notifications=email_notifications,
        timeout_seconds=0,
        schedule=schedule,
        max_concurrent_runs=1,
    )
    lg.info(
        "job: \n{}",
        jd(
            jsons.dump(job, strip_privates=True),
            indent=4,
        ),
    )


if __name__ == "__main__":
    sample_create_job()
