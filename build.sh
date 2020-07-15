#!/bin/bash

docker build -t "shipwire-analytics-grabber:${TAG:-latest}" .
