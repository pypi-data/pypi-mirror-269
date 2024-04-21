from typing import Callable

import chess
import numpy as np
from scipy.sparse import csr_matrix, vstack


class vectors_builder:
    def __init__(self, vectorizer):
        self.vectorizer = vectorizer

        self.data = []
        self.rows = []
        self.columns = []

        self.rowidx = 0

    @property
    def vecsize(self):
        return self.vectorizer.size

    def add(self, board: chess.Board):
        vec_indices = list(self.vectorizer(board))

        self.rows += [self.rowidx for _ in vec_indices]
        self.columns += vec_indices
        self.data += [1 for _ in vec_indices]

        self.rowidx += 1

    def build(self):
        return vectors.from_csr(
            csr_matrix(
                (self.data, (self.rows, self.columns)),
                shape=(max(self.rows) + 1, self.vecsize),
                dtype=np.uint8,
            )
        )


class vectors(csr_matrix):
    @classmethod
    def empty(cls, vecsize: int, dtype=np.uint8):
        new = __class__((0, vecsize), dtype=dtype)
        return new

    @property
    def size(self):
        return self.shape[0]

    @property
    def vecsize(self):
        return self.shape[1]

    @classmethod
    def from_csr(cls, mat: csr_matrix):
        new = cls.__new__(cls)
        super(csr_matrix, new).__init__(
            (mat.data, mat.indices, mat.indptr), mat.shape, mat.dtype
        )
        return new

    def __iadd__(self, other):
        self = self.from_csr(vstack([self, other]))
        return self

    def __getitem__(self, key):
        return self.from_csr(super().__getitem__(key))

    def apply(
        self, f: Callable[[np.ndarray], np.ndarray], *, axis: int = 0
    ) -> csr_matrix:
        """applies the function `f` to `mat.data` along the specified axis (default 0)."""
        assert axis in (0, 1)

        if axis == 0:
            self.data = f(self.data)

        elif axis == 1:
            for row_start, row_end in zip(self.indptr[:-1], self.indptr[1:]):
                if row_end > row_start:
                    self.data[row_start:row_end] = f(self.data[row_start:row_end])

    def covs(self):
        """computes sparse covariance of `mat` (covariance of non-zero entries)."""
        mat = self.from_csr(self)
        mat.apply(lambda x: x - x.sum() / mat.vecsize, axis=1)
        return (mat @ mat.T).toarray()

    def shuffle(self, rng: np.random.Generator):
        idx = rng.permutation(self.size)
        self = self[idx]
