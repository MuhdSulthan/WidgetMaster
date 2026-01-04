#!/bin/bash

# Check if Python is installed
if command -v python3 &>/dev/null; then
    python_cmd="python3"
elif command -v python &>/dev/null; then
    python_cmd="python"
else
    echo "Error: Python is not installed or not in PATH."
    exit 1
fi

# Check if Pillow is installed
$python_cmd -c "import PIL" &>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing Pillow library..."
    $python_cmd -m pip install pillow
fi

# Run the desktop widget application
echo "Starting Desktop Widget..."
$python_cmd main.py