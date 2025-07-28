@echo off
chcp 65001 >nul 2>&1
title 阻抗控制工具啟動器

echo ====================================
echo 阻抗控制工具快速啟動腳本
echo ====================================
echo.

echo [1/4] 檢查 Python 環境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 錯誤: 找不到 Python，請先安裝 Python 3.8+
    echo.
    echo 請從以下網址下載安裝 Python:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python 環境檢查通過
echo.

echo [2/4] 檢查並安裝必要套件...
pip install pandas openpyxl pyyaml
if errorlevel 1 (
    echo 警告: 套件安裝可能有問題，但繼續執行測試...
)
echo.

echo [3/4] 執行快速測試...
python test_integration.py
if errorlevel 1 (
    echo.
    echo 測試失敗，可能的原因:
    echo 1. Python 版本過舊 (需要 3.8+)
    echo 2. 缺少必要套件
    echo 3. 檔案路徑問題
    echo.
    echo 請嘗試手動執行以下命令:
    echo   cd src
    echo   python main.py ../tests/data/sample_netlist.net
    echo.
    pause
    exit /b 1
)

echo.
echo [4/4] 工具準備完成！
echo.
echo ====================================
echo 使用方法:
echo ====================================
echo 1. 開啟命令提示字元
echo 2. 進入 src 目錄: cd src
echo 3. 執行命令: python main.py [你的netlist檔案] -o [輸出檔案.xlsx]
echo.
echo 範例:
echo   python main.py ../tests/data/sample_netlist.net -o 我的結果.xlsx
echo.
echo 更多說明請查看 QUICK_START_GUIDE.md
echo ====================================
echo.
pause