#!/usr/bin/env bash

set -e

export PATH=env/bin:$PATH

set -x

black plugins/
isort plugins/
flake8 plugins/
mypy plugins/
