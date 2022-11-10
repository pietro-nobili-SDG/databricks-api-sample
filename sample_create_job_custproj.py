"""Create the task kinda like the customer projection would need."""
from databricks_cli.clusters.api import ClusterApi
from databricks_cli.jobs.api import JobsApi
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
from utils import get_databricks_client, jd


def sample_customer_projection_tasks() -> None:
    """Create the task kinda like the customer projection would need."""

    # get the main API client
    api_client = get_databricks_client()

    ####################################################################
    # get the cluster interface and get the cluster id
    cluster_api = ClusterApi(api_client)

    cluster_name = "test_databricks_api_01"

    # # this actually returns a list of cluster info
    # # cluster_ids = cluster_api.get_cluster_ids_by_name(cluster_name)
    # clusters = cluster_api.get_cluster_ids_by_name(cluster_name)
    # for cluster in clusters:
    #     lg.info("{}: {}", cluster_name, cluster["cluster_id"])

    cluster_id = cluster_api.get_cluster_id_for_name(cluster_name)
    lg.info("{}: {}", cluster_name, cluster_id)

    ####################################################################
    # create the job

    ########
    # TASK #
    ########
    notebook_path = "/Repos/whs_cust_projection/whs_cust_projection/notebooks/test_nb_script/test_nb_script"
    libraries = [
        Library("pyarrow==8.0.0"),
        Library("snowflake-sqlalchemy"),
        Library("tqdm"),
    ]
    source = "WORKSPACE"

    params_by_cluster = {
        cluster_id: [
            {"line": 10, "gender": "W"},
            {"line": 10, "gender": "M"},
        ],
        # "cluster_2": [
        #     {"line": 30, "gender": "G"},
        #     {"line": 30, "gender": "B"},
        # ],
    }
    shared_params = {
        "season": "2023-3",
        "actual_day_from_camp_start": 15,
    }

    tasks = []
    for cluster_id, params in params_by_cluster.items():

        # new cluster, reset state
        is_first_task_for_cluster = True
        last_task_key = ""

        for p in params:

            # build the task name
            task_key = f"automatic_{p['line']}{p['gender']}"

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
        pause_status="PAUSED",
    )
    email_notifications = JobEmailNotifications(
        on_success=["pietro.nobili@sdggroup.com"],
        on_failure=["pietro.nobili@sdggroup.com"],
        no_alert_for_skipped_runs=False,
    )
    job = JobSettings(
        name="test_automatic_task_structure",
        email_notifications=email_notifications,
        schedule=schedule,
        tasks=tasks,
        max_concurrent_runs=1,
    )

    json_payload = jsons.dump(job, strip_privates=True)

    # dump the result
    lg.info("job: \n{}", jd(json_payload, indent=4))

    # create the job API interface
    jobs_api = JobsApi(api_client)
    job_create_response = jobs_api.create_job(json=json_payload)
    lg.debug(f"{type(job_create_response)=}")
    lg.debug(f"{job_create_response=}")
    # a dict with the job_id:
    # {'job_id': 668699478230689}


if __name__ == "__main__":
    sample_customer_projection_tasks()
