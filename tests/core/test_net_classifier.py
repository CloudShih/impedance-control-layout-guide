"""Unit tests for :mod:`src.core.net_classifier`."""
from src.core.net_classifier import NetClassifier


class TestNetClassifier:
    """Test cases for net classification functionality."""

    def test_classify_i2c_nets(self, config_data):
        """I2C related net names should be classified correctly."""
        classifier = NetClassifier(config_data)
        result = classifier.classify(["I2C_SCL", "I2C_SDA"])
        assert result["I2C_SCL"]["signal_type"] == "I2C"
        assert result["I2C_SDA"]["category"] == "Communication Interface"

    def test_classify_spi_nets(self, config_data):
        """SPI nets should match the SPI rule."""
        classifier = NetClassifier(config_data)
        result = classifier.classify(["SPI_MOSI"])
        assert result["SPI_MOSI"]["rule_matched"] == "SPI"

    def test_classify_rf_nets(self, config_data):
        """RF nets use the RF rule with category RF."""
        classifier = NetClassifier(config_data)
        result = classifier.classify(["RF_ANT1"])
        assert result["RF_ANT1"]["category"] == "RF"

    def test_classify_unknown_nets(self, config_data):
        """Unknown nets fall back to the default classification."""
        classifier = NetClassifier(config_data)
        result = classifier.classify(["UNKNOWN_NET"])
        assert result["UNKNOWN_NET"]["category"] == "Other"

    def test_regex_pattern_matching(self, config_data):
        """Regex patterns should match even if keywords are absent."""
        classifier = NetClassifier(config_data)
        result = classifier.classify(["SCL_MAIN"])
        assert result["SCL_MAIN"]["signal_type"] == "I2C"

    def test_keyword_matching(self, config_data):
        """Keyword matching should ignore case."""
        classifier = NetClassifier(config_data)
        result = classifier.classify(["rf_tx"])
        assert result["rf_tx"]["category"] == "RF"

    def test_case_insensitive_matching(self, config_data):
        """Classification should be case insensitive."""
        classifier = NetClassifier(config_data)
        result = classifier.classify(["spi_mosi"])
        assert result["spi_mosi"]["signal_type"] == "SPI"