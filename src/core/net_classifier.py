"""Net classifier module for categorizing network names based on patterns and rules."""
from typing import List, Dict, Any, Optional, Tuple
import re
import logging
from config.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class NetClassificationError(Exception):
    """Custom exception for net classification errors."""
    pass


class NetClassifier:
    """Classifier for categorizing network names based on predefined rules."""

    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """Initialize the net classifier using rules from ``ConfigManager``.

        Args:
            config_manager: Configuration manager providing classification rules.
        """
        self.config_manager = config_manager or ConfigManager()
        self.classification_rules = self.config_manager.get_classification_rules()
    
    def classify(self, net_names: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Classify a list of net names according to predefined rules.
        
        Args:
            net_names: List of net names to classify
            
        Returns:
            Dictionary mapping net names to their classification details
        """
        results = {}
        
        for net_name in net_names:
            classification = self._classify_single_net(net_name)
            results[net_name] = classification
        
        logger.info(f"Classified {len(net_names)} nets")
        return results
    
    def _classify_single_net(self, net_name: str) -> Dict[str, Any]:
        """
        Classify a single net name.
        
        Args:
            net_name: Name of the net to classify
            
        Returns:
            Classification details including category, signal_type, etc.
        """
        # Try each classification rule
        for rule_name, rule_config in self.classification_rules.items():
            if self._matches_rule(net_name, rule_config):
                return {
                    'category': rule_config.get('category', 'Unknown'),
                    'signal_type': rule_config.get('signal_type', 'Single-End'),
                    'rule_matched': rule_name,
                    'priority': rule_config.get('priority', 100)
                }
        
        # Default classification if no rules match
        return {
            'category': 'Other',
            'signal_type': 'Single-End', 
            'rule_matched': 'default',
            'priority': 999
        }
    
    def _matches_rule(self, net_name: str, rule_config: Dict[str, Any]) -> bool:
        """
        Check if a net name matches a specific rule.
        
        Args:
            net_name: Name to check
            rule_config: Rule configuration dictionary
            
        Returns:
            True if net name matches the rule
        """
        # Check keyword matching
        keywords = rule_config.get('keywords', [])
        for keyword in keywords:
            if keyword.upper() in net_name.upper():
                return True
        
        # Check regex pattern matching
        patterns = rule_config.get('patterns', [])
        for pattern in patterns:
            try:
                if re.search(pattern, net_name, re.IGNORECASE):
                    return True
            except re.error as e:
                logger.warning(f"Invalid regex pattern '{pattern}': {e}")
        
        # Check exact matching
        exact_matches = rule_config.get('exact_matches', [])
        for exact in exact_matches:
            if net_name.upper() == exact.upper():
                return True
        
        return False
    
    def add_custom_rule(self, rule_name: str, rule_config: Dict[str, Any]) -> None:
        """
        Add a custom classification rule.
        
        Args:
            rule_name: Name of the rule
            rule_config: Rule configuration dictionary
        """
        required_fields = ['category', 'signal_type']
        for field in required_fields:
            if field not in rule_config:
                raise NetClassificationError(f"Missing required field '{field}' in rule config")
        
        self.classification_rules[rule_name] = rule_config
        logger.info(f"Added custom rule: {rule_name}")
    
    def get_classification_summary(self, classified_nets: Dict[str, Dict[str, Any]]) -> Dict[str, int]:
        """Get summary statistics of classification results."""
        summary = {}
        for net_data in classified_nets.values():
            category = net_data['category']
            summary[category] = summary.get(category, 0) + 1

        return summary
