"""
Configuration manager for loading and validating configuration files.
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import yaml
import json
import logging
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Custom exception for configuration errors."""
    pass


class ConfigManager:
    """Manager for loading and validating configuration files."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file (optional)
        """
        self.config_path = config_path
        self.config_data = {}
        self.default_config_path = Path(__file__).parent / "default_config.yaml"
        
    def load_config(self, config_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Configuration dictionary
            
        Raises:
            ConfigurationError: If loading fails
        """
        if config_path:
            self.config_path = config_path
            
        # Try to load user config first, fallback to default
        try:
            if self.config_path and self.config_path.exists():
                self.config_data = self._load_file(self.config_path)
                logger.info(f"Loaded configuration from: {self.config_path}")
            else:
                self.config_data = self._load_file(self.default_config_path)
                logger.info("Loaded default configuration")
                
            # Validate configuration
            self._validate_config(self.config_data)
            return self.config_data
            
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {str(e)}")
    
    def _load_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Load configuration from YAML or JSON file.
        
        Args:
            file_path: Path to configuration file
            
        Returns:
            Configuration dictionary
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.suffix.lower() in ['.yaml', '.yml']:
                    return yaml.safe_load(f)
                elif file_path.suffix.lower() == '.json':
                    return json.load(f)
                else:
                    raise ConfigurationError(f"Unsupported config file format: {file_path.suffix}")
                    
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML syntax in {file_path}: {str(e)}")
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON syntax in {file_path}: {str(e)}")
        except FileNotFoundError:
            raise ConfigurationError(f"Configuration file not found: {file_path}")
    
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate configuration structure.
        
        Args:
            config: Configuration dictionary to validate
            
        Raises:
            ConfigurationError: If validation fails
        """
        required_sections = [
            'net_classification_rules',
            'layout_rules',
            'template_mapping'
        ]
        
        for section in required_sections:
            if section not in config:
                raise ConfigurationError(f"Missing required configuration section: {section}")
        
        # Validate net classification rules
        self._validate_classification_rules(config['net_classification_rules'])
        
        # Validate layout rules
        self._validate_layout_rules(config['layout_rules'])
        
        # Validate template mapping
        self._validate_template_mapping(config['template_mapping'])
    
    def _validate_classification_rules(self, rules: Dict[str, Any]) -> None:
        """Validate net classification rules structure."""
        required_fields = ['category', 'signal_type', 'priority']
        
        for rule_name, rule_config in rules.items():
            for field in required_fields:
                if field not in rule_config:
                    raise ConfigurationError(
                        f"Missing required field '{field}' in classification rule '{rule_name}'"
                    )
    
    def _validate_layout_rules(self, rules: Dict[str, Any]) -> None:
        """Validate layout rules structure."""
        required_fields = ['impedance', 'description']
        
        for rule_name, rule_config in rules.items():
            for field in required_fields:
                if field not in rule_config:
                    raise ConfigurationError(
                        f"Missing required field '{field}' in layout rule '{rule_name}'"
                    )
    
    def _validate_template_mapping(self, mapping: Dict[str, Any]) -> None:
        """Validate template mapping structure."""
        if 'columns' not in mapping:
            raise ConfigurationError("Missing 'columns' section in template_mapping")
    
    def get_section(self, section_name: str) -> Dict[str, Any]:
        """
        Get a specific configuration section.
        
        Args:
            section_name: Name of the configuration section
            
        Returns:
            Configuration section dictionary
        """
        if not self.config_data:
            self.load_config()
            
        return self.config_data.get(section_name, {})
    
    def get_value(self, key_path: str, default_value: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key_path: Dot-separated key path (e.g., 'ui_settings.theme')
            default_value: Default value if key not found
            
        Returns:
            Configuration value
        """
        if not self.config_data:
            self.load_config()
            
        keys = key_path.split('.')
        value = self.config_data
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default_value
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """
        Update configuration with new values.
        
        Args:
            updates: Dictionary of updates to apply
        """
        if not self.config_data:
            self.load_config()
            
        self._deep_update(self.config_data, updates)
        self._validate_config(self.config_data)
    
    def _deep_update(self, base_dict: Dict[str, Any], update_dict: Dict[str, Any]) -> None:
        """
        Deep update dictionary values.
        
        Args:
            base_dict: Base dictionary to update
            update_dict: Updates to apply
        """
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def save_config(self, output_path: Optional[Path] = None) -> None:
        """
        Save current configuration to file.
        
        Args:
            output_path: Path to save configuration (optional)
        """
        if not self.config_data:
            raise ConfigurationError("No configuration data to save")
            
        save_path = output_path or self.config_path or Path("config.yaml")
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config_data, f, default_flow_style=False, 
                         allow_unicode=True, indent=2)
            logger.info(f"Configuration saved to: {save_path}")
            
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {str(e)}")
    
    def create_user_config_template(self, output_path: Path) -> None:
        """
        Create a user configuration template file.
        
        Args:
            output_path: Path for the template file
        """
        template_config = {
            'app_info': {
                'name': 'Custom Impedance Control Tool',
                'version': '2.0.0-custom'
            },
            'net_classification_rules': {
                'Custom_Rule': {
                    'keywords': ['CUSTOM'],
                    'patterns': ['.*CUSTOM.*'],
                    'category': 'Custom Category',
                    'signal_type': 'Custom Type',
                    'priority': 50
                }
            },
            'layout_rules': {
                'Custom_Rule': {
                    'impedance': '50 Ohm',
                    'description': 'Custom layout rule description',
                    'width': '5 mil',
                    'length_limit': 'No limit',
                    'spacing': '3W spacing',
                    'notes': 'Custom rule notes'
                }
            }
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(template_config, f, default_flow_style=False,
                         allow_unicode=True, indent=2)
            logger.info(f"User config template created at: {output_path}")
            
        except Exception as e:
            raise ConfigurationError(f"Failed to create config template: {str(e)}")
    
    def list_available_rules(self) -> Dict[str, List[str]]:
        """
        List all available classification and layout rules.
        
        Returns:
            Dictionary with rule categories and their names
        """
        if not self.config_data:
            self.load_config()
            
        return {
            'classification_rules': list(self.config_data.get('net_classification_rules', {}).keys()),
            'layout_rules': list(self.config_data.get('layout_rules', {}).keys())
        }
    
    def export_config_summary(self) -> Dict[str, Any]:
        """
        Export a summary of current configuration.
        
        Returns:
            Configuration summary dictionary
        """
        if not self.config_data:
            self.load_config()
            
        return {
            'app_info': self.config_data.get('app_info', {}),
            'total_classification_rules': len(self.config_data.get('net_classification_rules', {})),
            'total_layout_rules': len(self.config_data.get('layout_rules', {})),
            'supported_formats': self.config_data.get('netlist_parser', {}).get('supported_formats', []),
            'template_columns': list(self.config_data.get('template_mapping', {}).get('columns', {}).keys()),
            'config_source': str(self.config_path) if self.config_path else 'default'
        }