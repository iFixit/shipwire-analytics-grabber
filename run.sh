#!/bin/bash

set -euo pipefail

docker run \
 --env RUN_FOR_DATE="$RUN_FOR_DATE" \
 --env-file .env \
 -v /etc/hosts:/etc/hosts \
 $@ \
 shipwire-analytics-grabber:"${TAG:-testing}"
