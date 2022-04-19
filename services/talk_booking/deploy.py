import argparse
import time

import boto3


def get_current_task_definition(client, cluster, service):
    current_task_arn = client.describe_services(cluster=cluster, services=[service])[
        "services"
    ][0]["taskDefinition"]

    return client.describe_task_definition(taskDefinition=current_task_arn)[
        "taskDefinition"
    ]


def create_new_task_definition(client, current_definition, new_image):
    container_definition = current_definition["containerDefinitions"][0].copy()
    container_definition["image"] = new_image

    return client.register_task_definition(
        family=task_definition["family"],
        volumes=task_definition["volumes"],
        containerDefinitions=[container_definition],
    )["taskDefinition"]["taskDefinitionArn"]


def run_migrations(client, cluster, task_arn):
    response = client.run_task(
        cluster=cluster,
        taskDefinition=task_arn,
        overrides={
            "containerOverrides": [
                {"name": "talk-booking-app", "command": "python migrations.py".split()}
            ],
        },
    )
    print(response)


def update_service(client, cluster, service, task_arn):
    response = client.update_service(
        cluster=cluster, service=service, taskDefinition=task_arn,
    )
    print(response)


def wait_to_finish_deployment(client, cluster, service, timeout, task_definition_arn):
    sleep_seconds = 10
    timeout = int(timeout / sleep_seconds)
    cnt = 0
    deployment_finished = False

    while cnt < timeout:
        response = client.describe_services(cluster=cluster, services=[service])
        deployment = next(
            depl
            for depl in response["services"][0]["deployments"]
            if depl["status"] == "PRIMARY"
        )
        new_deployment_created = int(task_definition_arn.split(":")[-1]) < int(
            response["services"][0]["taskDefinition"].split(":")[-1]
        )

        if (
            deployment["runningCount"] == deployment["desiredCount"]
            or new_deployment_created
        ):
            deployment_finished = True
            break
        print(
            f"Waiting ... Running count: {deployment['runningCount']}; "
            f"Desired count: {deployment['desiredCount']}"
        )
        time.sleep(sleep_seconds)

    return deployment_finished


if __name__ == "__main__":
    print("Starting deployment...")

    DEPLOYMENT_TIMEOUT = 1800  # seconds

    parser = argparse.ArgumentParser()
    parser.add_argument("--cluster_name", help="Name of ECS cluster")
    parser.add_argument("--service_name", help="Service name")
    parser.add_argument("--new_image_uri", help="URI of new Docker image")

    args = parser.parse_args()
    print("ARGUMENTs:", args)
    cluster_name = args.cluster_name
    service_name = args.service_name
    new_image_uri = args.new_image_uri

    ecs_client = boto3.client("ecs")
    print("ECS CLIENT : ", ecs_client)

    task_definition = get_current_task_definition(
        ecs_client, cluster=cluster_name, service=service_name
    )
    print("TASK DEFINITION : ", task_definition)

    new_task_arn = create_new_task_definition(
        ecs_client, task_definition, new_image_uri
    )
    print("NEW TASK : ", new_task_arn)

    run_migrations(ecs_client, cluster_name, new_task_arn)

    update_service(
        ecs_client, cluster=cluster_name, service=service_name, task_arn=new_task_arn,
    )
    finished = wait_to_finish_deployment(
        ecs_client,
        cluster=cluster_name,
        service=service_name,
        timeout=DEPLOYMENT_TIMEOUT,
        task_definition_arn=new_task_arn,
    )

    if not finished:
        print("Did not stabilize ...")
        exit(1)
