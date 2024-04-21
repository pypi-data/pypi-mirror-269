import abc
import itertools
from typing import Iterable, Iterator, Self, TextIO

import chess
import chess.pgn
import numpy as np
from tqdm import tqdm

from chess2vec import vectorizers
from chess2vec.utils import sparse
from chess2vec.vectorizers import ActionVectorizer, PieceVectorizer


class BaseLoader(abc.ABC):
    def __init__(self, vectorizer) -> None:
        self.vectorizer = vectorizers.convert(vectorizer)
        self.init_entries()

    def init_entries(self) -> None:
        self.entries = sparse.vectors.empty(self.vectorizer.size, self.vectorizer.dtype)

    @property
    def size(self) -> int:
        return self.entries.size

    @property
    def vecsize(self) -> int:
        return self.entries.vecsize

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(size={self.size}, vectorizer={self.vectorizer})"
        )


class PositionLoader(BaseLoader):
    def __init__(self, vectorizer, *, with_fen=False):
        super().__init__(vectorizer)

        self.with_fen = with_fen

        if self.with_fen:
            self.labels = []

    @property
    def vecsize(self) -> int:
        return self.entries.vecsize

    @property
    def size(self) -> int:
        return self.entries.size

    def load_pgn(self, x: TextIO, games: int = None, status: bool = False):
        if games is None:
            games = float("inf")

        builder = sparse.vectors_builder(self.vectorizer)
        num_game = 0

        if status:
            bar = tqdm(total=games)

        game = chess.pgn.read_game(x)

        while game and num_game < games:
            board = game.board()

            for move in itertools.chain(game.mainline_moves(), (chess.Move.null(),)):
                builder.add(board)

                if self.with_fen:
                    self.labels.append(board.fen())

                board.push(move)

            if status:
                bar.update(1)

            game = chess.pgn.read_game(x)
            num_game += 1

        self.entries += builder.build()

        if status:
            bar.close()

    def save(self, file: str) -> None:
        """saves the already loaded data to a compressed .npz file."""
        _save_dict = {}
        _save_dict.update(
            indices=self.entries.indices,
            indptr=self.entries.indptr,
            data=self.entries.data,
        )

        if self.with_fen:
            _save_dict.update(labels=self.labels)

        np.savez_compressed(file, **_save_dict)

    def load_npz(self, x: Iterable[str]):
        """loads data from .npz file"""
        for file in x:
            with np.load(file) as loaded:
                self.entries += sparse.vectors(
                    self.vecsize,
                    self.vectorizer.dtype,
                    (
                        loaded["data"],
                        loaded["indices"],
                        loaded["indptr"],
                    ),
                )

                if self.with_fen:
                    self.labels += loaded["labels"]

    def batched(self, batch_size: int) -> Iterator[Self]:
        for idx in range(0, self.size, batch_size):
            child = self.__class__(self.vectorizer, with_fen=self.with_fen)

            child.entries = self.entries[idx : idx + batch_size]
            child.labels = self.labels[idx : idx + batch_size]

            yield child

    def shuffle(self, *, seed: int = 42):
        rng = np.random.default_rng(seed)
        idx = rng.permutation(self.size)

        self.entries = self.entries[idx]

        if self.with_fen:
            self.labels = list(np.array(self.labels)[idx])

    def sample(self, sample_size: int | float, *, seed: int = 42):
        if isinstance(sample_size, float):
            sample_size = self.size * sample_size

        sample = self.__class__(self.vectorizer, with_fen=self.with_fen)

        rng = np.random.default_rng(seed)
        idx = rng.permutation(sample_size)

        sample.entries = self.entries[idx]

        if self.with_fen:
            sample.append_labels(list(np.array(self.labels)[idx]))

        return sample

    def cov(self) -> np.ndarray:
        return sparse.covs(self.entries.T).toarray()

    def __add__(self, item):
        assert isinstance(item, type(self))

        new = self.__class__(self.vectorizer, with_fen=self.with_fen)

        new.entries += self.entries
        new.entries += item.entries

        if self.with_fen:
            new.labels = self.labels + item.labels

        return new
