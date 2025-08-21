"""
Layout Rule Model for managing layout design rules
佈局規則模型，用於管理佈局設計規則
"""

from dataclasses import dataclass, field, fields
from typing import Any, ClassVar, Dict, List, Optional
from PyQt5.QtCore import QObject, pyqtSignal


@dataclass(eq=False)
class LayoutRuleModel(QObject):
    """
    Model for individual layout design rule
    個別佈局設計規則的模型
    """

    # Signals for notifying changes
    dataChanged: ClassVar[pyqtSignal] = pyqtSignal()

    name: str = ""
    impedance: str = "50 Ohm"
    description: str = ""
    width: str = "5 mil"
    length_limit: str = "No specific limit"
    spacing: str = "3W spacing"
    via_rules: str = "Standard via rules"
    layer_stack: str = "Any signal layer"
    shielding: str = "Optional"
    notes: str = ""
    enabled: bool = True

    # Additional technical parameters
    differential_impedance: Optional[str] = None
    max_length_mm: Optional[float] = None
    min_spacing_mm: Optional[float] = None
    max_via_count: Optional[int] = None
    required_layers: List[str] = field(default_factory=list)

    def __post_init__(self):
        super().__init__()
    
    def load_from_dict(self, name: str, data: Dict[str, Any]):
        """Load layout rule from dictionary data"""
        self.name = name
        updates = {
            f.name: data.get(f.name, getattr(self, f.name))
            for f in fields(self) if f.name != 'name'
        }
        self.update(**updates)

    def update(self, **kwargs: Any):
        """Batch update attributes and emit change signal if modified"""
        changed = False
        for key, value in kwargs.items():
            if hasattr(self, key) and getattr(self, key) != value:
                setattr(self, key, value)
                changed = True
        if changed:
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
        data = self.to_dict()
        data['name'] = f"{self.name}_copy"
        if 'required_layers' in data:
            data['required_layers'] = data['required_layers'].copy()
        new_rule = LayoutRuleModel()
        new_rule.update(**data)
        return new_rule
