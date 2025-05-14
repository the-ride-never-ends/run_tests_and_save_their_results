#!/bin/bash

# Load the .env file.
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
    echo Loaded environment variables from .env
else
    echo ".env file not found"
    exit 1
fi

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

# Deactivate the virtual environment
deactivate

# Exit with the same code as the Python script
exit $?