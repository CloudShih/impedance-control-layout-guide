# 🔧 故障排除指南

## 🚨 quick_start.bat Crash 問題

### 常見 Crash 原因和解決方案

#### 1. 編碼問題 (最常見)
**症狀**: 腳本執行後立即關閉或顯示亂碼  
**原因**: Windows 命令列不支援 Unicode 字符  
**解決方案**: 
```cmd
# 使用修復版本
quick_start_fixed.bat

# 或使用簡化版本  
start.bat
```

#### 2. Python 未安裝
**症狀**: "python 不是內部或外部命令"  
**解決方案**:
```cmd
# 1. 下載安裝 Python 3.8+ 從 python.org
# 2. 安裝時勾選 "Add Python to PATH"
# 3. 重新開啟命令提示字元
```

#### 3. 權限問題
**症狀**: "拒絕存取" 或 "Permission denied"  
**解決方案**:
```cmd
# 以管理員身分執行命令提示字元
# 右鍵 -> "以系統管理員身分執行"
```

#### 4. 路徑問題
**症狀**: "找不到檔案" 或 "系統找不到指定的路徑"  
**解決方案**:
```cmd
# 確認在正確目錄執行
cd D:\ClaudeCode\projects\impedenceControll
dir  # 確認看到 quick_start.bat
```

---

## 🛠️ 診斷步驟

### 步驟 1: 執行診斷腳本
```cmd
diagnose.bat
```
這會檢查所有環境配置

### 步驟 2: 手動測試
```cmd
# 檢查 Python
python --version

# 檢查套件
pip list | findstr pandas

# 手動執行測試
python test_integration.py
```

### 步驟 3: 逐項驗證
```cmd
# 進入 src 目錄
cd src

# 直接執行主程式
python main.py ../tests/data/sample_netlist.net
```

---

## 💡 替代啟動方法

### 方法 1: 使用簡化腳本
```cmd
start.bat  # 更簡單，不會 crash
```

### 方法 2: 手動命令列
```cmd
cd src
python main.py ../tests/data/sample_netlist.net -o test.xlsx
```

### 方法 3: 分步執行
```cmd
# 1. 安裝套件
pip install pandas openpyxl pyyaml

# 2. 執行測試
python test_integration.py

# 3. 使用工具
cd src && python main.py ../tests/data/sample_netlist.net
```

---

## 🔍 深度除錯

### 檢查 Python 環境
```cmd
python -c "import sys; print(sys.version)"
python -c "import sys; print(sys.executable)"
```

### 檢查工作目錄
```cmd
echo %CD%
dir *.py
dir tests\data\
```

### 檢查模組導入
```cmd
python -c "import pandas, openpyxl, yaml; print('All modules OK')"
```

### 檢查檔案編碼
```cmd
# 如果看到亂碼，嘗試改變編碼
chcp 65001  # UTF-8
chcp 950    # 繁體中文
```

---

## 📞 仍然無法解決？

### 方案 A: 使用最基本方法
```cmd
cd src
python main.py --help  # 查看說明
python main.py ../tests/data/sample_netlist.net  # 直接執行
```

### 方案 B: 檢查系統要求
- Windows 10/11
- Python 3.8 或更新版本  
- 足夠的磁碟空間 (>100MB)
- 網路連線 (用於安裝套件)

### 方案 C: 重新安裝 Python
1. 從 python.org 下載最新版本
2. 安裝時選擇 "Add Python to PATH"
3. 重新開啟命令提示字元
4. 重新執行腳本

---

## ✅ 成功標誌

當你看到以下內容表示成功:
```
整合測試成功! 輸出檔案: ..\test_output.xlsx
檔案大小: 7879 位元組
```

---

## 🆘 緊急聯絡資訊

如果所有方法都失敗，請：
1. 執行 `diagnose.bat` 並記錄輸出
2. 檢查 Python 版本和套件版本
3. 嘗試最基本的手動命令
4. 查看錯誤訊息的具體內容

記住：即使啟動腳本失敗，核心工具功能仍然可以手動使用！