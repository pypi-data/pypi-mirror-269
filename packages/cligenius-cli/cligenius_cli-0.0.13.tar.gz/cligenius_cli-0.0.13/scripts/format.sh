#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place cligenius_cli tests --exclude=__init__.py
black cligenius_cli tests
isort cligenius_cli tests
