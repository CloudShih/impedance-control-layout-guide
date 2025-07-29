"""
Signal Rule Editor widget for editing signal classification rules
信號規則編輯器，用於編輯信號分類規則
"""

from typing import Dict
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QSpinBox, QComboBox, QTextEdit, QCheckBox,
    QLabel, QSplitter, QGroupBox, QHeaderView
)
from PyQt5.QtCore import Qt

try:
    from ..models.signal_rule_model import SignalRuleModel
    from ..controllers.signal_rule_controller import SignalRuleController
    from ..widgets.tooltip_widget import add_tooltip, TOOLTIP_TEXTS
except ImportError:
    # Fallback for when relative imports don't work
    from models.signal_rule_model import SignalRuleModel
    from controllers.signal_rule_controller import SignalRuleController
    from widgets.tooltip_widget import add_tooltip, TOOLTIP_TEXTS


class SignalRuleEditor(QWidget):
    """
    Widget for editing signal classification rules
    信號分類規則編輯器
    """
    
    def __init__(self, signal_rules: Dict[str, SignalRuleModel], 
                 controller: SignalRuleController):
        super().__init__()
        self.signal_rules = signal_rules
        self.controller = controller
        self.current_rule = None
        
        self.init_ui()
        self.setup_connections()
        self.refresh_rules_list()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QHBoxLayout(self)
        
        # Create splitter for rules list and editor
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Rules list (left panel)
        self.create_rules_list_panel(splitter)
        
        # Rule editor (right panel)
        self.create_rule_editor_panel(splitter)
        
        # Set splitter proportions
        splitter.setSizes([400, 800])
    
    def create_rules_list_panel(self, parent):
        """Create the rules list panel"""
        rules_widget = QWidget()
        parent.addWidget(rules_widget)
        
        layout = QVBoxLayout(rules_widget)
        
        # Title
        title_label = QLabel("信號分類規則")
        title_label.setAutoFillBackground(True)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white; padding: 5px; background: #2b2b2b; border: none;")
        layout.addWidget(title_label)
        
        # Rules table
        self.rules_table = QTableWidget()
        self.rules_table.setColumnCount(4)
        self.rules_table.setHorizontalHeaderLabels(["規則名稱", "類別", "信號類型", "優先級"])
        
        # Set header styles
        header = self.rules_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setStyleSheet("QHeaderView::section { background-color: #404040; color: white; font-weight: bold; border: 1px solid #555555; padding: 4px; }")
        
        # Set vertical header (row numbers) style
        v_header = self.rules_table.verticalHeader()
        v_header.setStyleSheet("QHeaderView::section { background-color: #404040; color: white; border: 1px solid #555555; }")
        
        # Set corner button style (top-left intersection)
        self.rules_table.setStyleSheet("QTableWidget { gridline-color: #555555; } QTableWidget::corner { background-color: #404040; border: 1px solid #555555; }")
        
        self.rules_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.rules_table.itemSelectionChanged.connect(self.on_rule_selected)
        layout.addWidget(self.rules_table)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.add_rule_btn = QPushButton("新增規則")
        self.add_rule_btn.clicked.connect(self.add_new_rule)
        buttons_layout.addWidget(self.add_rule_btn)
        
        self.remove_rule_btn = QPushButton("刪除規則")
        self.remove_rule_btn.clicked.connect(self.remove_selected_rule)
        buttons_layout.addWidget(self.remove_rule_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
    
    def create_rule_editor_panel(self, parent):
        """Create the rule editor panel"""
        editor_widget = QWidget()
        parent.addWidget(editor_widget)
        
        layout = QVBoxLayout(editor_widget)
        
        # Title
        title_label = QLabel("規則編輯器")
        title_label.setAutoFillBackground(True)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white; padding: 5px; background: #2b2b2b; border: none;")
        layout.addWidget(title_label)
        
        # Basic info group
        basic_group = QGroupBox("基本資訊")
        basic_layout = QVBoxLayout(basic_group)
        
        # Rule name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("規則名稱:"))
        self.name_edit = QLineEdit()
        add_tooltip(self.name_edit, TOOLTIP_TEXTS['signal_rule_name'])
        name_layout.addWidget(self.name_edit)
        basic_layout.addLayout(name_layout)
        
        # Category and signal type
        cat_layout = QHBoxLayout()
        cat_layout.addWidget(QLabel("類別:"))
        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)
        self.category_combo.addItems([
            "Communication Interface", "High Speed Interface", 
            "RF", "Power", "Clock", "General"
        ])
        add_tooltip(self.category_combo, TOOLTIP_TEXTS['signal_category'])
        cat_layout.addWidget(self.category_combo)
        
        cat_layout.addWidget(QLabel("信號類型:"))
        self.signal_type_combo = QComboBox()
        self.signal_type_combo.setEditable(True)
        self.signal_type_combo.addItems([
            "Single-End", "Differential", "I2C", "SPI", 
            "Power", "Clock", "RF"
        ])
        add_tooltip(self.signal_type_combo, TOOLTIP_TEXTS['signal_type'])
        cat_layout.addWidget(self.signal_type_combo)
        basic_layout.addLayout(cat_layout)
        
        # Priority and enabled
        priority_layout = QHBoxLayout()
        priority_layout.addWidget(QLabel("優先級:"))
        self.priority_spin = QSpinBox()
        self.priority_spin.setRange(0, 100)
        self.priority_spin.setValue(10)
        add_tooltip(self.priority_spin, TOOLTIP_TEXTS['signal_priority'])
        priority_layout.addWidget(self.priority_spin)
        
        self.enabled_check = QCheckBox("啟用此規則")
        self.enabled_check.setChecked(True)
        priority_layout.addWidget(self.enabled_check)
        priority_layout.addStretch()
        basic_layout.addLayout(priority_layout)
        
        layout.addWidget(basic_group)
        
        # Matching criteria group
        criteria_group = QGroupBox("匹配條件")
        criteria_layout = QVBoxLayout(criteria_group)
        
        # Keywords
        criteria_layout.addWidget(QLabel("關鍵字 (用逗號分隔):"))
        self.keywords_edit = QLineEdit()
        add_tooltip(self.keywords_edit, TOOLTIP_TEXTS['signal_keywords'])
        criteria_layout.addWidget(self.keywords_edit)
        
        # Patterns
        criteria_layout.addWidget(QLabel("正則表達式模式 (每行一個):"))
        self.patterns_edit = QTextEdit()
        self.patterns_edit.setMaximumHeight(100)
        add_tooltip(self.patterns_edit, TOOLTIP_TEXTS['signal_patterns'])
        criteria_layout.addWidget(self.patterns_edit)
        
        layout.addWidget(criteria_group)
        
        # Description
        desc_group = QGroupBox("描述")
        desc_layout = QVBoxLayout(desc_group)
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        add_tooltip(self.description_edit, TOOLTIP_TEXTS['signal_description'])
        desc_layout.addWidget(self.description_edit)
        layout.addWidget(desc_group)
        
        # Save button
        save_btn = QPushButton("儲存規則")
        save_btn.clicked.connect(self.save_current_rule)
        layout.addWidget(save_btn)
        
        layout.addStretch()
    
    def setup_connections(self):
        """Setup signal connections"""
        self.controller.ruleAdded.connect(self.refresh_rules_list)
        self.controller.ruleRemoved.connect(self.refresh_rules_list)
        self.controller.ruleModified.connect(self.refresh_rules_list)
    
    def refresh_rules_list(self):
        """Refresh the rules list table"""
        self.rules_table.setRowCount(len(self.signal_rules))
        
        for row, (rule_name, rule) in enumerate(self.signal_rules.items()):
            self.rules_table.setItem(row, 0, QTableWidgetItem(rule_name))
            self.rules_table.setItem(row, 1, QTableWidgetItem(rule.category))
            self.rules_table.setItem(row, 2, QTableWidgetItem(rule.signal_type))
            self.rules_table.setItem(row, 3, QTableWidgetItem(str(rule.priority)))
    
    def on_rule_selected(self):
        """Handle rule selection"""
        current_row = self.rules_table.currentRow()
        if current_row >= 0:
            rule_name = self.rules_table.item(current_row, 0).text()
            self.load_rule_for_editing(rule_name)
    
    def load_rule_for_editing(self, rule_name: str):
        """Load a rule for editing"""
        if rule_name in self.signal_rules:
            self.current_rule = rule_name
            rule = self.signal_rules[rule_name]
            
            # Load basic info
            self.name_edit.setText(rule.name)
            self.category_combo.setCurrentText(rule.category)
            self.signal_type_combo.setCurrentText(rule.signal_type)
            self.priority_spin.setValue(rule.priority)
            self.enabled_check.setChecked(rule.enabled)
            
            # Load matching criteria
            self.keywords_edit.setText(', '.join(rule.keywords))
            self.patterns_edit.setPlainText('\\n'.join(rule.patterns))
            
            # Load description
            self.description_edit.setPlainText(rule.description)
    
    def save_current_rule(self):
        """Save the currently edited rule"""
        if not self.current_rule:
            return
        
        rule = self.signal_rules[self.current_rule]
        
        # Save basic info
        rule.set_category(self.category_combo.currentText())
        rule.set_signal_type(self.signal_type_combo.currentText())
        rule.set_priority(self.priority_spin.value())
        rule.set_enabled(self.enabled_check.isChecked())
        rule.set_description(self.description_edit.toPlainText())
        
        # Save matching criteria
        keywords = [k.strip() for k in self.keywords_edit.text().split(',') if k.strip()]
        rule.keywords = keywords
        
        patterns = [p.strip() for p in self.patterns_edit.toPlainText().split('\\n') if p.strip()]
        rule.patterns = patterns
        
        rule.dataChanged.emit()
    
    def add_new_rule(self):
        """Add a new rule"""
        from PyQt5.QtWidgets import QInputDialog
        
        rule_name, ok = QInputDialog.getText(
            self, "新增規則", "請輸入規則名稱:"
        )
        
        if ok and rule_name.strip():
            if self.controller.add_rule(rule_name.strip()):
                self.load_rule_for_editing(rule_name.strip())
    
    def remove_selected_rule(self):
        """Remove the selected rule"""
        current_row = self.rules_table.currentRow()
        if current_row >= 0:
            rule_name = self.rules_table.item(current_row, 0).text()
            
            from PyQt5.QtWidgets import QMessageBox
            reply = QMessageBox.question(
                self, "刪除規則",
                f"確定要刪除規則 '{rule_name}' 嗎？",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.controller.remove_rule(rule_name)
                if self.current_rule == rule_name:
                    self.current_rule = None