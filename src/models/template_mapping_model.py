"""
Template Mapping Model for managing Excel output template
模板映射模型，用於管理Excel輸出模板
"""

from typing import Dict, Any, List
from PyQt5.QtCore import QObject, pyqtSignal


class TemplateMappingModel(QObject):
    """
    Model for managing template column mappings and output settings
    管理模板欄位映射和輸出設定的模型
    """
    
    # Signals for notifying changes
    dataChanged = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.columns: Dict[str, str] = {}
        self.output_settings: Dict[str, Any] = {}
        self.custom_headers: Dict[str, str] = {}
        self.column_order: List[str] = []
        self.hidden_columns: List[str] = []
        
        # Default settings
        self._set_defaults()
    
    def _set_defaults(self):
        """Set default template mapping values"""
        self.columns = {
            'Category': 'Category',
            'Net_Name': 'Net Name',
            'Pin': 'Pin (MT7921)',
            'Description': 'Description',
            'Impedance': 'Impedance',
            'Type': 'Type',
            'Width': 'Width',
            'Length_Limit': 'Length Limit (mil)',
            'Spacing': 'Spacing',
            'Shielding': 'Shielding',
            'Layer_Stack': 'Layer Stack',
            'Notes': 'Notes'
        }
        
        self.output_settings = {
            'sheet_name': 'Layout Guide',
            'auto_filter': True,
            'freeze_panes': 'A2',
            'column_width_auto': True,
            'header_formatting': True
        }
        
        self.column_order = list(self.columns.keys())
    
    def load_from_dict(self, data: Dict[str, Any]):
        """Load template mapping from dictionary data"""
        self.columns = data.get('columns', {})
        self.output_settings = data.get('output_settings', {})
        self.custom_headers = data.get('custom_headers', {})
        self.column_order = data.get('column_order', list(self.columns.keys()))
        self.hidden_columns = data.get('hidden_columns', [])
        
        self.dataChanged.emit()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template mapping to dictionary"""
        return {
            'columns': self.columns,
            'output_settings': self.output_settings,
            'custom_headers': self.custom_headers,
            'column_order': self.column_order,
            'hidden_columns': self.hidden_columns
        }
    
    def add_column(self, internal_name: str, display_name: str):
        """Add a new column mapping"""
        if internal_name and display_name:
            self.columns[internal_name] = display_name
            if internal_name not in self.column_order:
                self.column_order.append(internal_name)
            self.dataChanged.emit()
    
    def remove_column(self, internal_name: str):
        """Remove a column mapping"""
        if internal_name in self.columns:
            del self.columns[internal_name]
            if internal_name in self.column_order:
                self.column_order.remove(internal_name)
            if internal_name in self.hidden_columns:
                self.hidden_columns.remove(internal_name)
            if internal_name in self.custom_headers:
                del self.custom_headers[internal_name]
            self.dataChanged.emit()
    
    def update_column_display_name(self, internal_name: str, display_name: str):
        """Update the display name for a column"""
        if internal_name in self.columns:
            self.columns[internal_name] = display_name
            self.dataChanged.emit()
    
    def update_column_order(self, new_order: List[str]):
        """Update the column order"""
        # Validate that all columns in new_order exist
        valid_order = [col for col in new_order if col in self.columns]
        
        # Add any missing columns to the end
        for col in self.columns:
            if col not in valid_order:
                valid_order.append(col)
        
        self.column_order = valid_order
        self.dataChanged.emit()
    
    def move_column_up(self, internal_name: str):
        """Move a column up in the order"""
        if internal_name in self.column_order:
            current_index = self.column_order.index(internal_name)
            if current_index > 0:
                self.column_order[current_index], self.column_order[current_index - 1] = \
                    self.column_order[current_index - 1], self.column_order[current_index]
                self.dataChanged.emit()
    
    def move_column_down(self, internal_name: str):
        """Move a column down in the order"""
        if internal_name in self.column_order:
            current_index = self.column_order.index(internal_name)
            if current_index < len(self.column_order) - 1:
                self.column_order[current_index], self.column_order[current_index + 1] = \
                    self.column_order[current_index + 1], self.column_order[current_index]
                self.dataChanged.emit()
    
    def hide_column(self, internal_name: str):
        """Hide a column from output"""
        if internal_name in self.columns and internal_name not in self.hidden_columns:
            self.hidden_columns.append(internal_name)
            self.dataChanged.emit()
    
    def show_column(self, internal_name: str):
        """Show a previously hidden column"""
        if internal_name in self.hidden_columns:
            self.hidden_columns.remove(internal_name)
            self.dataChanged.emit()
    
    def set_custom_header(self, internal_name: str, custom_header: str):
        """Set a custom header for a column"""
        if internal_name in self.columns:
            if custom_header.strip():
                self.custom_headers[internal_name] = custom_header
            elif internal_name in self.custom_headers:
                del self.custom_headers[internal_name]
            self.dataChanged.emit()
    
    def get_display_header(self, internal_name: str) -> str:
        """Get the display header for a column (custom or default)"""
        if internal_name in self.custom_headers:
            return self.custom_headers[internal_name]
        return self.columns.get(internal_name, internal_name)
    
    def set_output_setting(self, key: str, value: Any):
        """Set an output setting"""
        if self.output_settings.get(key) != value:
            self.output_settings[key] = value
            self.dataChanged.emit()
    
    def get_output_setting(self, key: str, default: Any = None) -> Any:
        """Get an output setting"""
        return self.output_settings.get(key, default)
    
    def get_visible_columns(self) -> List[str]:
        """Get list of visible columns in order"""
        return [col for col in self.column_order if col not in self.hidden_columns]
    
    def get_visible_headers(self) -> List[str]:
        """Get list of visible column headers in order"""
        return [self.get_display_header(col) for col in self.get_visible_columns()]
    
    def validate(self) -> List[str]:
        """Validate the template mapping and return list of errors"""
        errors = []
        
        if not self.columns:
            errors.append("At least one column mapping must be defined")
        
        # Check for empty display names
        for internal_name, display_name in self.columns.items():
            if not display_name.strip():
                errors.append(f"Column '{internal_name}' has empty display name")
        
        # Check for duplicate display names
        display_names = list(self.columns.values())
        if len(display_names) != len(set(display_names)):
            duplicates = []
            seen = set()
            for name in display_names:
                if name in seen and name not in duplicates:
                    duplicates.append(name)
                seen.add(name)
            errors.append(f"Duplicate display names found: {', '.join(duplicates)}")
        
        # Validate output settings
        sheet_name = self.output_settings.get('sheet_name', '')
        if not sheet_name.strip():
            errors.append("Sheet name cannot be empty")
        
        # Check for invalid characters in sheet name
        invalid_chars = [':', '*', '?', '/', '\\', '[', ']']
        for char in invalid_chars:
            if char in sheet_name:
                errors.append(f"Sheet name contains invalid character: '{char}'")
        
        return errors
    
    def get_summary(self) -> str:
        """Get a summary string for the template mapping"""
        visible_count = len(self.get_visible_columns())
        total_count = len(self.columns)
        hidden_count = len(self.hidden_columns)
        
        return (f"Template: {total_count} columns ({visible_count} visible, {hidden_count} hidden), "
                f"Output: '{self.get_output_setting('sheet_name', 'Unknown')}'")
    
    def reset_to_defaults(self):
        """Reset template mapping to default values"""
        self._set_defaults()
        self.custom_headers.clear()
        self.hidden_columns.clear()
        self.dataChanged.emit()
    
    def clone(self) -> 'TemplateMappingModel':
        """Create a copy of this template mapping"""
        new_template = TemplateMappingModel()
        new_template.columns = self.columns.copy()
        new_template.output_settings = self.output_settings.copy()
        new_template.custom_headers = self.custom_headers.copy()
        new_template.column_order = self.column_order.copy()
        new_template.hidden_columns = self.hidden_columns.copy()
        return new_template