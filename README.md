# 阻抗控制佈局指南生成器 v2.0

> 智能化的電路板佈局指南自動生成工具

一個專業的阻抗控制工具，能夠從 Netlist 檔案自動提取網路名稱，智能分類網路類型，並生成標準化的 Excel 格式佈局指南。

## ✨ 主要特色

- 🔍 **智能 Netlist 解析** - 支援多種格式 (.net, .sp, .cir, .txt)
- 🧠 **智能網路分類** - 基於關鍵字和正則表達式的自動分類
- 📋 **自動規則應用** - 根據信號類型自動套用對應的佈局規則
- 📊 **專業 Excel 輸出** - 格式化的佈局指南文檔
- ⚙️ **靈活配置系統** - YAML 配置檔案，支援自定義規則
- 🖥️ **雙介面支援** - GUI 圖形介面 + CLI 命令列介面

## 🚀 快速開始

### ⚠️ 重要說明
- **測試腳本**: `run.bat` / `launch.sh` 僅用於功能驗證
- **實際使用**: 需要選擇你自己的 netlist 檔案

### 使用方法

#### 簡單圖形介面 (推薦新手)
```bash
python run_simple_gui.py
```

#### 進階圖形介面 (進階用戶)
```bash
python run_advanced_gui.py
```

#### 命令列 (專業用戶)
```bash
cd src && python main.py "你的netlist.net" -o "輸出.xlsx"
```

## 📖 完整文檔

- **[USER_MANUAL.md](USER_MANUAL.md)** - 完整使用說明書
- `examples/manual_tests/` - 手動測試與示範腳本

## 🛠️ 系統需求

- Python 3.8+
- Windows/macOS/Linux  
- 依賴套件: pandas, openpyxl, pyyaml, PyQt5

## 🧪 測試驗證

```bash
pytest
```

## 📈 版本歷史

- **v2.0** (2025-07-29) - 完整重構，模組化架構，GUI 增強
- **v1.0** - 基礎版本，硬編碼規則

## 📜 授權

MIT License

---

**立即開始使用，從手動分類到智能自動化！** 🎉