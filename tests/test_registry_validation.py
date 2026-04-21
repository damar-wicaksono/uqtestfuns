"""
Test module for registry validation functionality.
"""

import pytest

from uqtestfuns.core.registry.validation import (
    SpecValidationError,
    validate_marginal,
)


class TestMarginalValidation:
    """All tests related to registry validation."""

    def test_minimal_specification(self):
        """Test that mandatory keys are present in the registry."""
        marginal = {
            "distribution": "normal",
            "parameters": [0.0, 1.0],
        }

        # Raise no exception
        validate_marginal(marginal)

    def test_full_specification(self):
        """Test that all keys are present in the registry."""
        marginal = {
            "name": "X",
            "distribution": "normal",
            "parameters": [0.0, 1.0],
            "description": "A normal distribution",
        }

        # Raise no exception
        validate_marginal(marginal)

    @pytest.mark.parametrize("missing_key", ["distribution", "parameters"])
    def test_missing_key(self, missing_key):
        """Test that mandatory keys are missing."""
        marginal = {
            "name": "X",
            "distribution": "normal",
            "parameters": [0.0, 1.0],
            "description": "A normal distribution",
        }
        _ = marginal.pop(missing_key)

        with pytest.raises(SpecValidationError, match=missing_key):
            validate_marginal(marginal)

    def test_extra_key(self):
        """Test that an extra key is present."""
        marginal = {
            "name": "X",
            "distribution": "normal",
            "parameters": [0.0, 1.0],
            "description": "A normal distribution",
            "repeat": 4,
        }

        with pytest.raises(SpecValidationError, match="repeat"):
            validate_marginal(marginal)

    def test_empty_margina(self):
        """Test that an empty dictionary is not valid."""
        with pytest.raises(SpecValidationError):
            validate_marginal({})
