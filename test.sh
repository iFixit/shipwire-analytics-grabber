#!/bin/bash

set -euo pipefail

pip install pipenv
pipenv install
pipenv run black --check .
pipenv run pytest
