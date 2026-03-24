import pytest

from uqtestfuns.core.registry.registry import Registry
from uqtestfuns.core.registry.spec_parser import SpecValidationError

from pathlib import Path

VALID_YAML_DIR = Path(__file__).parent / "fixtures" / "valid_yaml"

PKG_ROOT = VALID_YAML_DIR


class TestScan:
    """All tests related to scanning for valid YAML files in the registry."""

    def test_scan(self):
        """Test scanning for valid YAML files into the registry."""
        registry = Registry()
        registry.scan(VALID_YAML_DIR, PKG_ROOT)

        expected = sum(
            1
            for f in VALID_YAML_DIR.iterdir()
            if f.is_file()
            and f.suffix == ".yaml"
            and not f.name.endswith("_inputs.yaml")
        )

        # Assertion
        assert len(registry) == expected

    def test_getitem(self):
        """Test getting an entry from the registry."""
        registry = Registry()
        registry.scan(VALID_YAML_DIR, PKG_ROOT)

        # Assertion
        for key in registry.keys():
            assert registry[key].name == key

    def test_item(self):
        """Test getting an item from the registry."""
        registry = Registry()
        registry.scan(VALID_YAML_DIR, PKG_ROOT)

        # Assertion
        for key, value in registry.items():
            assert value.name == key

    def test_getitem_invalid(self):
        """Test getting an invalid entry from the registry."""
        registry = Registry()

        with pytest.raises(KeyError):
            _ = registry["invalid_key"]

    def test_duplicate_keys(self):
        """Test that duplicate keys are not allowed."""
        registry = Registry()
        registry.scan(VALID_YAML_DIR, PKG_ROOT)

        with pytest.raises(SpecValidationError):
            registry.scan(VALID_YAML_DIR, PKG_ROOT)
