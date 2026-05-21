import pytest
import uqtestfuns as uqtf

from uqtestfuns.core.registry.entries import UQTestFunInfo

from conftest import assert_call


class TestListParameters:
    """All tests related to the list_parameters function."""

    def test_list_parameters(self, builtin_name: str):
        """Test calling list_parameters with a builtin function name."""
        assert_call(uqtf.list_parameters, builtin_name)

    @pytest.mark.parametrize("show", ["keywords", "all", "sets"])
    def test_list_parameters_show(self, builtin_name: str, show: str):
        """Test calling list_parameters showing keywords only."""
        assert_call(uqtf.list_parameters, builtin_name, show=show)

    def test_list_parameters_id(self, builtin_name: str, info: UQTestFunInfo):
        """Test calling list_parameters with id."""
        if info.default_parameters_id is None:
            pytest.skip("No default parameters available for this function")

        for param_id in info.available_parameters_ids:
            assert_call(
                uqtf.list_parameters,
                builtin_name,
                show="id",
                parameters_id=param_id,
            )
