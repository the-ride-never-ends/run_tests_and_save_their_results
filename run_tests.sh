#!/bin/bash

# Activate virtual environment for the tests if they exist
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Activated virtual environment from venv"
else
    echo "No virtual environment found in venv"
    exit 1
fi

# Pass all arguments to the Python script
python main.py "$@"

# Exit with the same code as the Python script
exit $?