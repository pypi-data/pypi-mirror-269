#!/usr/bin/env bash

set -e
set -x

mypy cligenius_cli
black cligenius_cli tests --check
isort cligenius_cli tests --check-only
