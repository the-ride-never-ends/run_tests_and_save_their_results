#!/bin/bash

# Ensure we're in the right directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Pass all arguments to the Python script
python main.py "$@"

# Exit with the same code as the Python script
exit $?