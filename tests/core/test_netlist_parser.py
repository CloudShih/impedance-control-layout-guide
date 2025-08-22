"""Unit tests for netlist parser module."""

from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from core.netlist_parser import NetlistParseError, NetlistParser


@pytest.fixture
def parser():
    """Provide a NetlistParser instance for tests."""
    return NetlistParser()


@pytest.fixture
def netlist_file(tmp_path: Path):
    """Create a temporary netlist file from provided content."""

    def _create(content, name: str = "test.net", binary: bool = False) -> Path:
        path = tmp_path / name
        if binary:
            path.write_bytes(content)
        else:
            path.write_text(content)
        return path

    return _create


class TestNetlistParser:
    """Test cases for netlist parsing functionality."""

    def test_parse_valid_netlist(self, parser, netlist_file, sample_netlist_content):
        """Test parsing a valid netlist file."""
        path = netlist_file(sample_netlist_content, "valid.net")
        result = parser.parse(path)
        expected = sorted(
            [
                "I2C_SCL",
                "I2C_SDA",
                "SPI_MOSI",
                "SPI_MISO",
                "RF_ANT1",
                "POWER_VDD",
                "GPIO_TEST",
            ]
        )
        assert result == expected

    def test_parse_empty_netlist(self, parser, netlist_file, empty_netlist):
        """Test parsing an empty netlist file."""
        path = netlist_file(empty_netlist, "empty.net")
        assert parser.parse(path) == []

    def test_parse_invalid_format(self, parser, netlist_file, sample_invalid_netlist):
        """Test parsing invalid netlist format should raise exception."""
        path = netlist_file(sample_invalid_netlist.encode("utf-16"), "invalid.net", binary=True)
        with pytest.raises(NetlistParseError):
            parser.parse(path)

    def test_extract_net_names(self, parser, sample_netlist_content):
        """Test extraction of net names from netlist content."""
        names = parser._extract_net_names(sample_netlist_content)
        assert names == [
            "I2C_SCL",
            "I2C_SDA",
            "SPI_MOSI",
            "SPI_MISO",
            "RF_ANT1",
            "POWER_VDD",
            "GPIO_TEST",
        ]

    def test_filter_excluded_components(self, parser):
        """Test filtering of excluded component identifiers."""
        names = ["R123", "NET_A", "10ohm", "C456", "SIGNAL_1"]
        assert parser._filter_excluded_names(names) == ["NET_A", "SIGNAL_1"]

    def test_parse_large_netlist(self, parser, netlist_file, large_netlist):
        """Test parsing performance with large netlist files."""
        path = netlist_file(large_netlist, "large.net")
        result = parser.parse(path)
        assert len(result) == 1000
        assert "TEST_NET_0" in result
        assert "TEST_NET_999" in result

