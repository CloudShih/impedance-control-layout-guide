"""
Configuration Model for managing YAML configuration data
配置模型，用於管理YAML配置資料
"""

import yaml
import copy
from pathlib import Path
from typing import Dict, List, Any, Optional
from PyQt5.QtCore import QObject, pyqtSignal

from models.signal_rule_model import SignalRuleModel
from models.layout_rule_model import LayoutRuleModel
from models.template_mapping_model import TemplateMappingModel


class ConfigurationModel(QObject):
    """
    Main configuration model that manages all configuration data
    主要配置模型，管理所有配置資料
    """
    
    # Signals for notifying view updates
    dataChanged = pyqtSignal()
    configLoaded = pyqtSignal(str)  # config file path
    configSaved = pyqtSignal(str)   # config file path
    validationError = pyqtSignal(str)  # error message
    
    def __init__(self):
        super().__init__()
        self.config_file_path: Optional[Path] = None
        self.app_info: Dict[str, Any] = {}
        self.netlist_parser: Dict[str, Any] = {}
        self.signal_rules: Dict[str, SignalRuleModel] = {}
        self.layout_rules: Dict[str, LayoutRuleModel] = {}
        self.template_mapping: TemplateMappingModel = TemplateMappingModel()
        self.ui_settings: Dict[str, Any] = {}
        self.logging: Dict[str, Any] = {}
        
        # Load default configuration
        self._load_default_config()
    
    def _load_default_config(self):
        """Load default configuration from default_config.yaml"""
        try:
            # Check if running in PyInstaller bundle
            import sys
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                # Running in PyInstaller bundle
                default_config_path = Path(sys._MEIPASS) / "src" / "config" / "default_config.yaml"
            else:
                # Running in development
                default_config_path = Path(__file__).parent.parent / "config" / "default_config.yaml"
            
            if default_config_path.exists():
                self.load_config(default_config_path)
            else:
                print(f"Warning: Config file not found at {default_config_path}")
        except Exception as e:
            print(f"Warning: Could not load default config: {e}")
    
    def load_config(self, config_path: Path) -> bool:
        """
        Load configuration from YAML file
        從YAML檔案載入配置
        """
        try:
            # Ensure config_path is a proper file path
            if not isinstance(config_path, (Path, str)):
                raise ValueError(f"config_path must be a Path or str, got {type(config_path)}: {config_path}")
            
            # Convert to Path object if it's a string
            if isinstance(config_path, str):
                config_path = Path(config_path)
            
            # Validate the path exists
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
            with open(config_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
            
            self._parse_config_data(config_data)
            self.config_file_path = config_path
            
            self.configLoaded.emit(str(config_path))
            self.dataChanged.emit()
            return True
            
        except Exception as e:
            error_msg = f"Failed to load config from {config_path}: {str(e)}"
            self.validationError.emit(error_msg)
            return False
    
    def save_config(self, config_path: Optional[Path] = None) -> bool:
        """
        Save current configuration to YAML file
        將目前配置儲存到YAML檔案
        """
        try:
            if config_path is None:
                config_path = self.config_file_path
            
            if config_path is None:
                raise ValueError("No config file path specified")
            
            config_data = self._build_config_data()
            
            with open(config_path, 'w', encoding='utf-8') as file:
                yaml.safe_dump(config_data, file, 
                             default_flow_style=False, 
                             allow_unicode=True,
                             indent=2)
            
            self.config_file_path = config_path
            self.configSaved.emit(str(config_path))
            return True
            
        except Exception as e:
            error_msg = f"Failed to save config: {str(e)}"
            self.validationError.emit(error_msg)
            return False
    
    def _parse_config_data(self, config_data: Dict[str, Any]):
        """Parse loaded YAML data into model objects"""
        try:
            # Parse app info
            self.app_info = config_data.get('app_info', {})
            
            # Parse netlist parser settings
            self.netlist_parser = config_data.get('netlist_parser', {})
            
            # Parse signal classification rules
            signal_rules_data = config_data.get('net_classification_rules', {})
            self.signal_rules.clear()
            for rule_name, rule_data in signal_rules_data.items():
                signal_rule = SignalRuleModel()
                signal_rule.load_from_dict(rule_name, rule_data)
                self.signal_rules[rule_name] = signal_rule
            
            # Parse layout rules
            layout_rules_data = config_data.get('layout_rules', {})
            self.layout_rules.clear()
            for rule_name, rule_data in layout_rules_data.items():
                layout_rule = LayoutRuleModel()
                layout_rule.load_from_dict(rule_name, rule_data)
                self.layout_rules[rule_name] = layout_rule
            
            # Parse template mapping
            template_data = config_data.get('template_mapping', {})
            self.template_mapping.load_from_dict(template_data)
            
            # Parse UI settings
            self.ui_settings = config_data.get('ui_settings', {})
            
            # Parse logging settings
            self.logging = config_data.get('logging', {})
            
        except Exception as e:
            error_msg = f"Error parsing configuration data: {str(e)}"
            print(error_msg)
            raise  # Re-raise the exception
    
    def _build_config_data(self) -> Dict[str, Any]:
        """Build YAML data from current model objects"""
        
        config_data = {}
        
        # Build app info
        config_data['app_info'] = self.app_info
        
        # Build netlist parser settings
        config_data['netlist_parser'] = self.netlist_parser
        
        # Build signal classification rules
        net_classification_rules = {}
        for rule_name, signal_rule in self.signal_rules.items():
            net_classification_rules[rule_name] = signal_rule.to_dict()
        config_data['net_classification_rules'] = net_classification_rules
        
        # Build layout rules
        layout_rules = {}
        for rule_name, layout_rule in self.layout_rules.items():
            layout_rules[rule_name] = layout_rule.to_dict()
        config_data['layout_rules'] = layout_rules
        
        # Build template mapping
        config_data['template_mapping'] = self.template_mapping.to_dict()
        
        # Build UI settings
        config_data['ui_settings'] = self.ui_settings
        
        # Build logging settings
        config_data['logging'] = self.logging
        
        return config_data
    
    def add_signal_rule(self, rule_name: str) -> SignalRuleModel:
        """Add a new signal rule"""
        signal_rule = SignalRuleModel()
        signal_rule.name = rule_name
        self.signal_rules[rule_name] = signal_rule
        self.dataChanged.emit()
        return signal_rule
    
    def remove_signal_rule(self, rule_name: str) -> bool:
        """Remove a signal rule"""
        if rule_name in self.signal_rules:
            del self.signal_rules[rule_name]
            self.dataChanged.emit()
            return True
        return False
    
    def add_layout_rule(self, rule_name: str) -> LayoutRuleModel:
        """Add a new layout rule"""
        layout_rule = LayoutRuleModel()
        layout_rule.name = rule_name
        self.layout_rules[rule_name] = layout_rule
        self.dataChanged.emit()
        return layout_rule
    
    def remove_layout_rule(self, rule_name: str) -> bool:
        """Remove a layout rule"""
        if rule_name in self.layout_rules:
            del self.layout_rules[rule_name]
            self.dataChanged.emit()
            return True
        return False
    
    def validate_config(self) -> List[str]:
        """Validate current configuration and return list of errors"""
        errors = []
        
        # Validate signal rules
        for rule_name, signal_rule in self.signal_rules.items():
            rule_errors = signal_rule.validate()
            if rule_errors:
                errors.extend([f"Signal rule '{rule_name}': {error}" for error in rule_errors])
        
        # Validate layout rules
        for rule_name, layout_rule in self.layout_rules.items():
            rule_errors = layout_rule.validate()
            if rule_errors:
                errors.extend([f"Layout rule '{rule_name}': {error}" for error in rule_errors])
        
        # Validate template mapping
        template_errors = self.template_mapping.validate() 
        if template_errors:
            errors.extend([f"Template mapping: {error}" for error in template_errors])
        
        return errors
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration"""
        return {
            'config_file': str(self.config_file_path) if self.config_file_path else "None",
            'signal_rules_count': len(self.signal_rules),
            'layout_rules_count': len(self.layout_rules),
            'template_columns': len(self.template_mapping.columns),
            'validation_errors': len(self.validate_config())
        }