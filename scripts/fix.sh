#!/usr/bin/env bash

set -e

export PATH=env/bin:$PATH

set -x

black plugins/
isort plugins/
