import numpy as np
from dogma_data import concatenate_numpy


def test_concatenate_numpy():
    first = np.array([1, 2, 3], dtype=np.int32)
    second = np.array([4, 5, 6], dtype=np.int32)

    res, cu = concatenate_numpy([first, second])
    np.testing.assert_equal(res, np.array([1, 2, 3, 4, 5, 6], dtype=np.int32))
    np.testing.assert_equal(cu, np.array([0, 3, 6], dtype=np.int64))