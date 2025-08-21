"""Tests for the NetClassifier using ConfigManager rules."""
from src.core.net_classifier import NetClassifier
from src.config.config_manager import ConfigManager


class TestNetClassifier:
    """Test cases for net classification."""

    def test_classify_with_config_manager(self, config_data):
        cm = ConfigManager()
        cm.config_data = config_data
        classifier = NetClassifier(cm)

        results = classifier.classify(["I2C_SCL", "UNKNOWN_NET"])

        assert results["I2C_SCL"]["signal_type"] == "I2C"
        assert results["UNKNOWN_NET"]["category"] == "Other"

