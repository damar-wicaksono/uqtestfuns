import pytest

from uqtestfuns.core.registry.entries import UQTestFunInfo
from uqtestfuns.core.registry.registry import Registry, is_inputs_yaml
from uqtestfuns.core.registry.parser import SpecValidationError

from pathlib import Path

VALID_YAML_DIR = Path(__file__).parent / "fixtures" / "valid_yaml"

PKG_ROOT = VALID_YAML_DIR


class TestScan:
    """All tests related to scanning for valid YAML files in the registry."""

    def test_scan(self):
        """Test scanning for valid YAML files into the registry."""
        registry = Registry(PKG_ROOT)
        registry.scan(VALID_YAML_DIR)

        expected = sum(
            1
            for f in list(VALID_YAML_DIR.rglob("*.yaml"))
            if f.is_file() and not is_inputs_yaml(f.name)
        )

        # Assertion
        assert len(registry) == expected

    def test_getitem(self):
        """Test getting an entry from the registry."""
        registry = Registry(PKG_ROOT)
        registry.scan(VALID_YAML_DIR)

        # Assertion
        for key in registry.keys():
            assert registry[key].name == key

    def test_item(self):
        """Test getting an item from the registry."""
        registry = Registry(PKG_ROOT)
        registry.scan(VALID_YAML_DIR)

        # Assertion
        for key, value in registry.items():
            assert value.name == key

    def test_getitem_invalid(self):
        """Test getting an invalid entry from the registry."""
        registry = Registry(PKG_ROOT)

        with pytest.raises(KeyError):
            _ = registry["invalid_key"]

    def test_getitem_invalid_suggestion(self):
        """Test getting an invalid entry from the registry with suggestion."""
        registry = Registry(PKG_ROOT)
        registry.scan(VALID_YAML_DIR)

        with pytest.raises(KeyError) as excinfo:
            _ = registry["ActiveInert15D"]  # See VALID_YAML_DIR

        # Assertions
        assert "Did you mean" in str(excinfo.value)
        assert "ActiveInert10D" in str(excinfo.value)

    def test_duplicate_keys(self):
        """Test that duplicate keys are not allowed."""
        registry = Registry(PKG_ROOT)
        registry.scan(VALID_YAML_DIR)

        with pytest.raises(SpecValidationError):
            # Rescan the same directory
            registry.scan(VALID_YAML_DIR)

    def test_values(self):
        """Test getting the values from the registry."""
        registry = Registry(PKG_ROOT)
        registry.scan(VALID_YAML_DIR)

        # Assertion
        for value in registry.values():
            assert isinstance(value, UQTestFunInfo)
