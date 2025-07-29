# 阻抗控制佈局指南生成器 - 完整使用說明書

**版本**: 2.0  
**更新日期**: 2025-07-29  
**適用系統**: Windows/macOS/Linux

> 智能化的電路板佈局指南自動生成工具

---

## 📖 目錄

1. [工具簡介](#工具簡介)
2. [系統需求](#系統需求)
3. [快速開始](#快速開始)
4. [詳細使用方法](#詳細使用方法)
5. [配置自定義](#配置自定義)
6. [使用者驗證指南](#使用者驗證指南)
7. [常見問題](#常見問題)
8. [故障排除](#故障排除)

---

## ⚠️ 重要說明

**`run.bat` / `launch.sh` 只是功能測試腳本，不是真正的使用方法！**

- `run.bat` / `launch.sh` = 驗證工具能否正常工作
- 實際使用 = 需要選擇你自己的 netlist 檔案
6. [輸出說明](#輸出說明)
7. [故障排除](#故障排除)
8. [進階用法](#進階用法)

---

## 🚀 工具簡介

阻抗控制佈局指南生成器是一個**智能化的電路板設計輔助工具**，能夠：

- 🔍 **自動解析** Netlist 檔案，提取網路名稱
- 🧠 **智能分類** 網路類型 (I2C, SPI, RF, PCIe, Power 等)
- 📋 **自動應用** 對應的佈局規則和阻抗要求
- 📊 **生成專業** Excel 格式的佈局指南文檔
- ⚙️ **支援自定義** 分類規則和佈局要求

### 從手動到自動的轉變
- **以前**: 手動查看 netlist → 手動分類 → 手動查找規則 → 手動填表 (數小時)
- **現在**: 一鍵處理 → 自動完成所有步驟 (幾秒鐘)

---

## 💻 系統需求

### 基本需求
- **作業系統**: Windows 10/11, macOS 10.14+, Linux
- **Python**: 3.8 或更新版本
- **記憶體**: 最少 512MB 可用記憶體
- **硬碟**: 至少 100MB 可用空間

### 必要套件
工具會自動安裝以下套件：
- `pandas` - 資料處理
- `openpyxl` - Excel 檔案操作
- `pyyaml` - 配置檔案處理
- `PyQt5` - 圖形使用者介面 (GUI 模式)

---

## 🚀 快速開始

### 方法一：一鍵啟動 (推薦)

**Windows 用戶**:
```cmd
雙擊 run.bat
```

**Linux/macOS 用戶**:
```bash
./launch.sh
```

### 方法二：命令列啟動

```bash
# 1. 進入專案目錄
cd impedenceControll

# 2. 啟動工具
cd src
python main.py netlist檔案.net -o 輸出檔案.xlsx
```

### 方法三：圖形介面啟動

```bash
python run_simple_gui.py
```

---

## 📋 詳細使用方法

### 🗂️ 檔案來源說明

#### Netlist 檔案 (你提供)
- **來源**: 你的 PCB 設計軟體 (Altium, KiCad, Cadence 等)
- **格式**: .net, .sp, .cir, .txt
- **範例位置**: 你可以參考 `tests/data/sample_netlist.net`

#### Layout Rules (內建或自定義)
- **預設規則**: `src/config/default_config.yaml`
- **包含**: I2C, SPI, RF, PCIe, USB, Power, Clock 等規則
- **自定義**: 你可以建立自己的 .yaml 配置檔案

#### Layout Guide 模板 (自動生成)
- **格式**: 標準 Excel 格式
- **欄位**: Category, Net Name, Description, Impedance, Type, Width 等
- **無需模板**: 工具自動建立專業格式

### 📋 實際使用步驟

#### 步驟一：準備你的檔案
你需要準備：
- 📄 **你的 Netlist 檔案** (.net, .sp, .cir, .txt)
- ⚙️ **配置檔案** (可選，不提供則使用預設規則)

#### 步驟二：選擇使用方式

## 📋 使用方法

### 🖥️ 圖形介面使用 (推薦新手)

1. **啟動 GUI**
   ```bash
   python run_simple_gui.py
   ```

2. **選擇檔案**
   - 點擊 "瀏覽..." 選擇你的 Netlist 檔案
   - 點擊 "另存為..." 選擇輸出位置

3. **生成指南**
   - 點擊 "生成佈局指南" 按鈕
   - 等待處理完成
   - 自動開啟生成的 Excel 檔案

### ⌨️ 命令列使用 (推薦專業用戶)

#### 基本語法
```bash
python main.py [netlist檔案] [選項]
```

#### 常用範例

**處理單一檔案**:
```bash
python main.py my_netlist.net -o layout_guide.xlsx
```

**使用自定義配置**:
```bash
python main.py netlist.net -c custom_config.yaml -o output.xlsx
```

**查看幫助**:
```bash
python main.py --help
```

#### 完整參數說明

| 參數 | 說明 | 範例 |
|------|------|------|
| `netlist檔案` | 輸入的 netlist 檔案路徑 | `pcb_design.net` |
| `-o, --output` | 輸出 Excel 檔案路徑 | `-o result.xlsx` |
| `-c, --config` | 自定義配置檔案路徑 | `-c my_rules.yaml` |
| `-t, --template` | Excel 模板檔案 (可選) | `-t template.xlsx` |

---

## ⚙️ 配置自定義

### 自定義分類規則

建立 `my_config.yaml` 檔案：

```yaml
net_classification_rules:
  UART:
    keywords: ["UART", "RX", "TX", "RTS", "CTS"]
    patterns: [".*UART.*", ".*RX.*", ".*TX.*"]
    category: "Communication Interface"
    signal_type: "UART"
    priority: 25
    
  CAN:
    keywords: ["CAN", "CANH", "CANL"]
    patterns: [".*CAN.*"]
    category: "Automotive Interface"
    signal_type: "Differential"
    priority: 30

layout_rules:
  UART:
    impedance: "50 Ohm"
    description: "UART通訊線路佈局規則"
    width: "5 mil"
    length_limit: "12 inch"
    spacing: "3W spacing"
    notes: "保持串列通訊品質"
```

### 使用自定義配置
```bash
python main.py netlist.net -c my_config.yaml -o output.xlsx
```

---

## 📊 輸出說明

### Excel 檔案結構

生成的 Excel 檔案包含以下欄位：

| 欄位名稱 | 說明 | 範例值 |
|----------|------|--------|
| **Category** | 網路分類 | Communication Interface |
| **Net Name** | 網路名稱 | I2C0_SCL |
| **Pin (MT7921)** | 晶片接腳 | A12 |
| **Description** | 詳細佈局規則描述 | I2C總線佈局要求... |
| **Impedance** | 阻抗要求 | 50 Ohm |
| **Type** | 信號類型 | I2C |
| **Width** | 線寬要求 | 5 mil |
| **Length Limit** | 長度限制 | 6 inch |
| **Spacing** | 間距要求 | 3W spacing |
| **Shielding** | 屏蔽要求 | Ground guard preferred |

### 支援的網路分類

| 分類 | 包含信號 | 典型阻抗 |
|------|----------|----------|
| **Communication Interface** | I2C, SPI, UART | 50 Ohm |
| **High Speed Interface** | PCIe, USB | 90/100 Ohm differential |
| **RF** | 天線, 射頻信號 | 50 Ohm |
| **Power** | 電源, 接地 | N/A |
| **Clock** | 時鐘信號 | 50 Ohm |
| **Other** | 一般 GPIO | 50 Ohm |

---

## 🔧 故障排除

### 常見問題

#### Q1: Python 找不到
**症狀**: `'python' 不是內部或外部命令`
**解決**: 
1. 從 [python.org](https://python.org) 下載 Python 3.8+
2. 安裝時勾選 "Add Python to PATH"
3. 重新開啟命令提示字元

#### Q2: 套件安裝失敗
**症狀**: `No module named 'pandas'`
**解決**:
```bash
pip install pandas openpyxl pyyaml PyQt5
```

#### Q3: 檔案找不到
**症狀**: `FileNotFoundError`
**解決**: 使用完整路徑或確認檔案存在
```bash
python main.py "C:\完整路徑\netlist.net" -o "C:\輸出路徑\result.xlsx"
```

#### Q4: Excel 檔案無法開啟
**症狀**: Excel 顯示檔案損壞
**解決**: 檢查 openpyxl 版本
```bash
pip install --upgrade openpyxl
```

### 診斷步驟

1. **檢查環境**
   ```bash
   python --version  # 應顯示 3.8+
   pip list | findstr pandas  # 檢查套件
   ```

2. **測試基本功能**
   ```bash
   cd src
   python main.py --help  # 查看幫助
   ```

3. **使用範例檔案測試**
   ```bash
   python main.py ../tests/data/sample_netlist.net
   ```

---

## 🎯 進階用法

### 批次處理多個檔案

建立批次處理腳本：

```python
# batch_process.py
import os
from pathlib import Path
from main import process_netlist_to_excel

netlist_dir = Path("netlist_files")
output_dir = Path("output_files")

for netlist_file in netlist_dir.glob("*.net"):
    output_file = output_dir / f"{netlist_file.stem}_layout_guide.xlsx"
    process_netlist_to_excel(netlist_file, output_path=output_file)
    print(f"處理完成: {output_file}")
```

### 整合到其他工具

```python
# 在你的 Python 程式中使用
from main import process_netlist_to_excel

result_path = process_netlist_to_excel(
    netlist_path=Path("design.net"),
    output_path=Path("layout_guide.xlsx")
)
print(f"佈局指南已生成: {result_path}")
```

### 自動化流程

```bash
# 結合其他工具的完整流程
altium_export.exe --netlist design.net    # 從 Altium 匯出
python main.py design.net -o guide.xlsx   # 生成佈局指南
email_tool.exe --send guide.xlsx          # 自動發送給團隊
```

---

## 🧪 使用者驗證指南

### 🎯 驗證目標
確保阻抗控制工具的以下功能正常運作：
- ✅ Netlist 檔案解析功能
- ✅ 網路名稱智能分類功能  
- ✅ 佈局規則自動應用功能
- ✅ Excel 檔案生成和格式化功能
- ✅ 配置檔案系統功能

### 📋 驗證前準備

#### 環境要求
- Python 3.8+ (建議 Python 3.13)
- 已安裝所需套件 (pandas, openpyxl, pyyaml)
- Windows/macOS/Linux 作業系統

#### 必要檔案確認
請確認以下檔案存在於專案目錄中：
```
impedenceControll/
├── src/
│   ├── main.py                    ✅ 主程式
│   ├── core/                      ✅ 核心模組
│   └── config/                    ✅ 配置檔案
├── tests/data/sample_netlist.net  ✅ 測試資料
├── requirements.txt               ✅ 依賴清單
└── test_integration.py            ✅ 整合測試
```

### 🚀 快速驗證步驟

#### 步驟 1: 環境驗證 (2分鐘)

1. **檢查 Python 版本**
   ```bash
   python --version
   ```
   **預期結果**: 顯示 Python 3.8 或更高版本

2. **安裝依賴套件**
   ```bash
   cd impedenceControll
   pip install -r requirements.txt
   ```
   **預期結果**: 所有套件成功安裝，無錯誤訊息

3. **驗證套件導入**
   ```bash
   python -c "import pandas, openpyxl, yaml; print('所有套件安裝成功')"
   ```
   **預期結果**: 顯示 "所有套件安裝成功"

#### 步驟 2: 快速整合測試 (3分鐘)

1. **執行自動整合測試**
   ```bash
   python test_integration.py
   ```
   **預期結果**:
   ```
   開始整合測試...
   [日誌訊息顯示處理步驟]
   整合測試成功! 輸出檔案: ..\test_output.xlsx
   檔案大小: 7879 位元組
   ```

2. **驗證輸出檔案**
   - ✅ 確認 `test_output.xlsx` 檔案已生成
   - ✅ 檔案大小約 7-8KB
   - ✅ 可以用 Excel 開啟

#### 步驟 3: 命令列介面驗證 (3分鐘)

1. **查看幫助訊息**
   ```bash
   cd src
   python main.py --help
   ```
   **預期結果**: 顯示完整的命令列參數說明

2. **使用範例 Netlist 執行**
   ```bash
   python main.py ../tests/data/sample_netlist.net -o manual_test_output.xlsx
   ```
   **預期結果**:
   - ✅ 顯示處理步驟日誌
   - ✅ 成功訊息: "成功生成佈局指南"
   - ✅ 生成 `manual_test_output.xlsx` 檔案

### ✅ 驗證檢查清單

#### 基本功能驗證
- [ ] Python 環境配置正確
- [ ] 所有依賴套件安裝成功
- [ ] 整合測試通過
- [ ] 命令列介面正常工作
- [ ] Excel 檔案成功生成

#### 內容品質驗證  
- [ ] 網路名稱正確提取 (20個)
- [ ] 智能分類功能正常 (4種類型)
- [ ] 佈局規則正確應用
- [ ] Excel 格式化正常
- [ ] 中文描述顯示正確

#### 進階功能驗證
- [ ] 自定義配置檔案支援
- [ ] 錯誤處理機制正常
- [ ] 效能表現符合預期
- [ ] 日誌輸出清晰可讀

---

## 📞 技術支援

### 文檔資源
- `README.md` - 專案概述
- `examples/` - 範例檔案和配置
- `tests/` - 測試案例和範例資料

### 版本資訊
- **當前版本**: 2.0
- **核心架構**: 模組化設計
- **配置系統**: YAML 驅動
- **支援格式**: .net, .sp, .cir, .txt

### 開發資訊
- **程式語言**: Python 3.8+
- **主要依賴**: pandas, openpyxl, pyyaml
- **架構模式**: 命令式 + 模組化
- **測試框架**: pytest

---

## 🎉 開始使用

現在你已經了解了工具的完整功能！選擇最適合你的使用方式：

- 🖱️ **新手用戶**: 使用簡單圖形介面 (`python run_simple_gui.py`)
- 🔧 **進階用戶**: 使用進階圖形介面 (`python run_advanced_gui.py`)
- ⌨️ **專業用戶**: 使用命令列 (`python main.py`)
- 📝 **自定義用戶**: 批次處理和配置編輯

從今天開始，告別手動分類和查找規則的繁瑣工作，享受自動化佈局指南生成的便利！

---

*© 2025 阻抗控制工具開發團隊*