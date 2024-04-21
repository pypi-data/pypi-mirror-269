r"""Contain some array indexing functions for nested data."""

from __future__ import annotations

__all__ = ["take_along_batch", "take_along_seq"]


from functools import partial
from typing import TYPE_CHECKING, Any, TypeVar

from batcharray import array
from batcharray.recursive import recursive_apply

if TYPE_CHECKING:
    import numpy as np

T = TypeVar("T")


def take_along_batch(data: Any, indices: np.ndarray) -> Any:
    r"""Return the arrays which index the arrays along the batch axis
    using the entries in ``indices``.

    Note:
        This function assumes the batch axis is the first
            axis of the arrays. All the arrays should have the
            same batch size.

    Args:
        data: The input data. Each item must be an array.
        indices: The 1-D array containing the indices to take.

    Returns:
        The indexed arrays along the batch axis.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from batcharray.nested import take_along_batch
    >>> arrays = {
    ...     "a": np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]),
    ...     "b": np.array([4, 3, 2, 1, 0]),
    ... }
    >>> out = take_along_batch(arrays, np.array([2, 4]))
    >>> out
    {'a': array([[4, 5], [8, 9]]), 'b': array([2, 0])}
    >>> out = take_along_batch(arrays, np.array([4, 3, 2, 1, 0]))
    >>> out
    {'a': array([[8, 9], [6, 7], [4, 5], [2, 3], [0, 1]]), 'b': array([0, 1, 2, 3, 4])}

    ```
    """
    return recursive_apply(data, partial(array.take_along_batch, indices=indices))


def take_along_seq(data: Any, indices: np.ndarray) -> Any:
    r"""Return the arrays which index the arrays along the sequence axis
    using the entries in ``indices``.

    Note:
        This function assumes the sequence axis is the second
            axis of the arrays. All the arrays should have the
            same sequence size.

    Args:
        data: The input data. Each item must be an array.
        indices: The 1-D array containing the indices to take.

    Returns:
        The indexed arrays along the sequence axis.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from batcharray.nested import take_along_seq
    >>> arrays = {'a': np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]), 'b': np.array([[4, 3, 2, 1, 0]])}
    >>> out = take_along_seq(arrays, np.array([2, 4]))
    >>> out
    {'a': array([[2, 4], [7, 9]]), 'b': array([[2, 0]])}
    >>> out = take_along_seq(arrays, np.array([4, 3, 2, 1, 0]))
    >>> out
    {'a': array([[4, 3, 2, 1, 0], [9, 8, 7, 6, 5]]), 'b': array([[0, 1, 2, 3, 4]])}

    ```
    """
    return recursive_apply(data, partial(array.take_along_seq, indices=indices))
