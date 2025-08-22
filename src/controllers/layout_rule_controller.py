"""
Layout Rule Controller for managing layout rule operations
佈局規則控制器，用於管理佈局規則操作
"""

from typing import List, Dict, Any, Optional
import logging
from PyQt5.QtCore import QObject, pyqtSignal

from models.layout_rule_model import LayoutRuleModel


logger = logging.getLogger(__name__)


class LayoutRuleController(QObject):
    """
    Controller for managing layout rule operations
    佈局規則操作控制器
    """
    
    # Signals for notifying view updates
    ruleAdded = pyqtSignal(str)         # rule name
    ruleRemoved = pyqtSignal(str)       # rule name
    ruleModified = pyqtSignal(str)      # rule name
    ruleValidated = pyqtSignal(str, bool, list)  # rule name, success, errors
    errorOccurred = pyqtSignal(str)     # error message
    
    def __init__(self, layout_rules: Dict[str, LayoutRuleModel]):
        super().__init__()
        self.layout_rules = layout_rules
    
    def add_rule(self, rule_name: str, rule_data: Optional[Dict[str, Any]] = None) -> bool:
        """Add a new layout rule"""
        try:
            if rule_name in self.layout_rules:
                return False
            
            new_rule = LayoutRuleModel()
            if rule_data:
                new_rule.load_from_dict(rule_name, rule_data)
            else:
                new_rule.name = rule_name
            
            new_rule.dataChanged.connect(lambda: self.ruleModified.emit(rule_name))
            
            self.layout_rules[rule_name] = new_rule
            self.ruleAdded.emit(rule_name)
            return True
            
        except Exception as e:
            logger.exception(f"Failed to add rule {rule_name}: {e}")
            self.errorOccurred.emit(str(e))
            raise
    
    def remove_rule(self, rule_name: str) -> bool:
        """Remove a layout rule"""
        if rule_name in self.layout_rules:
            del self.layout_rules[rule_name]
            self.ruleRemoved.emit(rule_name)
            return True
        return False
    
    def validate_rule(self, rule_name: str) -> bool:
        """Validate a specific rule"""
        if rule_name not in self.layout_rules:
            return False
        
        rule = self.layout_rules[rule_name]
        errors = rule.validate()
        success = len(errors) == 0
        
        self.ruleValidated.emit(rule_name, success, errors)
        return success
