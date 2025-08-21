"""
Signal Rule Model for managing signal classification rules
信號規則模型，用於管理信號分類規則
"""

from typing import List, Dict, Any, Optional
from PyQt5.QtCore import QObject, pyqtSignal


class SignalRuleModel(QObject):
    """
    Model for individual signal classification rule
    個別信號分類規則的模型
    """
    
    # Signals for notifying changes
    dataChanged = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.name: str = ""
        self.keywords: List[str] = []
        self.patterns: List[str] = []
        self.exact_matches: List[str] = []
        self.category: str = ""
        self.signal_type: str = ""
        self.priority: int = 10
        self.description: str = ""
        self.enabled: bool = True
    
    def load_from_dict(self, name: str, data: Dict[str, Any]):
        """Load signal rule from dictionary data"""
        self.name = name
        self.keywords = data.get('keywords', [])
        self.patterns = data.get('patterns', [])
        self.exact_matches = data.get('exact_matches', [])
        self.category = data.get('category', '')
        self.signal_type = data.get('signal_type', '')
        self.priority = data.get('priority', 10)
        self.description = data.get('description', '')
        self.enabled = data.get('enabled', True)
        
        self.dataChanged.emit()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert signal rule to dictionary"""
        return {
            'keywords': self.keywords,
            'patterns': self.patterns,
            'exact_matches': self.exact_matches,
            'category': self.category,
            'signal_type': self.signal_type,
            'priority': self.priority,
            'description': self.description,
            'enabled': self.enabled
        }
    
    def add_keyword(self, keyword: str):
        """Add a keyword to the rule"""
        if keyword and keyword not in self.keywords:
            self.keywords.append(keyword)
            self.dataChanged.emit()
    
    def remove_keyword(self, keyword: str):
        """Remove a keyword from the rule"""
        if keyword in self.keywords:
            self.keywords.remove(keyword)
            self.dataChanged.emit()
    
    def add_pattern(self, pattern: str):
        """Add a pattern to the rule"""
        if pattern and pattern not in self.patterns:
            self.patterns.append(pattern)
            self.dataChanged.emit()
    
    def remove_pattern(self, pattern: str):
        """Remove a pattern from the rule"""
        if pattern in self.patterns:
            self.patterns.remove(pattern)
            self.dataChanged.emit()
    
    def add_exact_match(self, match: str):
        """Add an exact match to the rule"""
        if match and match not in self.exact_matches:
            self.exact_matches.append(match)
            self.dataChanged.emit()
    
    def remove_exact_match(self, match: str):
        """Remove an exact match from the rule"""
        if match in self.exact_matches:
            self.exact_matches.remove(match)
            self.dataChanged.emit()
    
    def set_category(self, category: str):
        """Set the signal category"""
        if self.category != category:
            self.category = category
            self.dataChanged.emit()
    
    def set_signal_type(self, signal_type: str):
        """Set the signal type"""
        if self.signal_type != signal_type:
            self.signal_type = signal_type
            self.dataChanged.emit()
    
    def set_priority(self, priority: int):
        """Set the rule priority"""
        if self.priority != priority:
            self.priority = priority
            self.dataChanged.emit()
    
    def set_description(self, description: str):
        """Set the rule description"""
        if self.description != description:
            self.description = description
            self.dataChanged.emit()
    
    def set_enabled(self, enabled: bool):
        """Enable or disable the rule"""
        if self.enabled != enabled:
            self.enabled = enabled
            self.dataChanged.emit()
    
    def validate(self) -> List[str]:
        """Validate the signal rule and return list of errors"""
        errors = []
        
        if not self.name.strip():
            errors.append("Rule name cannot be empty")
        
        if not self.keywords and not self.patterns and not self.exact_matches:
            errors.append("At least one keyword, pattern, or exact match must be specified")
        
        if not self.category.strip():
            errors.append("Category cannot be empty")
        
        if not self.signal_type.strip():
            errors.append("Signal type cannot be empty")
        
        if self.priority < 0 or self.priority > 100:
            errors.append("Priority must be between 0 and 100")
        
        # Validate patterns (basic regex syntax check)
        import re
        for pattern in self.patterns:
            try:
                re.compile(pattern)
            except re.error as e:
                errors.append(f"Invalid pattern '{pattern}': {str(e)}")
        
        return errors
    
    def matches_net(self, net_name: str) -> bool:
        """Check if this rule matches a given net name"""
        import re
        
        if not self.enabled:
            return False
        
        net_name_upper = net_name.upper()
        
        # Check exact matches first
        for exact_match in self.exact_matches:
            if net_name_upper == exact_match.upper():
                return True
        
        # Check keywords
        for keyword in self.keywords:
            if keyword.upper() in net_name_upper:
                return True
        
        # Check patterns
        for pattern in self.patterns:
            try:
                if re.search(pattern, net_name, re.IGNORECASE):
                    return True
            except re.error:
                # Skip invalid patterns
                continue
        
        return False
    
    def get_summary(self) -> str:
        """Get a summary string for this rule"""
        enabled_str = "✓" if self.enabled else "✗"
        keyword_count = len(self.keywords)
        pattern_count = len(self.patterns)
        exact_count = len(self.exact_matches)
        
        return (f"{enabled_str} {self.name} ({self.category}/{self.signal_type}) "
                f"[K:{keyword_count}, P:{pattern_count}, E:{exact_count}] "
                f"Priority: {self.priority}")
    
    def clone(self) -> 'SignalRuleModel':
        """Create a copy of this signal rule"""
        new_rule = SignalRuleModel()
        new_rule.name = f"{self.name}_copy"
        new_rule.keywords = self.keywords.copy()
        new_rule.patterns = self.patterns.copy()
        new_rule.exact_matches = self.exact_matches.copy()
        new_rule.category = self.category
        new_rule.signal_type = self.signal_type
        new_rule.priority = self.priority
        new_rule.description = self.description
        new_rule.enabled = self.enabled
        return new_rule
