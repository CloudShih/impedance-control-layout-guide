"""
Signal Rule Controller for managing signal classification rule operations
信號規則控制器，用於管理信號分類規則操作
"""

from typing import List, Dict, Any, Optional
from PyQt5.QtCore import QObject, pyqtSignal

try:
    from ..models.signal_rule_model import SignalRuleModel
except ImportError:
    # Fallback for when relative imports don't work
    from models.signal_rule_model import SignalRuleModel


class SignalRuleController(QObject):
    """
    Controller for managing signal rule operations
    信號規則操作控制器
    """
    
    # Signals for notifying view updates
    ruleAdded = pyqtSignal(str)         # rule name
    ruleRemoved = pyqtSignal(str)       # rule name
    ruleModified = pyqtSignal(str)      # rule name
    ruleValidated = pyqtSignal(str, bool, list)  # rule name, success, errors
    testCompleted = pyqtSignal(str, list)  # rule name, matched nets
    
    def __init__(self, signal_rules: Dict[str, SignalRuleModel]):
        super().__init__()
        self.signal_rules = signal_rules
    
    def add_rule(self, rule_name: str, rule_data: Optional[Dict[str, Any]] = None) -> bool:
        """Add a new signal rule"""
        try:
            if rule_name in self.signal_rules:
                return False
            
            new_rule = SignalRuleModel()
            if rule_data:
                new_rule.load_from_dict(rule_name, rule_data)
            else:
                new_rule.name = rule_name
            
            new_rule.dataChanged.connect(lambda: self.ruleModified.emit(rule_name))
            
            self.signal_rules[rule_name] = new_rule
            self.ruleAdded.emit(rule_name)
            return True
            
        except Exception:
            return False
    
    def remove_rule(self, rule_name: str) -> bool:
        """Remove a signal rule"""
        if rule_name in self.signal_rules:
            del self.signal_rules[rule_name]
            self.ruleRemoved.emit(rule_name)
            return True
        return False
    
    def validate_rule(self, rule_name: str) -> bool:
        """Validate a specific rule"""
        if rule_name not in self.signal_rules:
            return False
        
        rule = self.signal_rules[rule_name]
        errors = rule.validate()
        success = len(errors) == 0
        
        self.ruleValidated.emit(rule_name, success, errors)
        return success
    
    def test_rule_against_nets(self, rule_name: str, net_list: List[str]) -> List[str]:
        """Test rule against a list of net names"""
        if rule_name not in self.signal_rules:
            return []
        
        rule = self.signal_rules[rule_name]
        matched_nets = [net for net in net_list if rule.matches_net(net)]
        
        self.testCompleted.emit(rule_name, matched_nets)
        return matched_nets