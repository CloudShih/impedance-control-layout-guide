# 阻抗控制佈局指南生成器 - 打包說明

## 概述
本文檔說明如何將阻抗控制佈局指南生成器打包為獨立的可執行檔案。

## 打包工具
- **PyInstaller 6.14.2** - Python 應用打包工具
- **UPX 壓縮** - 可執行檔壓縮以減少檔案大小

## 打包配置
打包配置檔案：`impedance_tool.spec`

### 主要設定
- **入口點**: `run_advanced_gui.py`
- **包含檔案**:
  - 配置檔案: `src/config/default_config.yaml`
  - 配置備份: `src/config/default_backup/default_config.yaml`
  - 範例配置: `examples/configs/*.yaml`
  - 說明文件: `README.md`, `USER_MANUAL.md`

### 隱藏匯入模組
- PyQt5 相關模組 (QtCore, QtGui, QtWidgets)
- 應用程式模組 (controllers, models, views, widgets, core)
- 資料處理模組 (pandas, openpyxl, yaml, jsonschema)

### 排除模組
- 測試相關 (pytest, pytest_cov, tests)
- 不必要模組 (tkinter, matplotlib, numpy, scipy)

## 打包步驟

### 1. 環境準備
```bash
pip install pyinstaller
```

### 2. 清理舊檔案
```bash
rm -rf build dist
```

### 3. 執行打包
```bash
pyinstaller impedance_tool.spec --clean --distpath="dist" --workpath="build"
```

### 4. 驗證結果
生成的可執行檔位於 `dist/阻抗控制佈局指南生成器.exe`

## 打包結果

### 檔案資訊
- **檔案名稱**: 阻抗控制佈局指南生成器.exe
- **檔案大小**: 約 103MB
- **執行方式**: 雙擊直接執行，無需安裝 Python 環境
- **相容性**: Windows 64-bit

### 包含功能
- ✅ 完整的圖形化介面
- ✅ Netlist 檔案處理
- ✅ 信號規則分類
- ✅ 佈局規則應用
- ✅ Excel 檔案輸出
- ✅ 配置檔案管理
- ✅ 工具提示系統

## 版本歷史

### v2.0.0 (2025-07-29)
- 初始打包版本
- 包含所有核心功能
- 修復阻抗單位驗證問題
- 支援配置備份功能

## 使用說明

### 系統需求
- Windows 10/11 (64-bit)
- 無需額外安裝 Python 或依賴套件

### 執行方式
1. 解壓縮或下載 `阻抗控制佈局指南生成器.exe`
2. 雙擊執行檔啟動應用程式
3. 根據介面指引進行操作

### 注意事項
- 首次執行可能需要較長啟動時間
- 防毒軟體可能誤報，請加入信任清單
- 建議在有足夠磁碟空間的位置執行

## 疑難排解

### 常見問題
1. **執行檔無法啟動**
   - 檢查是否為 64-bit Windows 系統
   - 確認防毒軟體未封鎖執行檔

2. **啟動速度慢**
   - 屬正常現象，首次啟動需要解壓縮和初始化
   - 後續執行會較快

3. **配置檔案問題**
   - 可執行檔內建預設配置
   - 如需自訂配置，請使用介面內的配置管理功能

## 開發者資訊
- 打包工具: PyInstaller 6.14.2
- Python 版本: 3.12.5
- 建置平台: Windows 11
- 建置日期: 2025-07-29

## 技術細節
- 單檔案打包 (onefile mode)
- UPX 壓縮啟用
- 隱藏控制台視窗 (windowed mode)
- 包含所有必要的 DLL 和資源檔案