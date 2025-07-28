"""
Help panel widget for displaying operation tutorials
操作教學面板元件
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QTabWidget, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor


class HelpPanel(QWidget):
    """
    Help panel showing operation tutorials and tips
    顯示操作教學和提示的說明面板
    """
    
    # Signal emitted when user wants to navigate to a specific tab
    navigateToTab = pyqtSignal(str)  # tab name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_context = "overview"
        self.init_ui()
        self.load_tutorial_content()
    
    def init_ui(self):
        """Initialize the help panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Title
        title_label = QLabel("操作教學")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Context selector
        self.create_context_selector(layout)
        
        # Content area
        self.content_area = QTextEdit()
        self.content_area.setReadOnly(True)
        self.content_area.setMaximumHeight(400)
        layout.addWidget(self.content_area)
        
        # Quick action buttons
        self.create_quick_actions(layout)
        
        # Apply styling
        self.apply_styling()
    
    def create_context_selector(self, parent_layout):
        """Create context selector buttons"""
        selector_layout = QHBoxLayout()
        
        # Context buttons
        self.context_buttons = {}
        contexts = [
            ("overview", "總覽"),
            ("signal", "信號規則"),
            ("layout", "佈局規則"),
            ("template", "模板設定"),
            ("process", "處理流程")
        ]
        
        for context_id, display_name in contexts:
            btn = QPushButton(display_name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, ctx=context_id: self.switch_context(ctx))
            self.context_buttons[context_id] = btn
            selector_layout.addWidget(btn)
        
        # Set initial selection
        self.context_buttons["overview"].setChecked(True)
        
        parent_layout.addLayout(selector_layout)
    
    def create_quick_actions(self, parent_layout):
        """Create quick action buttons"""
        actions_frame = QFrame()
        actions_layout = QVBoxLayout(actions_frame)
        
        # Quick actions label
        quick_label = QLabel("快速操作")
        quick_font = QFont()
        quick_font.setPointSize(10)
        quick_font.setBold(True)
        quick_label.setFont(quick_font)
        actions_layout.addWidget(quick_label)
        
        # Action buttons
        self.quick_actions = [
            ("新增信號規則", "signal", "add_signal_rule"),
            ("載入配置檔案", "overview", "load_config"),
            ("驗證配置", "overview", "validate_config"),
            ("處理Netlist", "process", "process_netlist")
        ]
        
        for action_text, context, action_id in self.quick_actions:
            btn = QPushButton(action_text)
            btn.clicked.connect(lambda checked, ctx=context, aid=action_id: self.handle_quick_action(ctx, aid))
            actions_layout.addWidget(btn)
        
        parent_layout.addWidget(actions_frame)
    
    def switch_context(self, context_id):
        """Switch to a different help context"""
        # Update button states
        for btn_id, btn in self.context_buttons.items():
            btn.setChecked(btn_id == context_id)
        
        # Update content
        self.current_context = context_id
        self.update_content()
    
    def update_content(self):
        """Update help content based on current context"""
        content = self.get_context_content(self.current_context)
        self.content_area.setHtml(content)
    
    def get_context_content(self, context_id):
        """Get help content for specific context"""
        contents = {
            "overview": self.get_overview_content(),
            "signal": self.get_signal_rules_content(),
            "layout": self.get_layout_rules_content(),
            "template": self.get_template_content(),
            "process": self.get_process_content()
        }
        
        return contents.get(context_id, "內容準備中...")
    
    def get_overview_content(self):
        """Get overview help content"""
        return """
        <h3>🚀 歡迎使用阻抗控制佈局指南生成器</h3>
        
        <h4>📋 主要功能</h4>
        <ul>
        <li><b>信號規則管理</b> - 定義網路名稱的分類規則</li>
        <li><b>佈局規則設定</b> - 配置各類信號的佈局要求</li>
        <li><b>模板自定義</b> - 自定義Excel輸出格式</li>
        <li><b>Netlist處理</b> - 自動分析並生成佈局指南</li>
        </ul>
        
        <h4>🎯 快速開始</h4>
        <ol>
        <li>點擊 <b>檔案 → 開啟配置</b> 載入現有配置</li>
        <li>或直接使用預設配置開始編輯</li>
        <li>在各個標籤頁中配置規則</li>
        <li>使用 <b>Netlist處理</b> 標籤處理網表檔案</li>
        </ol>
        
        <h4>💡 小提示</h4>
        <ul>
        <li>將滑鼠懸停在輸入欄位上可看到詳細說明</li>
        <li>使用 <b>Ctrl+S</b> 快速儲存配置</li>
        <li>使用 <b>編輯 → 驗證配置</b> 檢查設定是否正確</li>
        </ul>
        """
    
    def get_signal_rules_content(self):
        """Get signal rules help content"""
        return """
        <h3>⚡ 信號規則管理</h3>
        
        <h4>📝 規則組成</h4>
        <ul>
        <li><b>規則名稱</b> - 唯一的規則識別名稱</li>
        <li><b>類別</b> - 信號所屬的大類別</li>
        <li><b>信號類型</b> - 電氣特性分類</li>
        <li><b>優先級</b> - 匹配順序（數值越高優先級越高）</li>
        </ul>
        
        <h4>🎯 匹配條件</h4>
        <ul>
        <li><b>關鍵字</b> - 簡單的字串包含匹配</li>
        <li><b>正則表達式</b> - 精確的模式匹配</li>
        <li><b>精確匹配</b> - 完全相同的名稱匹配</li>
        </ul>
        
        <h4>✏️ 編輯步驟</h4>
        <ol>
        <li>在左側列表選擇要編輯的規則</li>
        <li>在右側面板修改規則參數</li>
        <li>點擊 <b>儲存規則</b> 確認修改</li>
        <li>使用 <b>新增規則</b> 按鈕創建新規則</li>
        </ol>
        
        <h4>💡 最佳實踐</h4>
        <ul>
        <li>為I2C/SPI等常用介面設定較高優先級</li>
        <li>使用正則表達式處理複雜的命名規則</li>
        <li>在描述中詳細說明規則的用途</li>
        </ul>
        """
    
    def get_layout_rules_content(self):
        """Get layout rules help content"""
        return """
        <h3>📏 佈局規則設定</h3>
        
        <h4>⚙️ 主要參數</h4>
        <ul>
        <li><b>阻抗控制</b> - 走線特徵阻抗（如50Ω、100Ω）</li>
        <li><b>線寬</b> - 走線寬度要求</li>
        <li><b>間距</b> - 走線間距規範</li>
        <li><b>長度限制</b> - 最大走線長度</li>
        <li><b>過孔規則</b> - 換層和過孔使用規範</li>
        </ul>
        
        <h4>🔧 進階設定</h4>
        <ul>
        <li><b>差分阻抗</b> - 差分信號對的阻抗</li>
        <li><b>層疊要求</b> - 建議使用的PCB層</li>
        <li><b>屏蔽要求</b> - 接地保護需求</li>
        </ul>
        
        <h4>📊 常見阻抗值</h4>
        <ul>
        <li><b>50Ω</b> - 單端信號標準值</li>
        <li><b>90Ω</b> - USB差分信號</li>
        <li><b>100Ω</b> - 高速差分信號</li>
        <li><b>75Ω</b> - 射頻信號</li>
        </ul>
        
        <h4>💡 設計建議</h4>
        <ul>
        <li>根據信號頻率選擇合適的阻抗值</li>
        <li>高頻信號需要更嚴格的間距控制</li>
        <li>電源信號著重電流承載能力</li>
        </ul>
        """
    
    def get_template_content(self):
        """Get template help content"""
        return """
        <h3>📋 模板設定管理</h3>
        
        <h4>🗂️ 欄位管理</h4>
        <ul>
        <li><b>內部名稱</b> - 系統識別用的欄位ID</li>
        <li><b>顯示名稱</b> - Excel中顯示的欄位標題</li>
        <li><b>欄位順序</b> - 在Excel中的顯示順序</li>
        <li><b>顯示控制</b> - 決定欄位是否在輸出中顯示</li>
        </ul>
        
        <h4>⚡ 快速操作</h4>
        <ul>
        <li><b>新增欄位</b> - 增加自定義輸出欄位</li>
        <li><b>刪除欄位</b> - 移除不需要的欄位</li>
        <li><b>調整順序</b> - 上移/下移欄位位置</li>
        <li><b>隱藏欄位</b> - 暫時隱藏不需要的欄位</li>
        </ul>
        
        <h4>📊 輸出設定</h4>
        <ul>
        <li><b>工作表名稱</b> - Excel中的分頁名稱</li>
        <li><b>自動篩選</b> - 啟用Excel篩選功能</li>
        <li><b>凍結窗格</b> - 固定標題行</li>
        <li><b>自動調整欄寬</b> - 根據內容調整欄位寬度</li>
        </ul>
        
        <h4>💡 自定義技巧</h4>
        <ul>
        <li>使用描述性的欄位名稱提高可讀性</li>
        <li>合理安排欄位順序，重要資訊靠前</li>
        <li>可以隱藏技術性較強的欄位簡化輸出</li>
        </ul>
        """
    
    def get_process_content(self):
        """Get processing help content"""
        return """
        <h3>⚙️ Netlist 處理流程</h3>
        
        <h4>📁 支援的檔案格式</h4>
        <ul>
        <li><b>.net</b> - 標準網表格式</li>
        <li><b>.sp</b> - SPICE網表格式</li>
        <li><b>.cir</b> - 電路模擬網表</li>
        <li><b>.txt</b> - 純文字網路清單</li>
        </ul>
        
        <h4>🔄 處理步驟</h4>
        <ol>
        <li><b>解析網表</b> - 提取網路名稱清單</li>
        <li><b>規則匹配</b> - 根據信號規則進行分類</li>
        <li><b>套用佈局規則</b> - 為每個網路指定佈局要求</li>
        <li><b>生成Excel</b> - 按模板格式輸出佈局指南</li>
        </ol>
        
        <h4>✅ 處理前檢查</h4>
        <ul>
        <li>確認已載入正確的配置檔案</li>
        <li>驗證信號規則和佈局規則無錯誤</li>
        <li>檢查Netlist檔案格式正確</li>
        <li>確保有足夠的磁碟空間儲存輸出檔案</li>
        </ul>
        
        <h4>❌ 常見問題</h4>
        <ul>
        <li><b>找不到匹配規則</b> - 網路會歸類為"Default"</li>
        <li><b>規則衝突</b> - 系統選擇優先級最高的規則</li>
        <li><b>檔案格式錯誤</b> - 檢查Netlist檔案編碼和格式</li>
        </ul>
        
        <h4>🎯 優化建議</h4>
        <ul>
        <li>定期檢查未分類的網路，完善規則庫</li>
        <li>根據專案特性調整規則優先級</li>
        <li>保存常用配置作為範本</li>
        </ul>
        """
    
    def handle_quick_action(self, context, action_id):
        """Handle quick action button clicks"""
        # Switch to appropriate context first
        if context != self.current_context:
            self.switch_context(context)
        
        # Emit navigation signal
        if action_id == "add_signal_rule":
            self.navigateToTab.emit("信號規則")
        elif action_id == "load_config":
            self.navigateToTab.emit("load_config")
        elif action_id == "validate_config":
            self.navigateToTab.emit("validate_config")
        elif action_id == "process_netlist":
            self.navigateToTab.emit("Netlist處理")
    
    def load_tutorial_content(self):
        """Load initial tutorial content"""
        self.update_content()
    
    def apply_styling(self):
        """Apply custom styling to the help panel"""
        self.setStyleSheet("""
            HelpPanel {
                background-color: #2e2e2e;
                color: #f0f0f0;
            }
            
            QPushButton {
                background-color: #444444;
                border: 1px solid #666666;
                padding: 6px 12px;
                border-radius: 3px;
                color: #f0f0f0;
                font-size: 9pt;
            }
            
            QPushButton:hover {
                background-color: #555555;
            }
            
            QPushButton:checked {
                background-color: #666666;
                border: 2px solid #888888;
            }
            
            QTextEdit {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 8px;
                color: #f0f0f0;
                font-family: "Microsoft YaHei", "微軟雅黑";
                font-size: 9pt;
                line-height: 1.4;
            }
            
            QLabel {
                color: #f0f0f0;
            }
            
            QFrame {
                border: 1px solid #555555;
                border-radius: 3px;
                margin: 4px;
                padding: 4px;
            }
        """)
    
    def set_context_from_tab(self, tab_name):
        """Set help context based on current tab"""
        tab_context_map = {
            "信號規則": "signal",
            "佈局規則": "layout", 
            "模板設定": "template",
            "Netlist處理": "process"
        }
        
        context = tab_context_map.get(tab_name, "overview")
        self.switch_context(context)