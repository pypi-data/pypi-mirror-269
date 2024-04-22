#!/bin/bash
# run with '. dev-setup.sh'

# AUTO DEV SETUP

# check if rye is installed
if ! command -v rye &> /dev/null
then
    echo "rye could not be found: installing now ..."
    curl -sSf https://rye-up.com/get | bash
    echo "Check the rye docs for more info: https://rye-up.com/"
fi

source "$HOME/.rye/env"

echo "SYNC: setup .venv"
rye sync

echo "ACTIVATE: activate .venv"
. .venv/bin/activate
# use 'deactivate' to exit the virtual environment

echo "SETUP: install pre-commit hooks"
pre-commit install

echo "TESTING ..."
pytest
