# ecs-session

Inspired by [ecsgo](https://github.com/tedsmitt/ecsgo) (`ecspy` is in use already).

Provides a tool to interact with AWS ECS tasks. Basically just wraps `aws`.

Currently provides:

* interactive execute-command (e.g. shell)
* port-forwarding

You can supply command-line arguments to specify which cluster/service/task/... to use or will be prompted
with a nice menu.

## Installation

```
pip install ecs-session
```

## Pre-requisites

### Tools

* [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* [session-manager-plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)

MacOS users can alternatively install this via Homebrew:
`brew install --cask session-manager-plugin awscli`

### Infrastructure

Use [ecs-exec-checker](https://github.com/aws-containers/amazon-ecs-exec-checker) to check for the pre-requisites to use ECS exec.


## Usage

See `ecs-session --help`.
