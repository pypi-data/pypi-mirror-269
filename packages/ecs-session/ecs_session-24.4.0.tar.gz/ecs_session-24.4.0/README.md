# ecspy

Inspired by [ecsgo](https://github.com/tedsmitt/ecsgo).

Provides a tool to interact with AWS ECS tasks.

## Installation

```
pip install git+https://github.com/morph027/ecspy
```

## Pre-requisites

* [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* [session-manager-plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)

MacOS users can alternatively install this via Homebrew:
`brew install --cask session-manager-plugin awscli`

### Infrastructure

Use [ecs-exec-checker](https://github.com/aws-containers/amazon-ecs-exec-checker) to check for the pre-requisites to use ECS exec.
