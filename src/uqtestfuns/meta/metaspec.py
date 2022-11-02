"""
This module contains the classes that implement specification
for a meta and the resulting test function.
"""
import math
import numpy as np
import itertools
from dataclasses import dataclass, field, InitVar
from typing import Dict, Callable, Tuple, Optional, Union, List


__all__ = ["UQMetaFunSpec", "UQTestFunSpec"]


def _preprocess_effects(
    effects_dict: Dict[int, Optional[int]], spatial_dimension: int
) -> Dict[int, int]:
    """Preprocess the effects dictionary.

    It will do the following things:
    - If a value is None, replace it with the number of all possible interaction
      terms.
    - If a value is larger than the dimension of the test function or it's zero
      exclude the key.

    >>> effects_dict = {1: None, 2: 3, 3: None, 4: 10}
    >>> spatial_dimension = 3
    >>> _preprocess_effects(effects_dict, spatial_dimension)
    {1: 3, 2: 3, 3: 1}

    Parameters
    ----------
    effects_dict : Dict[int, Optional[int]]
        Specified effects with the corresponding length to take into account in
        a realization of test function.
    spatial_dimension : int
        Number of dimensions of the test function.

    Returns
    -------
    Dict[int, int]
        Cleaned-up specified effects.
    """
    effects = dict()

    for key in list(effects_dict):
        if key <= spatial_dimension and effects_dict[key] != 0:
            if effects_dict[key] is None:
                effects[key] = math.comb(spatial_dimension, key)
            else:
                effects[key] = effects_dict[key]  # type: ignore

    return effects


def _select_basis(spatial_dimension: int, num_basis: int) -> Tuple[int, ...]:
    """Select basis of a certain length from a selection of basis.

    For example, with spatial dimension of 3 and number of basis functions of 9,
    the output may be a tuple of integers: (7, 3, 8) which means the first,
    second, and third dimension has the 7th, 3rd, and 8th basis function,
    respectively.

    Parameters
    ----------
    spatial_dimension : int
        Number of dimensions of the test function.
    num_basis : int
        Number of available basis functions to select from.

    Returns
    -------
    Tuple[int, ...]
        Selected basis function in each dimension.
    """
    selection = tuple(np.random.randint(0, num_basis, size=spatial_dimension))

    return selection


def _create_effects_tuples(
    spatial_dimension: int, effects_dict: Dict[int, int]
) -> Dict[int, Tuple[Tuple[int, ...], ...]]:
    """Create a dictionary of effect matrices.

    >>> spatial_dimension = 3
    >>> effects_dict = {1: None, 2: None, 3: None}
    >>> _create_effects_tuples(spatial_dimension, effects_dict)
    {1: ((0,), (1,), (2,)), 2: ((0, 1), (0, 2), (1, 2)), 3: ((0, 1, 2),)}
    >>> effects_dict = {}
    >>> _create_effects_tuples(spatial_dimension, effects_dict)
    {}
    >>> effects_dict = {1: 0, 2: None, 3: 0}
    >>> _create_effects_tuples(spatial_dimension, effects_dict)
    {2: ((0, 1), (0, 2), (1, 2))}
    >>> effects_dict = {5: None}
    >>> _create_effects_tuples(spatial_dimension, effects_dict)
    {}

    Parameters
    ----------
    spatial_dimension : int
        Number of dimensions of the test function.
    effects_dict : Dict[int, int]
        Specified effects to take into account.

    Returns
    -------
    Dict[int, Tuple[Tuple[int, ...], ...]]
        Effects tuples for each n-way interaction as specified in the effects.

    Notes
    -----
    - If an effect has a value of 0 then no effect is taken into account.
    - If an effect is larger than the spatial dimension of the test function
      then no effect is taken into account.
    """
    effects_tuples = dict()

    for key in effects_dict:
        if (
            effects_dict[key] != 0 and key <= spatial_dimension
        ):  # pragma: no cover
            effects_tuples[key] = tuple(
                itertools.combinations(np.arange(spatial_dimension), key)
            )

    return effects_tuples


def _select_effects(
    all_effects: Dict[int, Tuple[Tuple[int, ...], ...]],
    effects_dict: Dict[int, int],
) -> Dict[int, Tuple[Tuple[int, ...], ...]]:
    """Randomly select effects from all possible terms.

    Parameters
    ----------
    all_effects : Dict[int, Tuple[Tuple[int, ...], ...]]
        Effects tuples for each n-way interaction as specified in the effects.
    effects_dict : Dict[int, int]
        Specified effects with the corresponding length to take into account in
        a realization of test function.

    Returns
    -------
    Dict[int, Tuple[Tuple[int, ...], ...]]
        Selected interaction terms for each n-way interactions.
    """
    selected_effects = dict()

    for key in effects_dict:
        length = effects_dict[key]

        if length == len(all_effects[key]):
            # Take all
            selected_effects[key] = all_effects[key]
        else:
            # Randomly select the interaction tuples
            idx = np.random.choice(
                len(all_effects[key]), length, replace=False
            )
            selected_effects[key] = tuple([all_effects[key][i] for i in idx])

    return selected_effects


def _generate_effect_coeffs(
    coeffs_gen: Callable, effects_dict: Dict[int, int]
) -> Dict[int, np.ndarray]:
    """Generate the coefficient values for each effect term.

    Parameters
    ----------
    coeffs_gen : Callable
        Function to generate the coefficient values for each effect term.
    effects_dict : Dict[int, int]
        Specified effects with the corresponding length to take into account in
        a realization of test function.

    Returns
    -------
    Dict[int, np.ndarray]
        The coefficient values of each effect term.
    """
    coeffs = dict()

    for key in effects_dict:
        coeffs[key] = coeffs_gen(effects_dict[key])

    return coeffs


def _select_inputs(
    inputs: Union[List[Dict], Tuple[Dict, ...]], spatial_dimension: int
) -> Union[List[Dict], Tuple[Dict, ...]]:
    """Randomly select marginals of a given dimension from a set of inputs.

    Parameters
    ----------
    inputs : Union[List[Dict], Tuple[Dict, ...]]
        List of available marginals to construct a probabilistic input model for
        a test function realization.
    spatial_dimension : int
        Number of dimensions of the test function.

    Returns
    -------
    Union[List[Dict], Tuple[Dict, ...]]
        List of selected marginals to construct a probabilistic input model of
        the given dimension for a test function realization.
    """
    inputs_list = []
    indices = np.random.randint(
        low=0, high=len(inputs), size=spatial_dimension
    )

    for num, idx in enumerate(indices):
        # Create an independent copy to avoid unintended mutation
        selected_input = inputs[idx].copy()
        # Provide default name if not provided
        if selected_input.get("name", None) is None:
            selected_input["name"] = f"X{num}"

        inputs_list.append(selected_input)

    return inputs_list


@dataclass(frozen=True)
class UQTestFunSpec:
    """Specification class for a test function realization.

    An instance of UQTestFunSpec can be used to create a realization of test
    function from a fully-specified meta.

    Parameters
    ----------
    spatial_dimension : int
        Number of dimension of the test function.
    basis_functions : Dict[int, Callable]
        Collection of basis functions to choose from.
    selected_basis : Tuple[int, ...]
        Selected basis functions to construct the test function.
    effects_tuples : Dict[int, Tuple[Tuple[int, ...], ...]]
        Tuples that codify cross-terms between basis functions
        of each dimension that represents interaction terms
        in the test function.
    effects_coeffs : Dict[int, np.ndarray]
        Coefficients that appear in each of the terms in the test function.
    inputs : Union[List[Dict], Tuple[Dict, ...]]
        Input marginals to construct a multi-dimensional probabilistic input of
        the test function.
    """

    spatial_dimension: int
    basis_functions: Dict[int, Callable]
    selected_basis: Tuple[int, ...]
    effects_tuples: Dict[int, Tuple[Tuple[int, ...], ...]]
    effects_coeffs: Dict[int, np.ndarray]
    inputs: Union[List[Dict], Tuple[Dict, ...]]


@dataclass
class UQMetaFunSpec:
    """Specification class for a meta.

    Parameters
    ----------
    spatial_dimension : int
        Number of dimension of the generated test functions.
    basis_functions : Dict[int, Callable]
        Collection of basis functions to choose from.
    effects : Dict[int, Optional[int]]
        Specified effects with the corresponding length to take into account for
        all the test function realizations.
    inputs : Union[List[Dict], Tuple[Dict, ...]]
        List of available input marginals to construct a multi-dimensional
        probabilistic input of the test function realizations.
    coeffs_generator : Callable
        Function to generate the coefficient values for each effect term.
    """

    spatial_dimension: int
    basis_functions: Dict[int, Callable]
    effects: Dict[int, int] = field(init=False)
    effects_dict: InitVar[Dict[int, Optional[int]]]
    inputs: Union[List[Dict], Tuple[Dict, ...]]
    coeffs_generator: Callable
    _effects_tuples: Optional[Dict[int, Tuple[Tuple[int, ...], ...]]] = field(
        init=False, repr=False
    )

    def __post_init__(self, effects_dict):
        if self.spatial_dimension < 1:
            raise ValueError(
                f"Spatial dimension must be > 0! "
                f"Got {self.spatial_dimension}"
            )
        self._effects_tuples = None
        # Clean up the effects dictionary
        self.effects = _preprocess_effects(
            effects_dict, self.spatial_dimension
        )

    def get_sample(
        self, sample_size: int = 1
    ) -> Optional[Union[UQTestFunSpec, List[UQTestFunSpec]]]:
        """Get realizations of UQTestFunSpec.

        Parameters
        ----------
        sample_size : int, Optional
            Number of realizations.

        Returns
        -------
        Optional[Union[UQTestFunSpec, List[UQTestFunSpec]]]
            Realization(s) of UQTestFunSpec.

        Notes
        -----
        - An instance of UQTestFunSpec is used to construct a realization
          of a test function from the given meta.
        - With sample_size larger than one, a list of UQTestFunSpec instances
          is returned.
        """

        if sample_size < 1:
            return None

        # Generate all possible requested interactions and cache them
        if self._effects_tuples is None:
            self._effects_tuples = _create_effects_tuples(
                self.spatial_dimension, self.effects
            )

        sample = []
        for _ in range(sample_size):

            # Randomly select basis
            num_basis = len(self.basis_functions)
            selected_basis = _select_basis(self.spatial_dimension, num_basis)

            # Randomly select tuples of interaction terms
            effects_tuples = _select_effects(
                self._effects_tuples, self.effects
            )

            # Randomly generate the coefficients for all terms
            effects_coeffs = _generate_effect_coeffs(
                self.coeffs_generator, self.effects
            )

            # Randomly select input marginals and create an instance
            inputs = _select_inputs(self.inputs, self.spatial_dimension)

            # Create an instance of UQTestFunSpec
            uqtestfun_spec = UQTestFunSpec(
                self.spatial_dimension,
                self.basis_functions,
                selected_basis,
                effects_tuples,
                effects_coeffs,
                inputs,
            )

            sample.append(uqtestfun_spec)

        if sample_size == 1:
            return sample[0]
        else:
            return sample


if __name__ == "__main__":  # pragma: no cover
    import doctest

    doctest.testmod()
