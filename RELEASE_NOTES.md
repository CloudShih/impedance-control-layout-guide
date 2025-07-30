# 🎉 阻抗控制佈局指南生成器 v2.0.0 Release

> 專業的電路板佈局指南自動化生成工具

## 🚀 重大更新

### 新功能亮點

#### 🖥️ 雙GUI介面設計
- **簡單版介面** - 適合新手用戶，一鍵操作
- **進階版介面** - 提供完整的配置編輯功能

#### 📦 PyInstaller執行檔支援  
- **一鍵打包** - 自動生成獨立執行檔
- **無需Python環境** - 直接在任何Windows系統執行
- **配置文件內建** - 預設規則隨執行檔發布

#### ⚙️ 強化的配置系統
- **視覺化編輯器** - 圖形介面編輯所有設定
- **即時預覽** - 修改後立即看到效果
- **模板自定義** - 完全客製化Excel輸出格式

## 🔧 技術改進

### 架構升級
- ✅ **MVC設計模式** - 清晰的代碼結構
- ✅ **模組化設計** - 易於維護和擴展
- ✅ **絕對匯入** - 解決PyInstaller兼容性問題

### 品質保證
- ✅ **完整測試套件** - 單元測試覆蓋率高
- ✅ **錯誤處理機制** - 詳細的錯誤提示
- ✅ **日誌記錄系統** - 便於問題追蹤

## 📋 主要功能

### 智能解析
- 🔍 支援多種Netlist格式 (.net, .sp, .cir, .txt)
- 🧠 基於關鍵字和正則表達式的智能分類
- 🎯 自動識別信號類型 (高速、電源、時鐘、通訊等)

### 專業輸出
- 📊 標準化Excel佈局指南
- 📋 包含阻抗、線寬、間距等完整規格
- 🎨 專業格式化，直接可用於生產

### 靈活配置
- ⚙️ YAML格式配置文件
- 🔧 支援自定義分類規則
- 📝 可配置輸出模板

## 🐛 修復的問題

- ✅ **PyInstaller相對匯入錯誤** - 完全解決打包問題
- ✅ **配置文件載入失敗** - 修復執行檔中的路徑問題  
- ✅ **阻抗單位驗證錯誤** - 修正佈局規則驗證邏輯
- ✅ **numpy依賴缺失** - 修復打包後的依賴問題

## 💻 系統需求

### 開發環境
- Python 3.8+
- PyQt5 >= 5.15.0
- pandas >= 1.3.0
- 其他依賴見 requirements.txt

### 執行檔使用
- Windows 10/11 x64
- 無需安裝Python或其他依賴

## 🚀 快速開始

### 下載執行檔 (推薦)
1. 從 [Releases](../../releases) 下載最新的執行檔
2. 雙擊 `阻抗控制佈局指南生成器.exe` 啟動
3. 選擇你的Netlist文件，開始使用！

### 源碼安裝
```bash
git clone https://github.com/your-username/impedance-control-layout-guide.git
cd impedance-control-layout-guide
pip install -r requirements.txt
python run_advanced_gui.py
```

## 📚 文檔資源

- 📖 [用戶手冊](USER_MANUAL.md)
- 🔧 [打包說明](PACKAGING.md)  
- 📝 [變更日誌](CHANGELOG.md)
- 🧪 [Lesson Learn文檔](lesson_learn/)

## 🤝 貢獻指南

歡迎提交Issue和Pull Request！

### 開發環境設置
```bash
git clone https://github.com/your-username/impedance-control-layout-guide.git
cd impedance-control-layout-guide
pip install -r requirements.txt
pytest  # 運行測試
```

## 📄 授權協議

本專案採用 MIT 授權協議 - 詳見 [LICENSE](LICENSE) 文件

## 🙏 致謝

感謝所有貢獻者和使用者的支持！

---

**💫 享受更智能的PCB佈局設計體驗！**