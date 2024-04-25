#!/bin/sh -e
set -x

# Sort imports one per line, so autoflake can remove unused imports
isort --recursive  --force-single-line-imports --thirdparty cligenius_cli --apply cligenius_cli tests
sh ./scripts/format.sh
