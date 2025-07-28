# 🚀 阻抗控制工具快速啟動指南

## 🎯 三種啟動方式

### 方式一：一鍵啟動 (最推薦！)

**Windows 用戶**:
```cmd
# 雙擊執行或在命令列執行
quick_start.bat
```

**Linux/macOS 用戶**:
```bash
# 賦予執行權限
chmod +x quick_start.sh

# 執行腳本
./quick_start.sh
```

### 方式二：命令列啟動

```bash
# 1. 進入專案目錄
cd impedenceControll/src

# 2. 基本啟動
python main.py [netlist檔案] -o [輸出檔案.xlsx]
```

### 方式三：測試模式啟動

```bash
# 快速驗證工具功能
python test_integration.py
```

---

## 📝 實際操作範例

### 🎯 **範例 A: 處理範例檔案**
```bash
cd src
python main.py ../tests/data/sample_netlist.net -o 範例結果.xlsx
```
**結果**: 生成包含 20 個網路分類的 Excel 檔案

### 🎯 **範例 B: 處理你的 netlist**
```bash
python main.py "D:\MyProject\pcb_netlist.net" -o "D:\MyProject\layout_guide.xlsx"
```

### 🎯 **範例 C: 使用自定義規則**
```bash
python main.py my_netlist.net -c ../examples/configs/custom_config_example.yaml -o custom_result.xlsx
```

---

## 🔧 首次使用步驟

### 步驟 1: 環境準備 (1 分鐘)
```bash
# 檢查 Python 版本 (需要 3.8+)
python --version

# 安裝必要套件
pip install pandas openpyxl pyyaml
```

### 步驟 2: 快速測試 (2 分鐘)
```bash
# 執行內建測試
python test_integration.py
```
**成功標誌**: 看到 "整合測試成功! 輸出檔案: ../test_output.xlsx"

### 步驟 3: 處理你的檔案 (1 分鐘)
```bash
cd src
python main.py "你的netlist檔案路徑" -o "輸出檔案名稱.xlsx"
```

---

## 📊 輸出檔案說明

生成的 Excel 檔案包含：

| 欄位 | 說明 | 範例 |
|------|------|------|
| Category | 網路分類 | Communication Interface |
| Net Name | 網路名稱 | I2C0_SCL |
| Description | 佈局規則描述 | I2C總線佈局要求... |
| Impedance | 阻抗要求 | 50 Ohm |
| Type | 信號類型 | I2C |
| Width | 線寬要求 | 5 mil |
| Length Limit | 長度限制 | 6 inch |

---

## 🎨 自定義配置

### 建立自定義配置檔案
```yaml
# my_config.yaml
net_classification_rules:
  UART:
    keywords: ["UART", "RX", "TX"]
    category: "Communication Interface"
    signal_type: "UART"
    priority: 25

layout_rules:
  UART:
    impedance: "50 Ohm"
    description: "UART通訊佈局規則"
    width: "5 mil"
```

### 使用自定義配置
```bash
python main.py your_netlist.net -c my_config.yaml -o result.xlsx
```

---

## 🚨 常見問題快速解決

### 問題 1: 找不到 Python
```bash
# 下載安裝 Python 3.8+ 從 python.org
# 或使用包管理器安裝
```

### 問題 2: ModuleNotFoundError
```bash
pip install pandas openpyxl pyyaml
```

### 問題 3: 找不到檔案
```bash
# 使用絕對路徑
python main.py "C:\完整路徑\到\你的檔案.net" -o "輸出.xlsx"
```

### 問題 4: 權限問題
```bash
# 確保輸出目錄有寫入權限
# 或輸出到用戶目錄
python main.py input.net -o "~/desktop/output.xlsx"
```

---

## ⚡ 效能優化建議

- **小檔案** (< 100 nets): 直接使用，秒級完成
- **中檔案** (100-1000 nets): 預期 5-10 秒
- **大檔案** (> 1000 nets): 可能需要 30 秒-1 分鐘

---

## 📞 需要幫助？

1. **查看幫助**: `python main.py --help`
2. **檢查文檔**: 閱讀 `README.md`
3. **驗證功能**: 執行驗證檢查清單
4. **查看範例**: 檢查 `examples/` 目錄

---

## 🎉 使用成功標誌

- ✅ 命令執行無錯誤
- ✅ 生成 Excel 檔案
- ✅ 檔案可正常開啟
- ✅ 包含預期的網路分類和佈局規則

**恭喜！你已經成功掌握工具使用方法！** 🎊