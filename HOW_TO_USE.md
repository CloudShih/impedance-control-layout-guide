# 🚀 如何使用阻抗控制工具

## ⚠️ 重要說明

**`run.bat` 只是功能測試，不是真正的使用方法！**

- `run.bat` = 驗證工具能否正常工作
- 實際使用 = 需要選擇你自己的檔案

---

## 📋 實際使用步驟

### 步驟一：準備你的檔案

你需要準備：
- 📄 **你的 Netlist 檔案** (.net, .sp, .cir, .txt)
- ⚙️ **配置檔案** (可選，不提供則使用預設規則)

### 步驟二：選擇使用方式

#### 🖥️ 方式一：圖形介面 (最簡單)

```bash
cd src
python simple_gui.py
```

然後：
1. 點擊 "瀏覽..." 選擇你的 netlist 檔案
2. 點擊 "另存為..." 選擇輸出位置  
3. 點擊 "生成佈局指南"
4. 等待完成，自動開啟結果

#### ⌨️ 方式二：命令列

```bash
cd src
python main.py "C:\你的路徑\你的netlist.net" -o "C:\輸出路徑\結果.xlsx"
```

#### ⚙️ 方式三：使用自定義配置

```bash
cd src  
python main.py "你的netlist.net" -c "自定義配置.yaml" -o "結果.xlsx"
```

---

## 📂 檔案來源說明

### 🗂️ Netlist 檔案 (你提供)
- **來源**: 你的 PCB 設計軟體 (Altium, KiCad, Cadence 等)
- **格式**: .net, .sp, .cir, .txt
- **範例位置**: 你可以參考 `tests/data/sample_netlist.net`

### 📋 Layout Rules (內建或自定義)
- **預設規則**: `src/config/default_config.yaml`
- **包含**: I2C, SPI, RF, PCIe, USB, Power, Clock 等規則
- **自定義**: 你可以建立自己的 .yaml 配置檔案

### 📊 Layout Guide 模板 (自動生成)
- **格式**: 標準 Excel 格式
- **欄位**: Category, Net Name, Description, Impedance, Type, Width 等
- **無需模板**: 工具自動建立專業格式

---

## 🎯 實際範例操作

### 範例一：處理你的 PCB 設計

假設你有一個名為 `my_pcb.net` 的 netlist 檔案：

```bash
cd src
python main.py "D:\PCB_Projects\my_pcb.net" -o "D:\PCB_Projects\layout_guide.xlsx"
```

### 範例二：使用 GUI 操作

1. 執行 `python src/simple_gui.py`
2. 在 GUI 中選擇 `D:\PCB_Projects\my_pcb.net`
3. 選擇輸出為 `D:\PCB_Projects\layout_guide.xlsx`  
4. 點擊生成

### 範例三：批次處理多個檔案

```python
# batch_process.py
import os
from pathlib import Path
import sys
sys.path.append('src')
from main import process_netlist_to_excel

netlist_folder = Path("D:/PCB_Projects/netlists/")
output_folder = Path("D:/PCB_Projects/guides/")

for netlist_file in netlist_folder.glob("*.net"):
    output_file = output_folder / f"{netlist_file.stem}_guide.xlsx"
    process_netlist_to_excel(netlist_file, output_path=output_file)
    print(f"完成: {output_file}")
```

---

## ⚙️ 自定義配置範例

如果你想要自己的分類規則，建立 `my_rules.yaml`：

```yaml
net_classification_rules:
  UART:
    keywords: ["UART", "RX", "TX", "RTS", "CTS"]
    patterns: [".*UART.*", ".*RX.*", ".*TX.*"]
    category: "Communication Interface"
    signal_type: "UART"
    priority: 25

layout_rules:
  UART:
    impedance: "50 Ohm"
    description: "UART通訊線路需要適當的阻抗控制"
    width: "5 mil"
    length_limit: "12 inch"
    spacing: "3W spacing"
```

然後使用：
```bash
python main.py my_netlist.net -c my_rules.yaml -o output.xlsx
```

---

## 🔍 檔案處理流程

```
你的 Netlist 檔案
        ↓
   [Netlist 解析器]  ← 提取網路名稱
        ↓
   [智能分類器]     ← 根據規則分類
        ↓  
   [規則引擎]       ← 應用佈局規則
        ↓
   [Excel 生成器]   ← 生成專業報表
        ↓
   你的佈局指南.xlsx
```

---

## ❓ 常見問題

**Q: 我的 netlist 格式支援嗎？**
A: 支援 .net, .sp, .cir, .txt 等常見格式

**Q: 可以處理中文網路名嗎？**  
A: 可以，工具支援 Unicode

**Q: 輸出的 Excel 可以修改嗎？**
A: 當然可以，這就是標準的 Excel 檔案

**Q: 如何添加新的信號類型？**
A: 編輯配置檔案或建立自定義配置

---

## 🎉 開始使用

記住：**`run.bat` 只是測試工具功能，真正使用請選擇上面的方法！**

最推薦新手使用圖形介面：
```bash
python src/simple_gui.py
```

簡單、直觀、不會出錯！