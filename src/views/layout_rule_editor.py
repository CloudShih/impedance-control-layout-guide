"""
Layout Rule Editor widget for editing layout design rules
佈局規則編輯器，用於編輯佈局設計規則
"""

from typing import Dict, Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QComboBox, QTextEdit, QLabel, QSplitter,
    QGroupBox, QHeaderView, QFormLayout, QMessageBox, QCheckBox,
    QSpinBox, QDoubleSpinBox
)
from PyQt5.QtCore import Qt, pyqtSignal
import re

try:
    from ..models.layout_rule_model import LayoutRuleModel
    from ..controllers.layout_rule_controller import LayoutRuleController
    from ..widgets.tooltip_widget import add_tooltip, TOOLTIP_TEXTS
except ImportError:
    # Fallback for when relative imports don't work
    from models.layout_rule_model import LayoutRuleModel
    from controllers.layout_rule_controller import LayoutRuleController
    from widgets.tooltip_widget import add_tooltip, TOOLTIP_TEXTS


class LayoutRuleEditor(QWidget):
    """
    Widget for editing layout design rules
    佈局設計規則編輯器
    """
    
    # Signal emitted when rules are modified
    rulesModified = pyqtSignal()
    
    def __init__(self, layout_rules: Dict[str, LayoutRuleModel], 
                 controller: LayoutRuleController):
        super().__init__()
        self.layout_rules = layout_rules
        self.controller = controller
        self.current_rule = None
        self.is_editing = False
        
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
        
        # Set splitter proportions - move slider to right (left panel wider)
        splitter.setSizes([800, 800])
    
    def create_rules_list_panel(self, parent):
        """Create the rules list panel"""
        rules_widget = QWidget()
        parent.addWidget(rules_widget)
        
        layout = QVBoxLayout(rules_widget)
        
        # Title
        title_label = QLabel("佈局設計規則")
        title_label.setAutoFillBackground(True)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white; padding: 5px; background: #2b2b2b; border: none;")
        layout.addWidget(title_label)
        
        # Rules table
        self.rules_table = QTableWidget()
        self.rules_table.setColumnCount(4)
        self.rules_table.setHorizontalHeaderLabels(["規則名稱", "阻抗", "線寬", "描述"])
        
        # Set column widths and header styles
        header = self.rules_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.resizeSection(0, 120)
        header.resizeSection(1, 100)
        header.resizeSection(2, 80)
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
        add_tooltip(self.add_rule_btn, "新增一個新的佈局設計規則")
        buttons_layout.addWidget(self.add_rule_btn)
        
        self.remove_rule_btn = QPushButton("刪除規則")
        self.remove_rule_btn.clicked.connect(self.remove_selected_rule)
        add_tooltip(self.remove_rule_btn, "刪除選中的佈局設計規則")
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
        
        # Rule name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("規則名稱:"))
        self.rule_name_edit = QLineEdit()
        self.rule_name_edit.textChanged.connect(self.on_rule_data_changed)
        add_tooltip(self.rule_name_edit, "輸入佈局規則的名稱，例如: I2C, SPI, RF")
        name_layout.addWidget(self.rule_name_edit)
        layout.addLayout(name_layout)
        
        # Enabled checkbox
        self.enabled_checkbox = QCheckBox("啟用此規則")
        self.enabled_checkbox.setChecked(True)
        self.enabled_checkbox.stateChanged.connect(self.on_rule_data_changed)
        layout.addWidget(self.enabled_checkbox)
        
        # Create grouped sections
        self.create_impedance_section(layout)
        self.create_spacing_section(layout)
        self.create_layer_section(layout)
        self.create_description_section(layout)
        
        # Save/Cancel buttons
        buttons_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("儲存")
        self.save_btn.clicked.connect(self.save_current_rule)
        self.save_btn.setEnabled(False)
        buttons_layout.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.cancel_editing)
        self.cancel_btn.setEnabled(False)
        buttons_layout.addWidget(self.cancel_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        layout.addStretch()  # Add stretch to push everything to top
    
    def create_impedance_section(self, layout):
        """Create impedance and dimensions section"""
        impedance_group = QGroupBox("阻抗與尺寸")
        impedance_layout = QFormLayout(impedance_group)
        
        # Impedance
        self.impedance_edit = QLineEdit()
        self.impedance_edit.textChanged.connect(self.on_rule_data_changed)
        add_tooltip(self.impedance_edit, "設定線路阻抗值，例如: 50 Ohm, 100 Ohm differential")
        impedance_layout.addRow("阻抗:", self.impedance_edit)
        
        # Width
        self.width_edit = QLineEdit()
        self.width_edit.textChanged.connect(self.on_rule_data_changed)
        add_tooltip(self.width_edit, "設定線路寬度，例如: 5 mil, 0.127 mm")
        impedance_layout.addRow("線寬:", self.width_edit)
        
        # Length limit
        self.length_limit_edit = QLineEdit()
        self.length_limit_edit.textChanged.connect(self.on_rule_data_changed)
        add_tooltip(self.length_limit_edit, "設定線路長度限制，例如: 6 inch, 150 mm")
        impedance_layout.addRow("長度限制:", self.length_limit_edit)
        
        # Max length (numeric)
        self.max_length_spin = QDoubleSpinBox()
        self.max_length_spin.setRange(0.0, 1000.0)
        self.max_length_spin.setSuffix(" mm")
        self.max_length_spin.valueChanged.connect(self.on_rule_data_changed)
        add_tooltip(self.max_length_spin, "最大長度數值（毫米）")
        impedance_layout.addRow("最大長度:", self.max_length_spin)
        
        # Differential impedance
        self.diff_impedance_edit = QLineEdit()
        self.diff_impedance_edit.textChanged.connect(self.on_rule_data_changed)
        add_tooltip(self.diff_impedance_edit, "差分阻抗值，例如: 100 Ohm")
        impedance_layout.addRow("差分阻抗:", self.diff_impedance_edit)
        
        layout.addWidget(impedance_group)
    
    def create_spacing_section(self, layout):
        """Create spacing and via rules section"""
        spacing_group = QGroupBox("間距與過孔")
        spacing_layout = QFormLayout(spacing_group)
        
        # Spacing
        self.spacing_edit = QLineEdit()
        self.spacing_edit.textChanged.connect(self.on_rule_data_changed)
        add_tooltip(self.spacing_edit, "線路間距規則，例如: 3W spacing, 5W minimum")
        spacing_layout.addRow("間距規則:", self.spacing_edit)
        
        # Min spacing (numeric)
        self.min_spacing_spin = QDoubleSpinBox()
        self.min_spacing_spin.setRange(0.0, 10.0)
        self.min_spacing_spin.setSuffix(" mm")
        self.min_spacing_spin.valueChanged.connect(self.on_rule_data_changed)
        add_tooltip(self.min_spacing_spin, "最小間距數值（毫米）")
        spacing_layout.addRow("最小間距:", self.min_spacing_spin)
        
        # Via rules
        self.via_rules_combo = QComboBox()
        self.via_rules_combo.addItems([
            "標準過孔規則",
            "最小化過孔",
            "避免過孔",
            "使用盲孔/埋孔",
            "允許多層過孔"
        ])
        self.via_rules_combo.setEditable(True)
        self.via_rules_combo.currentTextChanged.connect(self.on_rule_data_changed)
        add_tooltip(self.via_rules_combo, "選擇或輸入過孔使用規則")
        spacing_layout.addRow("過孔規則:", self.via_rules_combo)
        
        # Max via count
        self.max_via_spin = QSpinBox()
        self.max_via_spin.setRange(0, 100)
        self.max_via_spin.setSpecialValueText("無限制")
        self.max_via_spin.valueChanged.connect(self.on_rule_data_changed)
        add_tooltip(self.max_via_spin, "最大過孔數量限制")
        spacing_layout.addRow("最大過孔數:", self.max_via_spin)
        
        layout.addWidget(spacing_group)
    
    def create_layer_section(self, layout):
        """Create layer stack and shielding section"""
        layer_group = QGroupBox("層疊與屏蔽")
        layer_layout = QFormLayout(layer_group)
        
        # Layer stack
        self.layer_stack_combo = QComboBox()
        self.layer_stack_combo.addItems([
            "任意信號層",
            "相同層走線",
            "專用RF層",
            "頂層優先",
            "內層優先",
            "指定層疊"
        ])
        self.layer_stack_combo.setEditable(True)
        self.layer_stack_combo.currentTextChanged.connect(self.on_rule_data_changed)
        add_tooltip(self.layer_stack_combo, "選擇或輸入層疊要求")
        layer_layout.addRow("層疊要求:", self.layer_stack_combo)
        
        # Required layers
        self.required_layers_edit = QLineEdit()
        self.required_layers_edit.textChanged.connect(self.on_rule_data_changed)
        add_tooltip(self.required_layers_edit, "指定必須使用的層，用逗號分隔，例如: L1, L2, L3")
        layer_layout.addRow("必要層:", self.required_layers_edit)
        
        # Shielding
        self.shielding_combo = QComboBox()
        self.shielding_combo.addItems([
            "可選屏蔽",
            "建議接地保護",
            "必須接地屏蔽",
            "完全接地包圍",
            "差分屏蔽",
            "無屏蔽要求"
        ])
        self.shielding_combo.setEditable(True)
        self.shielding_combo.currentTextChanged.connect(self.on_rule_data_changed)
        add_tooltip(self.shielding_combo, "選擇或輸入屏蔽要求")
        layer_layout.addRow("屏蔽要求:", self.shielding_combo)
        
        layout.addWidget(layer_group)
    
    def create_description_section(self, layout):
        """Create description and notes section"""
        desc_group = QGroupBox("描述與備註")
        desc_layout = QFormLayout(desc_group)
        
        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        self.description_edit.textChanged.connect(self.on_rule_data_changed)
        add_tooltip(self.description_edit, "輸入詳細的技術描述和應用說明")
        desc_layout.addRow("技術描述:", self.description_edit)
        
        # Notes
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(60)
        self.notes_edit.textChanged.connect(self.on_rule_data_changed)
        add_tooltip(self.notes_edit, "輸入額外的設計備註和注意事項")
        desc_layout.addRow("設計備註:", self.notes_edit)
        
        layout.addWidget(desc_group)
    
    def setup_connections(self):
        """Setup signal connections"""
        # Connect controller signals
        self.controller.ruleAdded.connect(self.on_rule_added)
        self.controller.ruleRemoved.connect(self.on_rule_removed)
        self.controller.ruleModified.connect(self.on_rule_modified)
    
    def refresh_rules_list(self):
        """Refresh the rules list table"""
        self.rules_table.setRowCount(len(self.layout_rules))
        
        for row, (rule_name, rule) in enumerate(self.layout_rules.items()):
            # Rule name
            name_item = QTableWidgetItem(rule_name)
            self.rules_table.setItem(row, 0, name_item)
            
            # Impedance
            impedance_item = QTableWidgetItem(rule.impedance)
            self.rules_table.setItem(row, 1, impedance_item)
            
            # Width
            width_item = QTableWidgetItem(rule.width)
            self.rules_table.setItem(row, 2, width_item)
            
            # Description (truncated)
            desc_text = rule.description[:50] + "..." if len(rule.description) > 50 else rule.description
            desc_item = QTableWidgetItem(desc_text)
            self.rules_table.setItem(row, 3, desc_item)
        
        # Update button states
        self.update_button_states()
    
    def on_rule_selected(self):
        """Handle rule selection in the table"""
        current_row = self.rules_table.currentRow()
        if current_row >= 0:
            rule_names = list(self.layout_rules.keys())
            if current_row < len(rule_names):
                rule_name = rule_names[current_row]
                self.load_rule_to_editor(rule_name)
    
    def load_rule_to_editor(self, rule_name: str):
        """Load a rule into the editor"""
        if rule_name not in self.layout_rules:
            return
        
        rule = self.layout_rules[rule_name]
        self.current_rule = rule_name
        
        # Block signals to prevent triggering changes while loading
        self.block_editor_signals(True)
        
        try:
            # Load basic info
            self.rule_name_edit.setText(rule_name)
            self.enabled_checkbox.setChecked(rule.enabled)
            
            # Load impedance section
            self.impedance_edit.setText(rule.impedance)
            self.width_edit.setText(rule.width)
            self.length_limit_edit.setText(rule.length_limit)
            if rule.max_length_mm is not None:
                self.max_length_spin.setValue(rule.max_length_mm)
            else:
                self.max_length_spin.setValue(0.0)
            
            self.diff_impedance_edit.setText(rule.differential_impedance or "")
            
            # Load spacing section
            self.spacing_edit.setText(rule.spacing)
            if rule.min_spacing_mm is not None:
                self.min_spacing_spin.setValue(rule.min_spacing_mm)
            else:
                self.min_spacing_spin.setValue(0.0)
            
            self.via_rules_combo.setCurrentText(rule.via_rules)
            if rule.max_via_count is not None:
                self.max_via_spin.setValue(rule.max_via_count)
            else:
                self.max_via_spin.setValue(0)
            
            # Load layer section
            self.layer_stack_combo.setCurrentText(rule.layer_stack)
            self.required_layers_edit.setText(", ".join(rule.required_layers))
            self.shielding_combo.setCurrentText(rule.shielding)
            
            # Load description section
            self.description_edit.setPlainText(rule.description)
            self.notes_edit.setPlainText(rule.notes)
            
        finally:
            self.block_editor_signals(False)
        
        # Update button states
        self.is_editing = True
        self.update_button_states()
    
    def block_editor_signals(self, block: bool):
        """Block or unblock editor signals"""
        widgets = [
            self.rule_name_edit, self.enabled_checkbox, self.impedance_edit,
            self.width_edit, self.length_limit_edit, self.max_length_spin,
            self.diff_impedance_edit, self.spacing_edit, self.min_spacing_spin,
            self.via_rules_combo, self.max_via_spin, self.layer_stack_combo,
            self.required_layers_edit, self.shielding_combo, self.description_edit,
            self.notes_edit
        ]
        
        for widget in widgets:
            widget.blockSignals(block)
    
    def on_rule_data_changed(self):
        """Handle changes in rule data"""
        if self.is_editing:
            self.save_btn.setEnabled(True)
            self.cancel_btn.setEnabled(True)
    
    def add_new_rule(self):
        """Add a new rule"""
        from PyQt5.QtWidgets import QInputDialog
        
        rule_name, ok = QInputDialog.getText(
            self, "新增佈局規則", "請輸入規則名稱:"
        )
        
        if ok and rule_name.strip():
            rule_name = rule_name.strip()
            
            if rule_name in self.layout_rules:
                QMessageBox.warning(self, "重複名稱", f"規則 '{rule_name}' 已存在!")
                return
            
            # Create new rule
            success = self.controller.add_rule(rule_name)
            if success:
                self.refresh_rules_list()
                # Select the new rule
                for row in range(self.rules_table.rowCount()):
                    if self.rules_table.item(row, 0).text() == rule_name:
                        self.rules_table.selectRow(row)
                        break
            else:
                QMessageBox.warning(self, "錯誤", f"無法創建規則 '{rule_name}'")
    
    def remove_selected_rule(self):
        """Remove the selected rule"""
        current_row = self.rules_table.currentRow()
        if current_row < 0:
            QMessageBox.information(self, "提示", "請先選擇要刪除的規則")
            return
        
        rule_names = list(self.layout_rules.keys())
        if current_row >= len(rule_names):
            return
        
        rule_name = rule_names[current_row]
        
        reply = QMessageBox.question(
            self, "確認刪除", f"確定要刪除規則 '{rule_name}' 嗎？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.controller.remove_rule(rule_name)
            if success:
                self.refresh_rules_list()
                self.clear_editor()
            else:
                QMessageBox.warning(self, "錯誤", f"無法刪除規則 '{rule_name}'")
    
    def save_current_rule(self):
        """Save the current rule"""
        if not self.current_rule:
            return
        
        if not self.validate_rule_data():
            return
        
        rule = self.layout_rules[self.current_rule]
        new_name = self.rule_name_edit.text().strip()
        
        # Check if name changed and new name exists
        if new_name != self.current_rule and new_name in self.layout_rules:
            QMessageBox.warning(self, "重複名稱", f"規則名稱 '{new_name}' 已存在!")
            return
        
        # Update rule data
        self.update_rule_from_editor(rule)
        
        # Handle name change
        if new_name != self.current_rule:
            # Remove old rule and add with new name
            old_rule_data = rule.to_dict()
            del self.layout_rules[self.current_rule]
            rule.name = new_name
            self.layout_rules[new_name] = rule
            self.current_rule = new_name
        
        # Refresh display
        self.refresh_rules_list()
        self.is_editing = False
        self.save_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        
        # Emit modification signal
        self.rulesModified.emit()
        
        QMessageBox.information(self, "成功", f"規則 '{new_name}' 已儲存")
    
    def update_rule_from_editor(self, rule: LayoutRuleModel):
        """Update rule object from editor fields"""
        rule.enabled = self.enabled_checkbox.isChecked()
        rule.impedance = self.impedance_edit.text().strip()
        rule.width = self.width_edit.text().strip()
        rule.length_limit = self.length_limit_edit.text().strip()
        
        # Handle numeric fields
        if self.max_length_spin.value() > 0:
            rule.max_length_mm = self.max_length_spin.value()
        else:
            rule.max_length_mm = None
        
        diff_imp = self.diff_impedance_edit.text().strip()
        rule.differential_impedance = diff_imp if diff_imp else None
        
        rule.spacing = self.spacing_edit.text().strip()
        
        if self.min_spacing_spin.value() > 0:
            rule.min_spacing_mm = self.min_spacing_spin.value()
        else:
            rule.min_spacing_mm = None
        
        rule.via_rules = self.via_rules_combo.currentText()
        
        if self.max_via_spin.value() > 0:
            rule.max_via_count = self.max_via_spin.value()
        else:
            rule.max_via_count = None
        
        rule.layer_stack = self.layer_stack_combo.currentText()
        
        # Handle required layers
        layers_text = self.required_layers_edit.text().strip()
        if layers_text:
            rule.required_layers = [layer.strip() for layer in layers_text.split(",")]
        else:
            rule.required_layers = []
        
        rule.shielding = self.shielding_combo.currentText()
        rule.description = self.description_edit.toPlainText().strip()
        rule.notes = self.notes_edit.toPlainText().strip()
    
    def validate_rule_data(self) -> bool:
        """Validate the current rule data"""
        # Check required fields
        if not self.rule_name_edit.text().strip():
            QMessageBox.warning(self, "驗證錯誤", "規則名稱不能為空")
            self.rule_name_edit.setFocus()
            return False
        
        if not self.impedance_edit.text().strip():
            QMessageBox.warning(self, "驗證錯誤", "阻抗值不能為空")
            self.impedance_edit.setFocus()
            return False
        
        # Validate impedance format
        impedance_text = self.impedance_edit.text().strip()
        if not re.match(r'^[\d.]+\s*(Ohm|ohm|Ω)(\s+differential)?$', impedance_text):
            QMessageBox.warning(self, "驗證錯誤", 
                              "阻抗格式不正確\n正確格式: '50 Ohm' 或 '100 Ohm differential'")
            self.impedance_edit.setFocus()
            return False
        
        return True
    
    def cancel_editing(self):
        """Cancel current editing"""
        if self.current_rule:
            self.load_rule_to_editor(self.current_rule)
        else:
            self.clear_editor()
        
        self.is_editing = False
        self.save_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
    
    def clear_editor(self):
        """Clear the editor fields"""
        self.block_editor_signals(True)
        
        try:
            self.rule_name_edit.clear()
            self.enabled_checkbox.setChecked(True)
            self.impedance_edit.clear()
            self.width_edit.clear()
            self.length_limit_edit.clear()
            self.max_length_spin.setValue(0.0)
            self.diff_impedance_edit.clear()
            self.spacing_edit.clear()
            self.min_spacing_spin.setValue(0.0)
            self.via_rules_combo.setCurrentIndex(0)
            self.max_via_spin.setValue(0)
            self.layer_stack_combo.setCurrentIndex(0)
            self.required_layers_edit.clear()
            self.shielding_combo.setCurrentIndex(0)
            self.description_edit.clear()
            self.notes_edit.clear()
        finally:
            self.block_editor_signals(False)
        
        self.current_rule = None
        self.is_editing = False
        self.update_button_states()
    
    def update_button_states(self):
        """Update button enabled states"""
        has_selection = self.rules_table.currentRow() >= 0
        self.remove_rule_btn.setEnabled(has_selection)
    
    def on_rule_added(self, rule_name: str):
        """Handle rule added signal from controller"""
        self.refresh_rules_list()
    
    def on_rule_removed(self, rule_name: str):
        """Handle rule removed signal from controller"""
        self.refresh_rules_list()
        if self.current_rule == rule_name:
            self.clear_editor()
    
    def on_rule_modified(self, rule_name: str):
        """Handle rule modified signal from controller"""
        self.refresh_rules_list()