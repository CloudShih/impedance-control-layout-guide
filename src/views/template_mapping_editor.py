"""
Template Mapping Editor widget for managing Excel output templates
模板映射編輯器，用於管理Excel輸出模板
"""

from typing import Dict, List, Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QTableWidget, 
    QTableWidgetItem, QPushButton, QLineEdit, QCheckBox, QTextEdit,
    QLabel, QGroupBox, QFormLayout, QMessageBox, QHeaderView,
    QInputDialog, QFileDialog, QComboBox, QSplitter
)
from PyQt5.QtCore import Qt, pyqtSignal, QAbstractTableModel, QModelIndex
import json
from pathlib import Path

# Use absolute imports for PyInstaller compatibility
from models.template_mapping_model import TemplateMappingModel
from controllers.template_mapping_controller import TemplateMappingController
from widgets.tooltip_widget import add_tooltip, TOOLTIP_TEXTS


class ColumnMappingTableModel(QAbstractTableModel):
    """Custom table model for column mappings"""
    
    def __init__(self, template_mapping: TemplateMappingModel):
        super().__init__()
        self.template_mapping = template_mapping
        self.headers = ["內部名稱", "顯示名稱", "可見", "順序"]
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.template_mapping.columns)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        row = index.row()
        col = index.column()
        
        if row >= len(self.template_mapping.columns):
            return None
        
        internal_names = list(self.template_mapping.columns.keys())
        internal_name = internal_names[row]
        
        if role == Qt.DisplayRole:
            if col == 0:  # Internal name
                return internal_name
            elif col == 1:  # Display name
                return self.template_mapping.columns[internal_name]
            elif col == 2:  # Visible
                return "是" if internal_name not in self.template_mapping.hidden_columns else "否"
            elif col == 3:  # Order
                try:
                    return str(self.template_mapping.column_order.index(internal_name) + 1)
                except ValueError:
                    return "未設定"
        
        elif role == Qt.CheckStateRole and col == 2:
            return Qt.Checked if internal_name not in self.template_mapping.hidden_columns else Qt.Unchecked
        
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None
    
    def flags(self, index):
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() == 1:  # Display name is editable
            flags |= Qt.ItemIsEditable
        elif index.column() == 2:  # Visible is checkable
            flags |= Qt.ItemIsUserCheckable
        return flags
    
    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False
        
        row = index.row()
        col = index.column()
        
        internal_names = list(self.template_mapping.columns.keys())
        internal_name = internal_names[row]
        
        if role == Qt.EditRole and col == 1:  # Display name
            self.template_mapping.update_column_display_name(internal_name, str(value))
            self.dataChanged.emit(index, index)
            return True
        elif role == Qt.CheckStateRole and col == 2:  # Visible
            self.template_mapping.set_column_visibility(internal_name, value == Qt.Checked)
            self.dataChanged.emit(index, index)
            return True
        
        return False
    
    def refresh(self):
        """Refresh the model data"""
        self.beginResetModel()
        self.endResetModel()


class TemplateMappingEditor(QWidget):
    """
    Widget for editing template mapping configurations
    模板映射配置編輯器
    """
    
    # Signal emitted when template is modified
    templateModified = pyqtSignal()
    
    def __init__(self, template_mapping: TemplateMappingModel, 
                 controller: TemplateMappingController):
        super().__init__()
        self.template_mapping = template_mapping
        self.controller = controller
        
        self.init_ui()
        self.setup_connections()
        self.load_template_data()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_mapping_tab()
        self.create_output_settings_tab()
        self.create_preview_tab()
        
        # Action buttons
        self.create_action_buttons(layout)
    
    def create_mapping_tab(self):
        """Create the column mapping tab"""
        mapping_widget = QWidget()
        self.tab_widget.addTab(mapping_widget, "欄位映射")
        
        layout = QVBoxLayout(mapping_widget)
        
        # Title
        title_label = QLabel("Excel輸出欄位映射設定")
        title_label.setAutoFillBackground(True)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white; padding: 5px; background: #2b2b2b; border: none;")
        layout.addWidget(title_label)
        
        # Column mapping table
        self.create_column_mapping_section(layout)
        
        # Column management buttons
        self.create_column_buttons(layout)
    
    def create_column_mapping_section(self, layout):
        """Create the column mapping table section"""
        # Create table
        self.column_table = QTableWidget()
        self.column_table.setColumnCount(4)
        self.column_table.setHorizontalHeaderLabels(["內部名稱", "顯示名稱", "可見", "順序"])
        
        # Set column widths and header styles
        header = self.column_table.horizontalHeader()
        header.resizeSection(0, 150)
        header.resizeSection(1, 200)
        header.resizeSection(2, 80)
        header.resizeSection(3, 80)
        header.setStretchLastSection(False)
        header.setStyleSheet("QHeaderView::section { background-color: #404040; color: white; font-weight: bold; border: 1px solid #555555; padding: 4px; }")
        
        # Set vertical header (row numbers) style
        v_header = self.column_table.verticalHeader()
        v_header.setStyleSheet("QHeaderView::section { background-color: #404040; color: white; border: 1px solid #555555; }")
        
        # Set corner button style (top-left intersection)
        self.column_table.setStyleSheet("QTableWidget { gridline-color: #555555; } QTableWidget::corner { background-color: #404040; border: 1px solid #555555; }")
        
        self.column_table.setSelectionBehavior(QTableWidget.SelectRows)
        add_tooltip(self.column_table, "管理Excel輸出的欄位映射關係")
        
        layout.addWidget(self.column_table)
    
    def create_column_buttons(self, layout):
        """Create column management buttons"""
        buttons_layout = QHBoxLayout()
        
        # Add column button
        self.add_column_btn = QPushButton("新增欄位")
        self.add_column_btn.clicked.connect(self.add_new_column)
        add_tooltip(self.add_column_btn, "新增一個新的輸出欄位")
        buttons_layout.addWidget(self.add_column_btn)
        
        # Remove column button
        self.remove_column_btn = QPushButton("刪除欄位")
        self.remove_column_btn.clicked.connect(self.remove_selected_column)
        add_tooltip(self.remove_column_btn, "刪除選中的輸出欄位")
        buttons_layout.addWidget(self.remove_column_btn)
        
        # Move up button
        self.move_up_btn = QPushButton("上移")
        self.move_up_btn.clicked.connect(self.move_column_up)
        add_tooltip(self.move_up_btn, "將選中欄位向上移動")
        buttons_layout.addWidget(self.move_up_btn)
        
        # Move down button
        self.move_down_btn = QPushButton("下移")
        self.move_down_btn.clicked.connect(self.move_column_down)
        add_tooltip(self.move_down_btn, "將選中欄位向下移動")
        buttons_layout.addWidget(self.move_down_btn)
        
        # Reset to defaults button
        self.reset_btn = QPushButton("重設為預設")
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        add_tooltip(self.reset_btn, "重設所有欄位映射為預設值")
        buttons_layout.addWidget(self.reset_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
    
    def create_output_settings_tab(self):
        """Create the output settings tab"""
        settings_widget = QWidget()
        self.tab_widget.addTab(settings_widget, "輸出設定")
        
        layout = QVBoxLayout(settings_widget)
        
        # Title
        title_label = QLabel("Excel輸出格式設定")
        title_label.setAutoFillBackground(True)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white; padding: 5px; background: #2b2b2b; border: none;")
        layout.addWidget(title_label)
        
        # Create settings groups
        self.create_excel_settings_group(layout)
        self.create_formatting_settings_group(layout)
        
        layout.addStretch()
    
    def create_excel_settings_group(self, layout):
        """Create Excel basic settings group"""
        excel_group = QGroupBox("Excel基本設定")
        excel_layout = QFormLayout(excel_group)
        
        # Sheet name
        self.sheet_name_edit = QLineEdit()
        self.sheet_name_edit.textChanged.connect(self.on_settings_changed)
        add_tooltip(self.sheet_name_edit, "設定Excel工作表名稱")
        excel_layout.addRow("工作表名稱:", self.sheet_name_edit)
        
        # Auto filter
        self.auto_filter_checkbox = QCheckBox("啟用自動篩選")
        self.auto_filter_checkbox.stateChanged.connect(self.on_settings_changed)
        add_tooltip(self.auto_filter_checkbox, "在Excel中啟用自動篩選功能")
        excel_layout.addRow("", self.auto_filter_checkbox)
        
        # Freeze panes
        self.freeze_panes_combo = QComboBox()
        self.freeze_panes_combo.addItems(["無", "A2", "B2", "A3", "B3"])
        self.freeze_panes_combo.setEditable(True)
        self.freeze_panes_combo.currentTextChanged.connect(self.on_settings_changed)
        add_tooltip(self.freeze_panes_combo, "設定凍結窗格位置，例如A2")
        excel_layout.addRow("凍結窗格:", self.freeze_panes_combo)
        
        layout.addWidget(excel_group)
    
    def create_formatting_settings_group(self, layout):
        """Create formatting settings group"""
        format_group = QGroupBox("格式設定")
        format_layout = QFormLayout(format_group)
        
        # Column width auto
        self.column_width_auto_checkbox = QCheckBox("自動調整欄寬")
        self.column_width_auto_checkbox.stateChanged.connect(self.on_settings_changed)
        add_tooltip(self.column_width_auto_checkbox, "自動根據內容調整欄位寬度")
        format_layout.addRow("", self.column_width_auto_checkbox)
        
        # Header formatting
        self.header_formatting_checkbox = QCheckBox("標題格式化")
        self.header_formatting_checkbox.stateChanged.connect(self.on_settings_changed)
        add_tooltip(self.header_formatting_checkbox, "對標題列套用特殊格式")
        format_layout.addRow("", self.header_formatting_checkbox)
        
        layout.addWidget(format_group)
    
    def create_preview_tab(self):
        """Create the preview tab"""
        preview_widget = QWidget()
        self.tab_widget.addTab(preview_widget, "預覽")
        
        layout = QVBoxLayout(preview_widget)
        
        # Title
        title_label = QLabel("模板預覽")
        title_label.setAutoFillBackground(True)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white; padding: 5px; background: #2b2b2b; border: none;")
        layout.addWidget(title_label)
        
        # Refresh button
        refresh_layout = QHBoxLayout()
        self.refresh_preview_btn = QPushButton("刷新預覽")
        self.refresh_preview_btn.clicked.connect(self.refresh_preview)
        add_tooltip(self.refresh_preview_btn, "刷新模板預覽")
        refresh_layout.addWidget(self.refresh_preview_btn)
        refresh_layout.addStretch()
        layout.addLayout(refresh_layout)
        
        # Preview table
        self.preview_table = QTableWidget()
        self.preview_table.setAlternatingRowColors(True)
        add_tooltip(self.preview_table, "顯示Excel輸出的預覽效果")
        layout.addWidget(self.preview_table)
    
    def create_action_buttons(self, layout):
        """Create main action buttons"""
        buttons_layout = QHBoxLayout()
        
        # Import template button
        self.import_btn = QPushButton("匯入模板")
        self.import_btn.clicked.connect(self.import_template)
        add_tooltip(self.import_btn, "從文件匯入模板配置")
        buttons_layout.addWidget(self.import_btn)
        
        # Export template button
        self.export_btn = QPushButton("匯出模板")
        self.export_btn.clicked.connect(self.export_template)
        add_tooltip(self.export_btn, "將模板配置匯出到文件")
        buttons_layout.addWidget(self.export_btn)
        
        buttons_layout.addStretch()
        
        # Apply button
        self.apply_btn = QPushButton("套用變更")
        self.apply_btn.clicked.connect(self.apply_changes)
        self.apply_btn.setEnabled(False)
        add_tooltip(self.apply_btn, "套用所有變更並更新預覽")
        buttons_layout.addWidget(self.apply_btn)
        
        layout.addLayout(buttons_layout)
    
    def setup_connections(self):
        """Setup signal connections"""
        # Connect controller signals
        self.controller.templateModified.connect(self.on_template_modified)
        self.controller.columnAdded.connect(self.on_column_added)
        self.controller.columnRemoved.connect(self.on_column_removed)
        self.controller.columnReordered.connect(self.on_column_reordered)
        
        # Connect table selection changes
        self.column_table.itemSelectionChanged.connect(self.on_column_selection_changed)
        self.column_table.itemChanged.connect(self.on_table_item_changed)
    
    def load_template_data(self):
        """Load template data into the UI"""
        self.refresh_column_table()
        self.load_output_settings()
        self.refresh_preview()
    
    def refresh_column_table(self):
        """Refresh the column mapping table"""
        # Block signals to prevent recursion during refresh
        self.column_table.blockSignals(True)
        
        try:
            self.column_table.setRowCount(len(self.template_mapping.columns))
            
            row = 0
            for internal_name in self.template_mapping.column_order:
                if internal_name not in self.template_mapping.columns:
                    continue
                    
                # Internal name (read-only)
                internal_item = QTableWidgetItem(internal_name)
                internal_item.setFlags(internal_item.flags() & ~Qt.ItemIsEditable)
                self.column_table.setItem(row, 0, internal_item)
                
                # Display name (editable)
                display_item = QTableWidgetItem(self.template_mapping.columns[internal_name])
                self.column_table.setItem(row, 1, display_item)
                
                # Visible checkbox
                visible_item = QTableWidgetItem()
                visible_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                visible_item.setCheckState(
                    Qt.Checked if internal_name not in self.template_mapping.hidden_columns 
                    else Qt.Unchecked
                )
                self.column_table.setItem(row, 2, visible_item)
                
                # Order (read-only)
                order_item = QTableWidgetItem(str(row + 1))
                order_item.setFlags(order_item.flags() & ~Qt.ItemIsEditable)
                self.column_table.setItem(row, 3, order_item)
                
                row += 1
        finally:
            # Always unblock signals
            self.column_table.blockSignals(False)
        
        self.update_button_states()
    
    def load_output_settings(self):
        """Load output settings into the UI"""
        settings = self.template_mapping.output_settings
        
        self.sheet_name_edit.setText(settings.get('sheet_name', 'Layout Guide'))
        self.auto_filter_checkbox.setChecked(settings.get('auto_filter', True))
        
        freeze_panes = settings.get('freeze_panes', 'A2')
        if freeze_panes == '':
            freeze_panes = '無'
        self.freeze_panes_combo.setCurrentText(freeze_panes)
        
        self.column_width_auto_checkbox.setChecked(settings.get('column_width_auto', True))
        self.header_formatting_checkbox.setChecked(settings.get('header_formatting', True))
    
    def on_column_selection_changed(self):
        """Handle column selection changes"""
        self.update_button_states()
    
    def on_table_item_changed(self, item):
        """Handle table item changes"""
        # Block signals to prevent recursion
        self.column_table.blockSignals(True)
        
        try:
            if item.column() == 1:  # Display name changed
                row = item.row()
                internal_name = self.column_table.item(row, 0).text()
                new_display_name = item.text()
                
                # Update the model
                self.template_mapping.update_column_display_name(internal_name, new_display_name)
                self.apply_btn.setEnabled(True)
                
            elif item.column() == 2:  # Visibility changed
                row = item.row()
                internal_name = self.column_table.item(row, 0).text()
                is_visible = item.checkState() == Qt.Checked
                
                # Update the model
                self.template_mapping.set_column_visibility(internal_name, is_visible)
                self.apply_btn.setEnabled(True)
        finally:
            # Always unblock signals
            self.column_table.blockSignals(False)
    
    def add_new_column(self):
        """Add a new column mapping"""
        dialog = AddColumnDialog(self)
        if dialog.exec_() == dialog.Accepted:
            internal_name = dialog.internal_name_edit.text().strip()
            display_name = dialog.display_name_edit.text().strip()
            
            if not internal_name or not display_name:
                QMessageBox.warning(self, "錯誤", "內部名稱和顯示名稱都不能為空")
                return
            
            if internal_name in self.template_mapping.columns:
                QMessageBox.warning(self, "錯誤", f"內部名稱 '{internal_name}' 已存在")
                return
            
            # Add to model
            success = self.controller.add_column(internal_name, display_name)
            if success:
                self.refresh_column_table()
                self.apply_btn.setEnabled(True)
            else:
                QMessageBox.warning(self, "錯誤", "無法新增欄位")
    
    def remove_selected_column(self):
        """Remove the selected column"""
        current_row = self.column_table.currentRow()
        if current_row < 0:
            QMessageBox.information(self, "提示", "請先選擇要刪除的欄位")
            return
        
        internal_name = self.column_table.item(current_row, 0).text()
        
        reply = QMessageBox.question(
            self, "確認刪除", f"確定要刪除欄位 '{internal_name}' 嗎？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.controller.remove_column(internal_name)
            if success:
                self.refresh_column_table()
                self.apply_btn.setEnabled(True)
            else:
                QMessageBox.warning(self, "錯誤", "無法刪除欄位")
    
    def move_column_up(self):
        """Move selected column up"""
        current_row = self.column_table.currentRow()
        if current_row <= 0:
            return
        
        # Get column order
        column_order = self.template_mapping.column_order.copy()
        
        # Swap positions
        column_order[current_row], column_order[current_row - 1] = \
            column_order[current_row - 1], column_order[current_row]
        
        # Update model
        self.template_mapping.reorder_columns(column_order)
        self.refresh_column_table()
        
        # Select the moved row
        self.column_table.selectRow(current_row - 1)
        self.apply_btn.setEnabled(True)
    
    def move_column_down(self):
        """Move selected column down"""
        current_row = self.column_table.currentRow()
        if current_row < 0 or current_row >= self.column_table.rowCount() - 1:
            return
        
        # Get column order
        column_order = self.template_mapping.column_order.copy()
        
        # Swap positions
        column_order[current_row], column_order[current_row + 1] = \
            column_order[current_row + 1], column_order[current_row]
        
        # Update model
        self.template_mapping.reorder_columns(column_order)
        self.refresh_column_table()
        
        # Select the moved row
        self.column_table.selectRow(current_row + 1)
        self.apply_btn.setEnabled(True)
    
    def reset_to_defaults(self):
        """Reset template to default values"""
        reply = QMessageBox.question(
            self, "確認重設", "確定要重設為預設模板嗎？所有自定義設定將被清除。",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.template_mapping.reset_to_defaults()
            self.load_template_data()
            self.apply_btn.setEnabled(True)
    
    def on_settings_changed(self):
        """Handle output settings changes"""
        # Update output settings in model
        settings = self.template_mapping.output_settings
        
        settings['sheet_name'] = self.sheet_name_edit.text()
        settings['auto_filter'] = self.auto_filter_checkbox.isChecked()
        
        freeze_panes = self.freeze_panes_combo.currentText()
        if freeze_panes == '無':
            freeze_panes = ''
        settings['freeze_panes'] = freeze_panes
        
        settings['column_width_auto'] = self.column_width_auto_checkbox.isChecked()
        settings['header_formatting'] = self.header_formatting_checkbox.isChecked()
        
        self.apply_btn.setEnabled(True)
    
    def refresh_preview(self):
        """Refresh the preview table"""
        # Create sample data for preview
        sample_data = self.create_sample_data()
        
        # Get visible columns in order
        visible_columns = [
            col for col in self.template_mapping.column_order 
            if col not in self.template_mapping.hidden_columns
        ]
        
        # Set up preview table
        self.preview_table.setColumnCount(len(visible_columns))
        self.preview_table.setRowCount(len(sample_data))
        
        # Set headers
        headers = [self.template_mapping.columns.get(col, col) for col in visible_columns]
        self.preview_table.setHorizontalHeaderLabels(headers)
        
        # Fill sample data
        for row, data_row in enumerate(sample_data):
            for col, column_key in enumerate(visible_columns):
                value = data_row.get(column_key, "")
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Read-only
                self.preview_table.setItem(row, col, item)
        
        # Set preview table header styles
        preview_header = self.preview_table.horizontalHeader()
        preview_header.setStyleSheet("QHeaderView::section { background-color: #404040; color: white; font-weight: bold; border: 1px solid #555555; padding: 4px; }")
        
        preview_v_header = self.preview_table.verticalHeader()
        preview_v_header.setStyleSheet("QHeaderView::section { background-color: #404040; color: white; border: 1px solid #555555; }")
        
        # Set preview table corner button style
        self.preview_table.setStyleSheet("QTableWidget { gridline-color: #555555; } QTableWidget::corner { background-color: #404040; border: 1px solid #555555; }")
        
        # Auto-resize columns
        self.preview_table.resizeColumnsToContents()
    
    def create_sample_data(self):
        """Create sample data for preview"""
        return [
            {
                'Category': 'High Speed',
                'Net_Name': 'USB_DP',
                'Pin': 'A1, A2',
                'Description': 'USB Differential Pair Data+',
                'Impedance': '90 Ohm differential',
                'Type': 'Differential',
                'Width': '5 mil',
                'Length_Limit': '6 inch',
                'Spacing': '3W spacing',
                'Shielding': 'Ground guard required',
                'Layer_Stack': 'Same layer',
                'Notes': 'Length matching required'
            },
            {
                'Category': 'Control',
                'Net_Name': 'I2C_SCL',
                'Pin': 'B3',
                'Description': 'I2C Clock Signal',
                'Impedance': '50 Ohm',
                'Type': 'Single-ended',
                'Width': '5 mil',
                'Length_Limit': '6 inch',
                'Spacing': '3W spacing',
                'Shielding': 'Ground guard preferred',
                'Layer_Stack': 'Any signal layer',
                'Notes': 'Pull-up resistor required'
            },
            {
                'Category': 'Power',
                'Net_Name': 'VCC_3V3',
                'Pin': 'C1, C2, C3',
                'Description': '3.3V Power Supply',
                'Impedance': 'N/A',
                'Type': 'Power',
                'Width': '10 mil',
                'Length_Limit': 'No limit',
                'Spacing': '5 mil minimum',
                'Shielding': 'Optional',
                'Layer_Stack': 'Power layers preferred',
                'Notes': 'Wide traces for current capacity'
            }
        ]
    
    def import_template(self):
        """Import template configuration from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "匯入模板配置", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            self.template_mapping.load_from_dict(template_data)
            self.load_template_data()
            self.apply_btn.setEnabled(True)
            
            QMessageBox.information(self, "成功", f"模板配置已從 {file_path} 匯入")
            
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"匯入模板配置失敗:\n{str(e)}")
    
    def export_template(self):
        """Export template configuration to file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "匯出模板配置", "template_config.json", "JSON Files (*.json);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            template_data = self.template_mapping.to_dict()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False, indent=2)
            
            QMessageBox.information(self, "成功", f"模板配置已匯出到 {file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"匯出模板配置失敗:\n{str(e)}")
    
    def apply_changes(self):
        """Apply all changes and refresh preview"""
        self.refresh_preview()
        self.apply_btn.setEnabled(False)
        self.templateModified.emit()
        
        QMessageBox.information(self, "成功", "所有變更已套用")
    
    def update_button_states(self):
        """Update button enabled states"""
        has_selection = self.column_table.currentRow() >= 0
        row_count = self.column_table.rowCount()
        current_row = self.column_table.currentRow()
        
        self.remove_column_btn.setEnabled(has_selection)
        self.move_up_btn.setEnabled(has_selection and current_row > 0)
        self.move_down_btn.setEnabled(has_selection and current_row < row_count - 1)
    
    def on_template_modified(self):
        """Handle template modified signal from controller"""
        self.refresh_column_table()
        self.refresh_preview()
    
    def on_column_added(self, column_name: str):
        """Handle column added signal from controller"""
        self.refresh_column_table()
    
    def on_column_removed(self, column_name: str):
        """Handle column removed signal from controller"""
        self.refresh_column_table()
    
    def on_column_reordered(self):
        """Handle column reordered signal from controller"""
        self.refresh_column_table()


class AddColumnDialog(QMessageBox):
    """Dialog for adding new columns"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("新增欄位")
        self.setIcon(QMessageBox.Question)
        self.setText("請輸入新欄位的資訊:")
        
        # Create input fields
        self.internal_name_edit = QLineEdit()
        self.internal_name_edit.setPlaceholderText("內部名稱 (例如: Custom_Field)")
        
        self.display_name_edit = QLineEdit()
        self.display_name_edit.setPlaceholderText("顯示名稱 (例如: 自定義欄位)")
        
        # Create layout
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        form_layout.addRow("內部名稱:", self.internal_name_edit)
        form_layout.addRow("顯示名稱:", self.display_name_edit)
        
        layout.addLayout(form_layout)
        
        # Add to message box
        widget = QWidget()
        widget.setLayout(layout)
        self.layout().addWidget(widget, 1, 0, 1, self.layout().columnCount())
        
        # Add buttons
        self.addButton("確定", QMessageBox.AcceptRole)
        self.addButton("取消", QMessageBox.RejectRole)