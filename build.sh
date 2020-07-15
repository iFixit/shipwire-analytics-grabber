#!/bin/bash

set -euo pipefail

docker build -t "shipwire-analytics-grabber:${TAG:-testing}" .
