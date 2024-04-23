# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecs_session']

package_data = \
{'': ['*']}

install_requires = \
['boto3', 'configargparse', 'shtab', 'simple_term_menu']

entry_points = \
{'console_scripts': ['ecspy = ecs_session:main']}

setup_kwargs = {
    'name': 'ecs-session',
    'version': '24.4.1',
    'description': 'ECS SSM tool',
    'long_description': '# ecs-session\n\nInspired by [ecsgo](https://github.com/tedsmitt/ecsgo) (`ecspy` is in use already).\n\nProvides a tool to interact with AWS ECS tasks. Basically just wraps `aws`.\n\n## Installation\n\n```\npip install ecs-session\n```\n\n## Pre-requisites\n\n* [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)\n* [session-manager-plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)\n\nMacOS users can alternatively install this via Homebrew:\n`brew install --cask session-manager-plugin awscli`\n\n### Infrastructure\n\nUse [ecs-exec-checker](https://github.com/aws-containers/amazon-ecs-exec-checker) to check for the pre-requisites to use ECS exec.\n',
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
