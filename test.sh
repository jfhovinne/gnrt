#!/usr/bin/env bash

pip install -r requirements.txt
flake8 --max-line-length=127 gnrt
pip freeze | safety check --stdin
bandit -r gnrt -c .bandit.yml
python -m pytest
