"""
Netlist parser module for extracting net names from various netlist formats.
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
import re
import logging

logger = logging.getLogger(__name__)


class NetlistParseError(Exception):
    """Custom exception for netlist parsing errors."""
    pass


class NetlistParser:
    """Parser for different netlist file formats."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the netlist parser.
        
        Args:
            config: Configuration dictionary containing parser settings
        """
        self.config = config or {}
        self.supported_formats = ['.net', '.sp', '.cir', '.txt']
        self.excluded_patterns = [
            r'^[a-zA-Z][0-9]+$',  # Component references like R123, C45
            r'^[0-9]+$',          # Pure numbers
            r'^[0-9]+(ohm|f|h)$'  # Values like 10ohm, 22f, 1h
        ]
    
    def parse(self, netlist_path: Path) -> List[str]:
        """
        Parse netlist file and extract unique net names.
        
        Args:
            netlist_path: Path to the netlist file
            
        Returns:
            List of unique net names
            
        Raises:
            NetlistParseError: If parsing fails
        """
        try:
            if not netlist_path.exists():
                raise NetlistParseError(f"Netlist file not found: {netlist_path}")
            
            file_extension = netlist_path.suffix.lower()
            if file_extension not in self.supported_formats:
                logger.warning(f"Unsupported format {file_extension}, attempting generic parsing")
            
            with open(netlist_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            net_names = self._extract_net_names(content)
            filtered_names = self._filter_excluded_names(net_names)
            
            logger.info(f"Extracted {len(filtered_names)} net names from {netlist_path}")
            return sorted(list(set(filtered_names)))  # Remove duplicates and sort
            
        except Exception as e:
            raise NetlistParseError(f"Failed to parse netlist {netlist_path}: {str(e)}")
    
    def _extract_net_names(self, content: str) -> List[str]:
        """
        Extract net names from netlist content.
        
        Args:
            content: Raw netlist file content
            
        Returns:
            List of potential net names
        """
        net_names = []
        
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('*') or line.startswith('#'):
                continue  # Skip empty lines and comments
            
            # Check if line starts with a number (typical netlist format)
            if line and line[0].isdigit():
                parts = line.split()
                if len(parts) > 1:
                    # Second element is typically the net name
                    potential_net = parts[1]
                    if potential_net and not self._is_excluded_word(potential_net):
                        net_names.append(potential_net)
        
        return net_names
    
    def _filter_excluded_names(self, names: List[str]) -> List[str]:
        """
        Filter out component references and other excluded patterns.
        
        Args:
            names: List of potential net names
            
        Returns:
            Filtered list of net names
        """
        filtered = []
        for name in names:
            if not self._is_excluded_word(name):
                filtered.append(name)
        return filtered
    
    def _is_excluded_word(self, word: str) -> bool:
        """
        Check if a word matches excluded patterns.
        
        Args:
            word: Word to check
            
        Returns:
            True if word should be excluded
        """
        for pattern in self.excluded_patterns:
            if re.fullmatch(pattern, word, re.IGNORECASE):
                return True
        return False
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats."""
        return self.supported_formats.copy()
    
    def validate_netlist_format(self, netlist_path: Path) -> bool:
        """
        Validate if the netlist file format is supported.
        
        Args:
            netlist_path: Path to netlist file
            
        Returns:
            True if format is supported
        """
        return netlist_path.suffix.lower() in self.supported_formats
