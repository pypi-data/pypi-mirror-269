#!/usr/bin/env python3
"""
ECSSession
"""

import json
import os

from boto3 import session
from botocore import exceptions


class ECSSession:
    """
    ECSSession
    """

    def __init__(
        self,
        cluster: str,
        command: str,
        container: str,
        container_index: int,
        ecs: session.Session,
        local_port: int,
        profile: str,
        region: str,
        remote_port: int,
        ssm: session.Session,
        task: str,
        task_details: dict,
    ):
        """
        ECSSession
        """
        self.cluster = cluster
        self.command = command
        self.container = container
        self.container_index = container_index
        self.ecs = ecs
        self.local_port = local_port
        self.profile = profile
        self.region = region
        self.remote_port = remote_port
        self.ssm = ssm
        self.task = task
        self.task_details = task_details
        self.runtime_id = (
            task_details.get("tasks")[0].get("containers")[container_index].get("runtimeId")
        )
        self.target = f"ecs:{self.cluster}_{self.runtime_id.split('-')[0]}_{self.runtime_id}"


    def port_forward(self):
        """
        forward port
        """
        parameters = {
            "portNumber": [str(self.remote_port)],
            "localPortNumber": [str(self.local_port)],
        }
        try:
            ssm_start_session = self.ssm.start_session(
                Target=self.target,
                DocumentName="AWS-StartPortForwardingSession",
                Parameters=parameters,
            )
        except exceptions.ClientError as err:
            print(err)
            exit(1)
        args = [
            "session-manager-plugin",
            json.dumps(
                {
                    "SessionId": ssm_start_session.get("SessionId"),
                    "TokenValue": ssm_start_session.get("TokenValue"),
                    "StreamUrl": ssm_start_session.get("StreamUrl"),
                }
            ),
            self.region,
            "StartSession",
        ]
        if self.profile:
            args.extend([self.profile])
        args.extend(
            [
                json.dumps(
                    {
                        "Target": self.target,
                        "DocumentName": "AWS-StartPortForwardingSession",
                        "Parameters": parameters,
                    }
                ),
                f"https://ecs.{self.region}.amazonaws.com",
            ]
        )
        try:
            os.execvp(
                "session-manager-plugin",
                args,
            )
        except FileNotFoundError:
            print("session-manager-plugin missing!")


    def execute_command(self):
        """
        execute command
        """
        try:
            ecs_execute_command_session = self.ecs.execute_command(
                cluster=self.cluster,
                container=self.container,
                task=self.task,
                command=self.command,
                interactive=True,
            ).get("session")
        except exceptions.ClientError as err:
            print(err)
            exit(1)
        args = [
            "session-manager-plugin",
            json.dumps(ecs_execute_command_session),
            self.region,
            "StartSession",
        ]
        if self.profile:
            args.extend([self.profile])
        args.extend(
            [
                json.dumps(
                    {"Target": self.target},
                ),
                f"https://ecs.{self.region}.amazonaws.com",
            ]
        )
        try:
            os.execvp(
                "session-manager-plugin",
                args,
            )
        except FileNotFoundError:
            print("session-manager-plugin missing!")
