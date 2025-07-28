"""
Test configuration and fixtures for impedance control tool tests.
"""
import pytest
import yaml
import pandas as pd
from pathlib import Path
from typing import Dict, Any

@pytest.fixture(scope="session")
def test_data_dir():
    """Get the test data directory path."""
    return Path(__file__).parent / "data"

@pytest.fixture(scope="session")
def config_data():
    """Load default configuration data for testing."""
    return {
        "net_classification_rules": {
            "I2C": {
                "keywords": ["I2C", "SCL", "SDA", "ADR"],
                "patterns": [r".*I2C.*", r".*SCL.*", r".*SDA.*"],
                "signal_type": "I2C",
                "category": "Communication Interface"
            },
            "SPI": {
                "keywords": ["SPI", "CSB", "MI", "MO", "SCLK"],
                "patterns": [r".*SPI.*", r".*CSB.*", r".*MI.*", r".*MO.*"],
                "signal_type": "SPI", 
                "category": "Communication Interface"
            },
            "RF": {
                "keywords": ["RF", "ANT", "RX", "TX"],
                "patterns": [r".*RF.*", r".*ANT.*", r".*RX.*", r".*TX.*"],
                "signal_type": "Single-End",
                "category": "RF"
            }
        },
        "layout_rules": {
            "I2C": {
                "impedance": "50 Ohm",
                "description": "I2C layout rules with proper shielding",
                "width": "5 mil",
                "length_limit": "6 inch"
            },
            "SPI": {
                "impedance": "50 Ohm", 
                "description": "SPI layout rules with ground shielding",
                "width": "5 mil",
                "length_limit": "6 inch"
            },
            "RF": {
                "impedance": "50 Ohm",
                "description": "RF layout with ground surrounding",
                "width": "Variable",
                "length_limit": "Variable"
            }
        },
        "template_mapping": {
            "columns": {
                "Category": "Category",
                "Net Name": "Net Name", 
                "Pin": "Pin (MT7921)",
                "Description": "Description",
                "Impedance": "Impedance",
                "Type": "Type",
                "Width": "Width",
                "Length Limit": "Length Limit (mil)"
            }
        }
    }

@pytest.fixture
def sample_netlist_content():
    """Sample netlist file content for testing."""
    return """
1 I2C_SCL R123 C456 L789
2 I2C_SDA R234 C567 L890
3 SPI_MOSI R345 C678 L901
4 SPI_MISO R456 C789 L012
5 RF_ANT1 R567 C890 L123
6 POWER_VDD R678 C901 L234
7 GPIO_TEST R789 C012 L345
"""

@pytest.fixture
def sample_excel_template(tmp_path):
    """Create a sample Excel template for testing."""
    template_path = tmp_path / "sample_template.xlsx"
    
    # Create sample template structure
    template_data = {
        "Category": ["Communication Interface", "RF", "Power"],
        "Net Name": ["SAMPLE_NET1", "SAMPLE_NET2", "SAMPLE_NET3"],
        "Pin (MT7921)": ["A1", "B2", "C3"],
        "Description": ["Sample desc 1", "Sample desc 2", "Sample desc 3"],
        "Impedance": ["50 Ohm", "50 Ohm", "N/A"],
        "Type": ["I2C", "Single-End", "Power"],
        "Width": ["5 mil", "Variable", "10 mil"],
        "Length Limit (mil)": ["6000", "Variable", "1000"]
    }
    
    df = pd.DataFrame(template_data)
    df.to_excel(template_path, index=False)
    
    return template_path

@pytest.fixture
def sample_invalid_netlist():
    """Invalid netlist content for error testing."""
    return "This is not a valid netlist format"

@pytest.fixture
def empty_netlist():
    """Empty netlist for edge case testing."""
    return ""

@pytest.fixture
def large_netlist():
    """Large netlist for performance testing."""
    lines = []
    for i in range(1000):
        lines.append(f"{i+1} TEST_NET_{i} R{i} C{i} L{i}")
    return "\n".join(lines)

@pytest.fixture
def mock_excel_file(tmp_path):
    """Create a mock Excel file for template testing."""
    excel_path = tmp_path / "mock_template.xlsx"
    
    data = {
        "Column1": [1, 2, 3],
        "Column2": ["A", "B", "C"], 
        "Column3": [True, False, True]
    }
    
    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)
    
    return excel_path