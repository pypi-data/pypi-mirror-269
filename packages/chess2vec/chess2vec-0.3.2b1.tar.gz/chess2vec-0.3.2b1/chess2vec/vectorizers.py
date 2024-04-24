import abc

import chess

from chess2vec import utils

import numpy as np


def full_classname(obj):
    return ".".join((obj.__class__.__module__, obj.__class__.__qualname__))


class BaseVectorizer(abc.ABC):
    @abc.abstractmethod
    def __call__(self, board: chess.Board): ...

    def __repr__(self) -> str:
        return f"{full_classname(self)}(size={self.size}, dtype={self.dtype})"


class ActionVectorizer(BaseVectorizer):
    @utils.convert_result(np.array, dtype=np.uint16)
    @utils.convert_result(list)
    def __call__(self, board: chess.Board):
        for move in board.legal_moves:
            pt = board.piece_type_at(move.from_square)

            if not board.turn:
                move.from_square ^= 0x38
                move.to_square ^= 0x38

            yield 64 * (64 * (pt - 1) + move.from_square) + move.to_square


class PieceVectorizer(BaseVectorizer):
    @utils.convert_result(np.array, dtype=np.uint16)
    @utils.convert_result(list)
    def __call__(self, board: chess.Board):
        for sq in chess.scan_reversed(board.occupied):
            piece = board.piece_at(sq)

            if not board.turn:
                sq ^= 0x38

            yield 64 * (6 * (int(board.turn) ^ piece.color) + piece.piece_type) + sq


class FENVectorizer(BaseVectorizer):
    def __call__(self, board: chess.Board) -> str:
        return board.fen()
