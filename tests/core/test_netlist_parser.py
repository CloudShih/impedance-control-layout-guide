"""Tests for :mod:`src.core.netlist_parser`."""
from pathlib import Path

from src.core.netlist_parser import NetlistParser


class TestNetlistParser:
    """Test cases for netlist parsing functionality."""

    def test_parse_valid_netlist(self, tmp_path, sample_netlist_content):
        """Parser should return all net names from a valid file."""
        netlist = tmp_path / "sample.net"
        netlist.write_text(sample_netlist_content)
        parser = NetlistParser()
        nets = parser.parse(netlist)
        assert "I2C_SCL" in nets and "RF_ANT1" in nets
        assert len(nets) == 7

    def test_parse_empty_netlist(self, tmp_path):
        """Empty files result in no net names."""
        netlist = tmp_path / "empty.net"
        netlist.write_text("")
        parser = NetlistParser()
        assert parser.parse(netlist) == []

    def test_parse_invalid_format(self, tmp_path, sample_invalid_netlist):
        """Invalid formats simply produce an empty list."""
        netlist = tmp_path / "invalid.net"
        netlist.write_text(sample_invalid_netlist)
        parser = NetlistParser()
        assert parser.parse(netlist) == []

    def test_extract_net_names(self, sample_netlist_content):
        """Raw extraction should include all names before filtering."""
        parser = NetlistParser()
        names = parser._extract_net_names(sample_netlist_content)
        assert "I2C_SCL" in names
        assert "R123" not in names

    def test_filter_excluded_components(self):
        """Component references and numbers are removed."""
        parser = NetlistParser()
        names = ["R123", "TEST", "123", "NET1"]
        filtered = parser._filter_excluded_names(names)
        assert filtered == ["TEST", "NET1"]

    def test_parse_large_netlist(self, tmp_path, large_netlist):
        """Large netlists should be parsed completely."""
        netlist = tmp_path / "large.net"
        netlist.write_text(large_netlist)
        parser = NetlistParser()
        nets = parser.parse(netlist)
        assert len(nets) == 1000