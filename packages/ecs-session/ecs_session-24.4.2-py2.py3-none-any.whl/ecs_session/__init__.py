#!/usr/bin/env python3

import json
import os

import configargparse
import shtab
from boto3 import session
from simple_term_menu import TerminalMenu


def get_parser():
    """argument parser"""
    parser = configargparse.ArgParser(
        prog="pyecs",
        auto_env_var_prefix="PYECS_",
    )
    shtab.add_argument_to(parser, ["--print-completion"])
    parser.add_argument("--profile", help="AWS Profile")
    parser.add_argument(
        "--region",
        help="AWS region name",
        default="eu-central-1",
    )
    parser.add_argument(
        "--cluster",
        help="ECS cluster name",
    )
    parser.add_argument(
        "--service",
        help="ECS service name",
    )
    parser.add_argument(
        "--task",
        help="ECS task id",
    )
    parser.add_argument(
        "--container",
        help="ECS container name",
    )
    parser.add_argument(
        "--command",
        help="Execute command",
        default="/bin/bash",
    )
    parser.add_argument(
        "--remote-port",
        help="ECS container remote port",
        type=int,
    )
    parser.add_argument(
        "--local-port",
        help="Local port for forwarding. Defaults to random port (0)",
        type=int,
        default=0,
    )
    subparsers = parser.add_subparsers(
        dest="action",
        help="action",
    )
    subparsers.required = True
    subparsers.add_parser("forward", help="Portforwarding")
    subparsers.add_parser("command", help="Execute command")
    return parser


def show_menu(items: list, title: str, source: list = None, clear_screen: bool = True):
    """
    menu function
    """
    index = None
    source = source or items
    menu = TerminalMenu(
        items, title=title, show_search_hint=True, clear_screen=clear_screen
    )
    index = menu.show()
    if index is None:
        exit(0)
    return source[index], index


def ecs_paginator(ecs: session.Session.client, paginator: str, leaf: str, **kwargs):
    """
    aws paginator
    """
    arns = []
    paginator = ecs.get_paginator(paginator)
    iterator = paginator.paginate(**kwargs)
    for page in iterator:
        arns.extend(page.get(leaf))
    return arns


def get_cluster(ecs: session.Session.client, cluster: str):
    """
    get clusters
    """
    if cluster:
        return cluster, None
    arns = ecs_paginator(
        ecs=ecs,
        paginator="list_clusters",
        leaf="clusterArns",
    )
    clusters = [cluster.split("/")[-1] for cluster in arns]
    return show_menu(
        items=clusters,
        title="Select cluster",
    )


def get_service(ecs: session.Session.client, service: str, cluster: str):
    """
    get service
    """
    if service:
        return service, None
    arns = ecs_paginator(
        ecs=ecs,
        paginator="list_services",
        leaf="serviceArns",
        cluster=cluster,
    )
    services = [service.split("/")[-1] for service in arns]
    return show_menu(
        items=services,
        title="Select service",
    )


def get_task(ecs: session.Session.client, task: str, cluster: str, service: str):
    """
    get services
    """
    if task:
        return task, None
    arns = ecs_paginator(
        ecs=ecs,
        paginator="list_tasks",
        leaf="taskArns",
        cluster=cluster,
        serviceName=service,
    )
    tasks = [task.split("/")[-1] for task in arns]
    return show_menu(
        items=tasks,
        title="Select task",
    )


def get_container(containers: list, container: str):
    """
    get container
    """
    if container:
        return container, containers.index(container)
    return show_menu(
        items=containers,
        title="Select container",
    )


def portforward(
    ecs: session.Session.client,
    cluster: str,
    container_index: int,
    task_details: dict,
    remote_port: int,
    local_port: int,
    profile: str,
):
    """
    portforward
    """
    if not remote_port:
        task_definition_arn = task_details.get("tasks")[0].get("taskDefinitionArn")
        task_definition = ecs.describe_task_definition(
            taskDefinition=task_definition_arn
        ).get("taskDefinition")
        ports = [
            str(container.get("containerPort"))
            for container in task_definition.get("containerDefinitions")[
                container_index
            ].get("portMappings")
        ]
        remote_port, _ = show_menu(items=ports, title="Select port", clear_screen=False)
    runtime_id = (
        task_details.get("tasks")[0].get("containers")[container_index].get("runtimeId")
    )
    args = [
        "aws",
        "ssm",
        "start-session",
        "--document-name",
        "AWS-StartPortForwardingSession",
        "--parameters",
        json.dumps(
            {
                "portNumber": [str(remote_port)],
                "localPortNumber": [str(local_port)],
            }
        ),
        "--target",
        f"ecs:{cluster}_{runtime_id.split('-')[0]}_{runtime_id}",
    ]
    if profile:
        args.extend(
            [
                "--profile",
                profile,
            ]
        )
    os.execvp(
        "aws",
        args,
    )


def command(cluster: str, task: str, container: str, command: str, profile: str):
    """
    command
    """
    args = [
        "aws",
        "ecs",
        "execute-command",
        "--cluster",
        cluster,
        "--task",
        task,
        "--container",
        container,
        "--command",
        command,
        "--interactive",
    ]
    if profile:
        args.extend(
            [
                "--profile",
                profile,
            ]
        )
    os.execvp(
        "aws",
        args,
    )


def main():
    """main function"""
    parser = get_parser()
    arguments, _ = parser.parse_known_args()
    boto3_session = session.Session(
        region_name=arguments.region, profile_name=arguments.profile
    )
    ecs = boto3_session.client("ecs")
    cluster, _ = get_cluster(ecs=ecs, cluster=arguments.cluster)
    service, _ = get_service(ecs=ecs, service=arguments.service, cluster=cluster)
    task, _ = get_task(ecs=ecs, task=arguments.task, cluster=cluster, service=service)
    task_details = ecs.describe_tasks(cluster=cluster, tasks=[task])
    containers = [
        container.get("name")
        for container in task_details.get("tasks")[0].get("containers")
    ]
    container, container_index = get_container(
        containers=containers,
        container=arguments.container,
    )
    function = {
        "forward": portforward,
        "command": command,
    }
    args = {
        "forward": {
            "cluster": cluster,
            "container_index": container_index,
            "ecs": ecs,
            "task_details": task_details,
            "remote_port": arguments.remote_port,
            "local_port": arguments.local_port,
            "profile": arguments.profile,
        },
        "command": {
            "cluster": cluster,
            "container": container,
            "task": task,
            "command": arguments.command,
            "profile": arguments.profile,
        },
    }
    print(f"cluster: {cluster}")
    print(f"service: {service}")
    print(f"task: {task}")
    print(f"container: {container}")
    function.get(arguments.action)(**args.get(arguments.action))


if __name__ == "__main__":
    main()
