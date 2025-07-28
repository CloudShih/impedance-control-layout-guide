#!/bin/bash

echo "Impedance Control Tool Launcher"
echo "==============================="
echo

# Check Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python not found. Please install Python 3.8+"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "Python: OK"

# Install packages
echo "Installing required packages..."
$PYTHON_CMD -m pip install pandas openpyxl pyyaml PyQt5 > /dev/null 2>&1

# Test basic functionality
echo "Testing core functionality..."
$PYTHON_CMD test_tool.py

if [ $? -eq 0 ]; then
    echo
    echo "SUCCESS! Tool is ready to use"
    echo
    echo "Usage:"
    echo "  GUI:         $PYTHON_CMD simple_gui.py"
    echo "  Command:     $PYTHON_CMD main.py netlist.net -o output.xlsx"
    echo
    echo "See USER_MANUAL.md for detailed instructions"
else
    echo
    echo "Test failed. Please check your environment."
    exit 1
fi