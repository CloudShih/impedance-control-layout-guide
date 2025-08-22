"""Rule engine module for applying layout rules based on net classifications."""
from typing import List, Dict, Any, Optional
import logging
from config.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class RuleEngineError(Exception):
    """Custom exception for rule engine errors."""
    pass


class RuleEngine:
    """Engine for applying layout rules to classified networks."""

    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """Initialize the rule engine using rules from ``ConfigManager``.

        Args:
            config_manager: Configuration manager providing layout rules.
        """
        self.config_manager = config_manager or ConfigManager()
        self.layout_rules = self.config_manager.get_layout_rules()
    
    def apply_rules(self, classified_nets: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Apply layout rules to classified networks.
        
        Args:
            classified_nets: Dictionary of classified nets from NetClassifier
            
        Returns:
            Dictionary with net names mapped to complete layout information
        """
        results = {}
        
        for net_name, classification in classified_nets.items():
            layout_info = self._apply_single_rule(net_name, classification)
            results[net_name] = layout_info
        
        logger.info(f"Applied layout rules to {len(classified_nets)} nets")
        return results
    
    def _apply_single_rule(self, net_name: str, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply layout rule to a single net.
        
        Args:
            net_name: Name of the net
            classification: Classification information from NetClassifier
            
        Returns:
            Complete layout information for the net
        """
        signal_type = classification.get('signal_type', 'Single-End')
        category = classification.get('category', 'Other')
        
        # Find applicable layout rule
        rule_config = self._find_applicable_rule(signal_type, category)
        
        # Build complete layout information
        layout_info = {
            # Original classification info
            'net_name': net_name,
            'category': category,
            'signal_type': signal_type,
            'rule_matched': classification.get('rule_matched', 'default'),
            
            # Layout rule information
            'impedance': rule_config.get('impedance', '50 Ohm'),
            'description': rule_config.get('description', 'General purpose signal'),
            'width': rule_config.get('width', 'TBD'),
            'length_limit': rule_config.get('length_limit', 'TBD'),
            'spacing': rule_config.get('spacing', 'TBD'),
            'via_rules': rule_config.get('via_rules', 'Standard'),
            'layer_stack': rule_config.get('layer_stack', 'Any'),
            'shielding': rule_config.get('shielding', 'Optional'),
            
            # Additional fields for Excel output
            'pin_assignment': 'TBD',
            'notes': rule_config.get('notes', ''),
            'priority': classification.get('priority', 999)
        }
        
        return layout_info
    
    def _find_applicable_rule(self, signal_type: str, category: str) -> Dict[str, Any]:
        """
        Find the most applicable layout rule for a signal type and category.
        
        Args:
            signal_type: Type of signal (I2C, SPI, RF, etc.)
            category: Category of the net
            
        Returns:
            Layout rule configuration
        """
        # First try to match by signal type
        if signal_type in self.layout_rules:
            return self.layout_rules[signal_type]
        
        # Then try to match by category
        category_mappings = {
            'Communication Interface': 'I2C',  # Default for communication
            'High Speed Interface': 'PCIe',
            'RF': 'RF',
            'Power': 'Power'
        }
        
        mapped_type = category_mappings.get(category)
        if mapped_type and mapped_type in self.layout_rules:
            return self.layout_rules[mapped_type]
        
        # Return default rule
        return self.layout_rules.get('Default', {})
    
    def add_custom_rule(self, rule_type: str, rule_config: Dict[str, Any]) -> None:
        """
        Add a custom layout rule.
        
        Args:
            rule_type: Type/name of the rule
            rule_config: Rule configuration dictionary
        """
        self.layout_rules[rule_type] = rule_config
        logger.info(f"Added custom layout rule: {rule_type}")
    
    def validate_rule_config(self, rule_config: Dict[str, Any]) -> bool:
        """
        Validate a rule configuration.
        
        Args:
            rule_config: Rule configuration to validate
            
        Returns:
            True if configuration is valid
        """
        required_fields = ['impedance', 'description']
        for field in required_fields:
            if field not in rule_config:
                logger.error(f"Missing required field '{field}' in rule config")
                return False
        
        return True
    
    def get_rule_summary(self) -> Dict[str, List[str]]:
        """Get summary of available rules."""
        summary = {}
        for rule_type, config in self.layout_rules.items():
            summary[rule_type] = {
                'description': config.get('description', 'No description'),
                'impedance': config.get('impedance', 'Not specified'),
                'signal_types': config.get('applicable_signals', ['General'])
            }

        return summary
