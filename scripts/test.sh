#!/usr/bin/env bash

set -e

export PATH=env/bin:$PATH

set -x

black --check plugins/
isort --check plugins/
flake8 plugins/
mypy plugins/
