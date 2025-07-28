"""
Layout Rule Model for managing layout design rules
佈局規則模型，用於管理佈局設計規則
"""

from typing import Dict, Any, List, Optional
from PyQt5.QtCore import QObject, pyqtSignal


class LayoutRuleModel(QObject):
    """
    Model for individual layout design rule
    個別佈局設計規則的模型
    """
    
    # Signals for notifying changes
    dataChanged = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.name: str = ""
        self.impedance: str = "50 Ohm"
        self.description: str = ""
        self.width: str = "5 mil"
        self.length_limit: str = "No specific limit"
        self.spacing: str = "3W spacing"
        self.via_rules: str = "Standard via rules"
        self.layer_stack: str = "Any signal layer"
        self.shielding: str = "Optional"
        self.notes: str = ""
        self.enabled: bool = True
        
        # Additional technical parameters
        self.differential_impedance: Optional[str] = None
        self.max_length_mm: Optional[float] = None
        self.min_spacing_mm: Optional[float] = None
        self.max_via_count: Optional[int] = None
        self.required_layers: List[str] = []
    
    def load_from_dict(self, name: str, data: Dict[str, Any]):
        """Load layout rule from dictionary data"""
        self.name = name
        self.impedance = data.get('impedance', '50 Ohm')
        self.description = data.get('description', '')
        self.width = data.get('width', '5 mil')
        self.length_limit = data.get('length_limit', 'No specific limit')
        self.spacing = data.get('spacing', '3W spacing')
        self.via_rules = data.get('via_rules', 'Standard via rules')
        self.layer_stack = data.get('layer_stack', 'Any signal layer')
        self.shielding = data.get('shielding', 'Optional')
        self.notes = data.get('notes', '')
        self.enabled = data.get('enabled', True)
        
        # Load additional technical parameters
        self.differential_impedance = data.get('differential_impedance')
        self.max_length_mm = data.get('max_length_mm')
        self.min_spacing_mm = data.get('min_spacing_mm')
        self.max_via_count = data.get('max_via_count')
        self.required_layers = data.get('required_layers', [])
        
        self.dataChanged.emit()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert layout rule to dictionary"""
        result = {
            'impedance': self.impedance,
            'description': self.description,
            'width': self.width,
            'length_limit': self.length_limit,
            'spacing': self.spacing,
            'via_rules': self.via_rules,
            'layer_stack': self.layer_stack,
            'shielding': self.shielding,
            'notes': self.notes,
            'enabled': self.enabled
        }
        
        # Add optional technical parameters if they exist
        if self.differential_impedance is not None:
            result['differential_impedance'] = self.differential_impedance
        if self.max_length_mm is not None:
            result['max_length_mm'] = self.max_length_mm
        if self.min_spacing_mm is not None:
            result['min_spacing_mm'] = self.min_spacing_mm
        if self.max_via_count is not None:
            result['max_via_count'] = self.max_via_count
        if self.required_layers:
            result['required_layers'] = self.required_layers
        
        return result
    
    def set_impedance(self, impedance: str):
        """Set the impedance requirement"""
        if self.impedance != impedance:
            self.impedance = impedance
            self.dataChanged.emit()
    
    def set_description(self, description: str):
        """Set the rule description"""
        if self.description != description:
            self.description = description
            self.dataChanged.emit()
    
    def set_width(self, width: str):
        """Set the trace width requirement"""
        if self.width != width:
            self.width = width
            self.dataChanged.emit()
    
    def set_length_limit(self, length_limit: str):
        """Set the length limit requirement"""
        if self.length_limit != length_limit:
            self.length_limit = length_limit
            self.dataChanged.emit()
    
    def set_spacing(self, spacing: str):
        """Set the spacing requirement"""
        if self.spacing != spacing:
            self.spacing = spacing
            self.dataChanged.emit()
    
    def set_via_rules(self, via_rules: str):
        """Set the via rules"""
        if self.via_rules != via_rules:
            self.via_rules = via_rules
            self.dataChanged.emit()
    
    def set_layer_stack(self, layer_stack: str):
        """Set the layer stack requirement"""
        if self.layer_stack != layer_stack:
            self.layer_stack = layer_stack
            self.dataChanged.emit()
    
    def set_shielding(self, shielding: str):
        """Set the shielding requirement"""
        if self.shielding != shielding:
            self.shielding = shielding
            self.dataChanged.emit()
    
    def set_notes(self, notes: str):
        """Set the additional notes"""
        if self.notes != notes:
            self.notes = notes
            self.dataChanged.emit()
    
    def set_enabled(self, enabled: bool):
        """Enable or disable the rule"""
        if self.enabled != enabled:
            self.enabled = enabled
            self.dataChanged.emit()
    
    def set_differential_impedance(self, diff_impedance: Optional[str]):
        """Set differential impedance requirement"""
        if self.differential_impedance != diff_impedance:
            self.differential_impedance = diff_impedance
            self.dataChanged.emit()
    
    def set_max_length_mm(self, max_length: Optional[float]):
        """Set maximum length in mm"""
        if self.max_length_mm != max_length:
            self.max_length_mm = max_length
            self.dataChanged.emit()
    
    def set_min_spacing_mm(self, min_spacing: Optional[float]):
        """Set minimum spacing in mm"""
        if self.min_spacing_mm != min_spacing:
            self.min_spacing_mm = min_spacing
            self.dataChanged.emit()
    
    def set_max_via_count(self, max_vias: Optional[int]):
        """Set maximum via count"""
        if self.max_via_count != max_vias:
            self.max_via_count = max_vias
            self.dataChanged.emit()
    
    def add_required_layer(self, layer: str):
        """Add a required layer"""
        if layer and layer not in self.required_layers:
            self.required_layers.append(layer)
            self.dataChanged.emit()
    
    def remove_required_layer(self, layer: str):
        """Remove a required layer"""
        if layer in self.required_layers:
            self.required_layers.remove(layer)
            self.dataChanged.emit()
    
    def validate(self) -> List[str]:
        """Validate the layout rule and return list of errors"""
        errors = []
        
        if not self.name.strip():
            errors.append("Rule name cannot be empty")
        
        if not self.impedance.strip():
            errors.append("Impedance cannot be empty")
        
        if not self.width.strip():
            errors.append("Width cannot be empty")
        
        # Validate numerical values if they exist
        if self.max_length_mm is not None and self.max_length_mm <= 0:
            errors.append("Maximum length must be positive")
        
        if self.min_spacing_mm is not None and self.min_spacing_mm < 0:
            errors.append("Minimum spacing cannot be negative")
        
        if self.max_via_count is not None and self.max_via_count < 0:
            errors.append("Maximum via count cannot be negative")
        
        # Validate impedance format (basic check)
        if self.impedance:
            impedance_lower = self.impedance.lower()
            if 'ohm' not in impedance_lower and 'ω' not in impedance_lower:
                errors.append("Impedance should include 'Ohm' or 'Ω' unit")
        
        return errors
    
    def get_summary(self) -> str:
        """Get a summary string for this rule"""
        enabled_str = "✓" if self.enabled else "✗"
        impedance_short = self.impedance.replace("Ohm", "Ω")
        
        summary = f"{enabled_str} {self.name} ({impedance_short}, {self.width})"
        
        if self.differential_impedance:
            diff_short = self.differential_impedance.replace("Ohm", "Ω")
            summary += f" [Diff: {diff_short}]"
        
        if self.max_length_mm:
            summary += f" [Max: {self.max_length_mm}mm]"
        
        return summary
    
    def is_differential(self) -> bool:
        """Check if this rule is for differential signals"""
        return (self.differential_impedance is not None or 
                'differential' in self.impedance.lower() or
                'diff' in self.impedance.lower())
    
    def get_impedance_value(self) -> Optional[float]:
        """Extract numerical impedance value"""
        try:
            # Extract number from impedance string
            import re
            match = re.search(r'(\d+(?:\.\d+)?)', self.impedance)
            if match:
                return float(match.group(1))
        except:
            pass
        return None
    
    def clone(self) -> 'LayoutRuleModel':
        """Create a copy of this layout rule"""
        new_rule = LayoutRuleModel()
        new_rule.name = f"{self.name}_copy"
        new_rule.impedance = self.impedance
        new_rule.description = self.description
        new_rule.width = self.width
        new_rule.length_limit = self.length_limit
        new_rule.spacing = self.spacing
        new_rule.via_rules = self.via_rules
        new_rule.layer_stack = self.layer_stack
        new_rule.shielding = self.shielding
        new_rule.notes = self.notes
        new_rule.enabled = self.enabled
        new_rule.differential_impedance = self.differential_impedance
        new_rule.max_length_mm = self.max_length_mm
        new_rule.min_spacing_mm = self.min_spacing_mm
        new_rule.max_via_count = self.max_via_count
        new_rule.required_layers = self.required_layers.copy()
        return new_rule