r"""Contain some indexing functions for arrays."""

from __future__ import annotations

__all__ = ["take_along_batch", "take_along_seq"]

import numpy as np

from batcharray.constants import BATCH_AXIS, SEQ_AXIS


def take_along_batch(array: np.ndarray, indices: np.ndarray) -> np.ndarray:
    r"""Return a new array which index the input array along the batch
    axis using the entries in ``indices``.

    Note:
        This function assumes the batch axis is the first axis.

    Args:
        array: The input array.
        indices: The 1-D array containing the indices to take.

    Returns:
        The indicesed array along the batch axis.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from batcharray.array import take_along_batch
    >>> array = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
    >>> out = take_along_batch(array, np.array([2, 4]))
    >>> out
    array([[4, 5],
           [8, 9]])
    >>> out = take_along_batch(array, np.array([4, 3, 2, 1, 0]))
    >>> out
    array([[8, 9],
           [6, 7],
           [4, 5],
           [2, 3],
           [0, 1]])

    ```
    """
    return np.take(array, indices=indices, axis=BATCH_AXIS)


def take_along_seq(array: np.ndarray, indices: np.ndarray) -> np.ndarray:
    r"""Return a new array which indiceses the input array along the
    sequence axis using the entries in ``indices``.

    Note:
        This function assumes the sequence axis is the second axis.

    Args:
        array: The input array.
        indices: The 1-D array containing the indices to take.

    Returns:
        The indicesed array along the sequence axis.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from batcharray.array import take_along_seq
    >>> array = np.array([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    >>> out = take_along_seq(array, np.array([2, 4]))
    >>> out
    array([[2, 4],
           [7, 9]])
    >>> out = take_along_seq(array, np.array([4, 3, 2, 1, 0]))
    >>> out
    array([[4, 3, 2, 1, 0],
           [9, 8, 7, 6, 5]])

    ```
    """
    if indices.ndim == 1:
        return np.take(array, indices=indices, axis=SEQ_AXIS)
    batch_size, seq_len = indices.shape[:2]
    batch_indices = np.arange(batch_size).repeat(seq_len)
    indices = indices.flatten()
    return array[batch_indices, indices].reshape(batch_size, seq_len, *array.shape[2:])
