# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecs_session']

package_data = \
{'': ['*']}

install_requires = \
['boto3', 'configargparse', 'shtab', 'simple_term_menu']

entry_points = \
{'console_scripts': ['ecs-session = ecs_session.cli:run']}

setup_kwargs = {
    'name': 'ecs-session',
    'version': '24.4.5',
    'description': 'ECS SSM tool',
    'long_description': '# ecs-session\n\nInspired by [ecsgo](https://github.com/tedsmitt/ecsgo) (`ecspy` is in use already).\n\nProvides a tool to interact with AWS ECS tasks.\n\nCurrently provides:\n\n* interactive execute-command (e.g. shell)\n* port-forwarding\n\nYou can supply command-line arguments to specify which cluster/service/task/... to use or will be prompted with a nice menu.\n\n## Installation\n\n```\npip install ecs-session\n```\n\n## Pre-requisites\n\n### [session-manager-plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)\n\n#### Linux\n\n```bash\ncurl https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb -o "/tmp/session-manager-plugin.deb"\nmkdir -p ~/bin\ndpkg-deb --fsys-tarfile /tmp/session-manager-plugin.deb | tar --strip-components=4 -C ~/bin/ -xvf - usr/local/sessionmanagerplugin/bin/session-manager-plugin\n```\n\n#### MacOS\n\n`brew install --cask session-manager-plugin`\n\n### Infrastructure\n\nUse [ecs-exec-checker](https://github.com/aws-containers/amazon-ecs-exec-checker) to check for the pre-requisites to use ECS exec.\n\n\n## Usage\n\nSee `ecs-session --help`.\n',
    'author': 'Stefan Heitmüller',
    'author_email': 'stefan.heitmueller@gmx.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/morph027/ecs-session',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
