@echo off
echo 阻抗控制工具啟動器
echo ==================

echo 檢查 Python...
python --version
if errorlevel 1 (
    echo 錯誤: 找不到 Python
    pause
    exit
)

echo 安裝套件...
pip install pandas openpyxl pyyaml

echo 執行測試...
python test_integration.py

echo.
echo 完成！現在可以使用工具了
echo 使用方法: cd src
echo          python main.py [netlist檔案] -o [輸出檔案.xlsx]
pause