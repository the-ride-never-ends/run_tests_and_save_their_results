#!/bin/bash
# Run unit tests in a python process
# We do this because we need to activate the virtual environment in the other python program.

# Get the bash profile or zsh profile
source ~/.bashrc 2>/dev/null || source ~/.bash_profile 2>/dev/null || source ~/.zshrc 2>/dev/null || {
    echo "No profile found. Please check your shell configuration."
    exit 1
}

# Load the venv path from the environment.
TEST_VENV_PATH=${TEST_VENV_PATH:-"$(pwd)/venv"}
echo "Using virtual environment path: $TEST_VENV_PATH"

# Check if argument is provided, otherwise use current directory
if [ "$1" ]; then
    PROJECT_DIR="$1"
    cd "$PROJECT_DIR" || { echo "Failed to change directory to $PROJECT_DIR"; exit 1; }
else
    echo "No project directory provided. Please provide a directory."
    exit 1
fi

# Activate virtual environment for the tests if they exist
if [ -d "$TEST_VENV_PATH" ]; then
    source "$TEST_VENV_PATH/bin/activate" || {
        echo "Failed to activate virtual environment. Please check the venv directory."
        exit 1
    } && echo "Activated virtual environment at $TEST_VENV_PATH"
else
    echo "No virtual environment found at $TEST_VENV_PATH"
    exit 1
fi

# Run the tests
python -m unittest discover -s "$PROJECT_DIR" -p test_*.py

# Deactivate the virtual environment
deactivate || {
    echo "Failed to deactivate virtual environment. Please check the venv directory."
    exit 1
} && echo "Deactivated virtual environment at $TEST_VENV_PATH"
exit 0