#!/bin/bash

echo "===================================="
echo "阻抗控制工具快速啟動腳本"
echo "===================================="
echo

# 檢查 Python 是否可用
if ! command -v python &> /dev/null; then
    echo "❌ 錯誤: 找不到 Python，請先安裝 Python 3.8+"
    exit 1
fi

echo "✅ Python 環境檢查通過"

# 安裝依賴
echo "📦 檢查並安裝必要套件..."
pip install pandas openpyxl pyyaml > /dev/null 2>&1

# 執行整合測試
echo "🧪 執行快速測試..."
python test_integration.py

if [ $? -ne 0 ]; then
    echo "❌ 測試失敗，請檢查環境配置"
    exit 1
fi

echo
echo "✅ 工具準備完成！"
echo
echo "🚀 使用方法:"
echo "   cd src"
echo "   python main.py [你的netlist檔案.net] -o [輸出檔案.xlsx]"
echo
echo "📝 範例:"
echo "   python main.py ../tests/data/sample_netlist.net -o 我的結果.xlsx"
echo