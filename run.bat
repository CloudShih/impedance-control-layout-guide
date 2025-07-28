@echo off
echo Impedance Control Tool Launcher
echo ================================

echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found
    echo Please install Python 3.8+ from python.org
    pause
    exit
)

echo Installing packages...
pip install pandas openpyxl pyyaml

echo Running test...
python test_tool.py
if errorlevel 1 (
    echo TEST FAILED - Please check environment
    pause
    exit
)

echo.
echo SUCCESS! Tool is ready to use
echo.
echo Usage: cd src
echo        python main.py [netlist_file] -o [output.xlsx]
echo.
echo Example: python main.py ../tests/data/sample_netlist.net -o result.xlsx
echo.
pause