@echo off
echo 系統診斷工具
echo =============
echo.

echo 1. 檢查 Python 版本:
python --version
echo.

echo 2. 檢查 Python 路徑:
where python
echo.

echo 3. 檢查已安裝的套件:
pip list | findstr pandas
pip list | findstr openpyxl  
pip list | findstr PyYAML
echo.

echo 4. 檢查當前目錄:
dir
echo.

echo 5. 檢查測試檔案是否存在:
if exist "tests\data\sample_netlist.net" (
    echo 測試檔案存在
) else (
    echo 警告: 找不到測試檔案
)
echo.

echo 6. 嘗試導入 Python 模組:
python -c "import pandas; print('pandas: OK')"
python -c "import openpyxl; print('openpyxl: OK')"  
python -c "import yaml; print('yaml: OK')"
echo.

echo 診斷完成！
pause