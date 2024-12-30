#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd "$SCRIPT_DIR"

source venv/bin/activate
python3 app.py
