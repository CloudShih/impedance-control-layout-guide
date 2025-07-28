@echo off
echo ====================================
echo 阻抗控制工具快速啟動腳本
echo ====================================
echo.

REM 檢查 Python 是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤: 找不到 Python，請先安裝 Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python 環境檢查通過

REM 安裝依賴
echo 📦 檢查並安裝必要套件...
pip install pandas openpyxl pyyaml >nul 2>&1

REM 執行整合測試
echo 🧪 執行快速測試...
python test_integration.py

if errorlevel 1 (
    echo ❌ 測試失敗，請檢查環境配置
    pause
    exit /b 1
)

echo.
echo ✅ 工具準備完成！
echo.
echo 🚀 使用方法:
echo    cd src
echo    python main.py [你的netlist檔案.net] -o [輸出檔案.xlsx]
echo.
echo 📝 範例:
echo    python main.py ../tests/data/sample_netlist.net -o 我的結果.xlsx
echo.
pause