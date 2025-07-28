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

### 一鍵啟動 (推薦)

**Windows**:
```cmd
雙擊 run.bat
```

**Linux/macOS**:
```bash
./launch.sh
```

### 圖形介面使用

```bash
cd src
python simple_gui.py
```

### 命令列使用

```bash
cd src
python main.py your_netlist.net -o layout_guide.xlsx
```

## 📖 詳細說明

完整的使用說明請查看 **[USER_MANUAL.md](USER_MANUAL.md)**

## 🛠️ 系統需求

- Python 3.8+
- Windows/macOS/Linux
- 依賴套件: pandas, openpyxl, pyyaml, PyQt5

## 📂 專案結構

```
impedenceControll/
├── src/                          # 主要程式碼
│   ├── core/                     # 核心模組
│   │   ├── netlist_parser.py     # Netlist 解析器
│   │   ├── net_classifier.py     # 網路分類器
│   │   ├── rule_engine.py        # 規則引擎
│   │   └── template_mapper.py    # 模板映射器
│   ├── config/                   # 配置管理
│   │   ├── config_manager.py     # 配置管理器
│   │   └── default_config.yaml   # 預設配置
│   ├── main.py                   # 主程式 (CLI)
│   └── simple_gui.py             # 圖形介面
├── tests/                        # 測試套件
├── examples/                     # 範例檔案
├── run.bat                       # Windows 啟動腳本
├── launch.sh                     # Linux/macOS 啟動腳本
└── USER_MANUAL.md               # 詳細使用說明
```

## 🎯 使用範例

### 基本使用

```bash
python main.py pcb_netlist.net -o layout_guide.xlsx
```

### 使用自定義配置

```bash
python main.py netlist.net -c custom_rules.yaml -o output.xlsx
```

### 批次處理

```python
from main import process_netlist_to_excel

result = process_netlist_to_excel(
    netlist_path=Path("design.net"),
    output_path=Path("guide.xlsx")
)
```

## 📊 輸出示例

生成的 Excel 檔案包含：

| Category | Net Name | Description | Impedance | Type | Width |
|----------|----------|-------------|-----------|------|-------|
| Communication Interface | I2C0_SCL | I2C總線佈局規則... | 50 Ohm | I2C | 5 mil |
| RF | ANT1_P | RF信號需要接地包圍... | 50 Ohm | Single-End | Calculated |
| Power | VDD_CORE | 電源線需要足夠銅厚... | N/A | Power | Current based |

## 🔧 自定義配置

```yaml
# custom_config.yaml
net_classification_rules:
  UART:
    keywords: ["UART", "RX", "TX"]
    category: "Communication Interface"
    signal_type: "UART"
    
layout_rules:
  UART:
    impedance: "50 Ohm"
    description: "UART通訊佈局規則"
    width: "5 mil"
```

## 🧪 測試

執行測試套件：

```bash
pytest tests/
```

## 📈 版本歷史

- **v2.0** (2025-07-28) - 完整重構，模組化架構，配置驅動
- **v1.0** - 基礎版本，硬編碼規則

## 🤝 貢獻

歡迎提交 Issues 和 Pull Requests！

## 📜 授權

MIT License

---

**立即開始使用，從手動分類到智能自動化！** 🎉