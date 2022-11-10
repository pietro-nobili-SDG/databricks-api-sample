"""Sample interface with databricks API."""
import jsons
from loguru import logger as lg

from databricks_api import (
    CronSchedule,
    JobEmailNotifications,
    JobSettings,
    JobTaskSettings,
    Library,
    NotebookTask,
    TaskDependency,
)
from utils import jd


def sample_create_job_auto_task() -> None:
    """Create a job by automatically assembling the tasks."""
    ########
    # TASK #
    ########

    # static for all tasks
    libraries = [
        Library("pyarrow==8.0.0"),
        Library("snowflake-sqlalchemy"),
        Library("tqdm"),
    ]
    notebook_path = "/the/path"
    source = "WORKSPACE"

    params_by_cluster = {
        "cluster_1": [
            {"line": 10, "gender": "W"},
            {"line": 10, "gender": "M"},
        ],
        "cluster_2": [
            {"line": 30, "gender": "G"},
            {"line": 30, "gender": "B"},
        ],
        # "cluster_3": [
        #     {"line": 15, "gender": "W"},
        #     {"line": 15, "gender": "M"},
        #     {"line": 16, "gender": "W"},
        #     {"line": 16, "gender": "M"},
        # ],
    }
    shared_params = {"season": "2023-3"}

    tasks = []
    for cluster_id, params in params_by_cluster.items():

        # new cluster, reset state
        is_first_task_for_cluster = True
        last_task_key = ""

        for p in params:

            # build the task name
            task_key = f"{p['line']}{p['gender']}"

            # add the season to the params
            # which is modifying the list so I kinda hate it
            p.update(shared_params)

            # build the task
            notebook_task = NotebookTask(
                notebook_path=notebook_path,
                source=source,
                base_parameters=p,
            )

            # build the libraries if needed
            # and the depends on object
            if is_first_task_for_cluster:
                # first task must wait for this libraries
                lib = libraries
                # first task depends on nothing
                do = None
                is_first_task_for_cluster = False
            else:
                # arguably other tasks should require libraries
                # even if those are already installed on the cluster by now
                lib = None
                # other tasks depend on the previous
                do = [TaskDependency(last_task_key)]

            # build the task
            task = JobTaskSettings(
                task_key=task_key,
                depends_on=do,
                notebook_task=notebook_task,
                existing_cluster_id=cluster_id,
                libraries=lib,
            )
            tasks.append(task)

            last_task_key = task_key

    #######
    # JOB #
    #######

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
        schedule=schedule,
        tasks=tasks,
        max_concurrent_runs=1,
    )

    # dump the result
    lg.info(
        "job: \n{}",
        jd(
            jsons.dump(job, strip_privates=True),
            indent=4,
        ),
    )


def sample_create_job_manual() -> None:
    """Create a job by assembling the pieces manually."""
    ########
    # TASK #
    ########

    libraries = [
        Library("pyarrow==8.0.0"),
        Library("snowflake-sqlalchemy"),
        Library("tqdm"),
    ]
    base_parameters = {"line": 10, "gender": "M"}
    notebook_task = NotebookTask(
        notebook_path="/the/path",
        source="WORKSPACE",
        base_parameters=base_parameters,
    )
    existing_cluster_id = "cluster_id"
    tasks = [
        JobTaskSettings(
            task_key="task_key_00",
            notebook_task=notebook_task,
            existing_cluster_id=existing_cluster_id,
            libraries=libraries,
        ),
        JobTaskSettings(
            task_key="task_key_01",
            depends_on=[
                TaskDependency("task_key_00"),
            ],
            notebook_task=notebook_task,
            existing_cluster_id=existing_cluster_id,
        ),
    ]

    #######
    # JOB #
    #######

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
        tasks=tasks,
        max_concurrent_runs=1,
    )

    # dump the result
    lg.info(
        "job: \n{}",
        jd(
            jsons.dump(job, strip_privates=True),
            indent=4,
        ),
    )


if __name__ == "__main__":
    # sample_create_job_manual()
    sample_create_job_auto_task()
