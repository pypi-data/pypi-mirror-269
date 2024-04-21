import abc
from typing import Iterator

import chess
import numpy as np

classname = lambda obj: ".".join((obj.__class__.__module__, obj.__class__.__qualname__))


class BaseVectorizer(abc.ABC):
    @property
    @abc.abstractmethod
    def size(self) -> int: ...

    @property
    @abc.abstractmethod
    def dtype(self): ...

    @abc.abstractmethod
    def __call__(self, board: chess.Board) -> Iterator[int]: ...

    def __repr__(self) -> str:
        return f"{classname(self)}(size={self.size}, dtype={self.dtype})"


class ActionVectorizer(BaseVectorizer):
    size = 24576
    dtype = np.uint8

    def __call__(self, board: chess.Board) -> Iterator[int]:
        for move in board.legal_moves:
            pt = board.piece_type_at(move.from_square)

            if not board.turn:
                move.from_square ^= 0x38
                move.to_square ^= 0x38

            yield 64 * (64 * (pt - 1) + move.from_square) + move.to_square


class PieceVectorizer(BaseVectorizer):
    size = 768
    dtype = np.uint8

    def __call__(self, board: chess.Board) -> Iterator[int]:
        for sq in chess.scan_reversed(board.occupied):
            piece = board.piece_at(sq)

            if not board.turn:
                sq ^= 0x38

            yield 64 * (6 * (int(board.turn) ^ piece.color) + piece.piece_type) + sq


str_to_repr = {
    "action": ActionVectorizer(),
    "piece": PieceVectorizer(),
}


def convert(candidate: str | BaseVectorizer):
    if issubclass(type(candidate), BaseVectorizer):
        return candidate

    return str_to_repr[candidate]
