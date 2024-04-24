# Copyright 2024 Paion Data
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
import json
import logging

from screwdriver_cd_sdk_python.events import start_build
from screwdriver_cd_sdk_python.pipeline import (create_pipeline,
                                                search_pipelines_by_name)
from screwdriver_cd_sdk_python.secrets import create_or_update_secret


def initialize(pipelines_config_path: str, screwdriver_api_url: str, token: str) -> None:
    """
    Given a JSON file containing Screwdriver pipeline definitions, this method initializes all pipelines on a running
    Screwdriver instance.

    The basics works like this

    .. highlight:: json
    .. code-block:: json

        [
            {
                "git": "git@github.com:paion-data/immutable-infrastructure-as-a-service.git"
            },
            {
                "git": "git@github.com:paion-data/docker-kong.git"
            },
        ]

    We also support loading AWS secrets into Screwdriver instances. To do that, download the IAM credentials CSV file
    and specify the absolute path of that file by

    .. highlight:: json
    .. code-block:: json

        [
            {
                "git": "git@github.com:paion-data/docker-kong.git",
                "awsCredentialFile": "abs-path-to/aws_accessKeys.csv",
            }
        ]

    In addition, one can also preload
    `GitHub Secrets <https://screwdriver-docs.paion-data.dev/user-guide/configuration/secrets>`_ with, for example

    .. highlight:: json
    .. code-block:: json

        [
            {
                "git": "git@github.com:paion-data/docker-kong.git",
                "secrets": [
                    {
                        "name": "MY_CREDENTIAL_FILE",
                        "type": "file",
                        "value": "/home/root/credential.json"
                    },
                    {
                        "name": "MY_PASSWORD",
                        "type": "value",
                        "value": "23efdsf324gfdg"
                    }
                ],
            }
        ]

    Note that both value and file based secrets are supported as shown in the example above

    :param pipelines_config_path:  The absolute JSON file containing Screwdriver pipeline definitions
    :param screwdriver_api_url:  The Screwdriver API URL. For example, https://screwdriver.mycompany.com
    :param token:  `The Screwdriver API Token <https://screwdriver-docs.paion-data.dev/user-guide/tokens.html>`_
    """
    with open(pipelines_config_path, 'r') as file:
        pipelines = json.load(file)

    for pipeline in pipelines:

        git_url = pipeline["git"]
        repo_name = git_url[git_url.find(":") + 1:git_url.find(".git")]

        pipeline_id = None
        for match in search_pipelines_by_name(name=repo_name, screwdriver_api_url=screwdriver_api_url, token=token):
            if match["name"] == repo_name:
                pipeline_id = match["id"]
                logging.debug("{} is already created.".format(repo_name))

                break

        if pipeline_id is None:
            logging.debug("Creating {}...".format(repo_name))
            pipeline_id = create_pipeline(
                checkout_url=pipeline["git"],
                screwdriver_api_url=screwdriver_api_url,
                token=token
            )["id"]

        if "awsCredentialFile" in pipeline:
            with open(pipeline["awsCredentialFile"], 'r') as file:
                lines = csv.reader(file)
                for i, row in enumerate(lines):
                    if i == 1:
                        create_or_update_secret(
                            secret_name="AWS_ACCESS_KEY_ID",
                            secret_value=row[0],
                            pipeline_id=pipeline_id,
                            screwdriver_api_url=screwdriver_api_url,
                            token=token
                        )
                        create_or_update_secret(
                            secret_name="AWS_SECRET_ACCESS_KEY",
                            secret_value=row[1],
                            pipeline_id=pipeline_id,
                            screwdriver_api_url=screwdriver_api_url,
                            token=token
                        )
        if pipeline["secrets"]:
            for secret in pipeline["secrets"]:
                if secret["type"] == "value":
                    create_or_update_secret(
                        secret_name=secret["name"],
                        secret_value=secret["value"],
                        pipeline_id=pipeline_id,
                        screwdriver_api_url=screwdriver_api_url,
                        token=token
                    )
                else:
                    create_or_update_secret(
                        secret_name=secret["name"],
                        secret_value=_file_content(secret["value"]),
                        pipeline_id=pipeline_id,
                        screwdriver_api_url=screwdriver_api_url,
                        token=token
                    )

        if pipeline["runOnCreate"]:
            start_build(pipeline_id=pipeline_id, screwdriver_api_url=screwdriver_api_url, token=token)


def _file_content(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read().rstrip('\n')  # https://stackoverflow.com/a/70233945
