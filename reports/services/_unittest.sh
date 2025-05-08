#!/bin/bash
# Run unit tests in a python process
# We do this because we need to activate the virtual environment in the other python program.

# Get the bash profile or zsh profile
source ~/.bashrc 2>/dev/null || source ~/.bash_profile 2>/dev/null || source ~/.zshrc 2>/dev/null || {
    echo "No profile found. Please check your shell configuration."
    exit 1
}

# Check if argument is provided, otherwise use current directory
if [ "$1" ]; then
    PROJECT_DIR="$1"
    cd "$PROJECT_DIR" || { echo "Failed to change directory to $PROJECT_DIR"; exit 1; }
else
    echo "No project directory provided. Please provide a directory."
    exit 1
fi

# Activate virtual environment for the tests if they exist
if [ -d "venv" ]; then
    source venv/bin/activate || source .venv/bin/activate || {
        echo "Failed to activate virtual environment. Please check the venv directory."
        exit 1
    }
    echo "Activated virtual environment from venv"
else
    echo "No virtual environment found in venv"
    exit 1
fi

python -m unittest discover -s "$PROJECT_DIR/tests" -p test_*.py