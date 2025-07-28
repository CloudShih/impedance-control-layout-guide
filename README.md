# Impedance Control Layout Guide Generator

一個智能的阻抗控制佈局指南生成工具，能夠從 Netlist 檔案自動提取網路名稱，根據預定義規則進行分類，並生成標準化的 Excel 格式佈局指南。

## 功能特色

- 🔍 **智能 Netlist 解析**：支援多種 netlist 格式
- 📊 **靈活規則配置**：可配置的網路分類和佈局規則
- 📋 **動態模板映射**：自動適應不同 Excel 模板格式
- 🎯 **精確分類系統**：基於正則表達式和關鍵字的智能分類
- 🖥️ **友善使用界面**：直觀的 GUI 操作介面

## 專案結構

```
impedenceControll/
├── src/
│   ├── core/                    # 核心功能模組
│   ├── config/                  # 配置檔案
│   └── ui/                      # 使用者界面
├── tests/                       # 測試套件
├── examples/                    # 範例檔案
└── docs/                        # 說明文檔
```

## 使用方法

1. 準備 Netlist 檔案 (.net)
2. 準備 Layout Guide Template (Excel)
3. 設定 Layout Rules 配置檔案
4. 執行工具生成結果

## 開發者資訊

- 語言：Python 3.8+
- 主要依賴：PyQt5, pandas, openpyxl
- 測試框架：pytest