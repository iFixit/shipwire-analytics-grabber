#!/bin/bash

pipenv lock -r --pre > requirements.txt
docker build -t "shipwire-analytics-grabber:${TAG:-latest}" .
