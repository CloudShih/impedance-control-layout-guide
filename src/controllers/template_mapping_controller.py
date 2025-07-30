"""
Template Mapping Controller for managing template operations
模板映射控制器，用於管理模板操作
"""

from typing import List, Dict, Any, Optional
from PyQt5.QtCore import QObject, pyqtSignal

from models.template_mapping_model import TemplateMappingModel


class TemplateMappingController(QObject):
    """
    Controller for managing template mapping operations
    模板映射操作控制器
    """
    
    # Signals for notifying view updates
    templateModified = pyqtSignal()
    columnAdded = pyqtSignal(str)       # column name
    columnRemoved = pyqtSignal(str)     # column name
    columnReordered = pyqtSignal()
    templateValidated = pyqtSignal(bool, list)  # success, errors
    
    def __init__(self, template_mapping: TemplateMappingModel):
        super().__init__()
        self.template_mapping = template_mapping
        
        # Connect to model signals
        self.template_mapping.dataChanged.connect(self.templateModified)
    
    def add_column(self, internal_name: str, display_name: str) -> bool:
        """Add a new column mapping"""
        try:
            self.template_mapping.add_column(internal_name, display_name)
            self.columnAdded.emit(internal_name)
            return True
        except Exception:
            return False
    
    def remove_column(self, internal_name: str) -> bool:
        """Remove a column mapping"""
        try:
            self.template_mapping.remove_column(internal_name)
            self.columnRemoved.emit(internal_name)
            return True
        except Exception:
            return False
    
    def reorder_columns(self, new_order: List[str]) -> bool:
        """Reorder columns"""
        try:
            self.template_mapping.update_column_order(new_order)
            self.columnReordered.emit()
            return True
        except Exception:
            return False
    
    def validate_template(self) -> bool:
        """Validate template mapping"""
        errors = self.template_mapping.validate()
        success = len(errors) == 0
        
        self.templateValidated.emit(success, errors)
        return success