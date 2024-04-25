import abc
from abc import ABC
from typing import Iterable

import chess
import chess.pgn
import numpy as np

from chess2vec import utils


class Component(ABC):
    @abc.abstractmethod
    def __call__(self, board: chess.Board): ...

    def __repr__(self) -> str:
        return f"{'.'.join((self.__module__, self.__class__.__qualname__))}()"


class MetaComponent(ABC):
    @abc.abstractmethod
    def __call__(self, game: chess.pgn.Game): ...

    def __repr__(self) -> str:
        return f"{'.'.join((self.__module__, self.__class__.__qualname__))}()"


class Composition:
    def __init__(
        self, comp: Iterable[Component] = None, meta: Iterable[MetaComponent] = None
    ) -> None:
        self.comp = tuple(comp) if comp else tuple()
        self.meta = tuple(meta) if meta else tuple()

    def compose(self, game: chess.pgn.Game):
        board = game.board()
        yield tuple(c(board) for c in self.comp)

        for move in game.mainline_moves():
            board.push(move)
            yield tuple(c(board) for c in self.comp)

    def __call__(self, game: chess.pgn.Game):
        return {
            "meta": tuple(m(game) for m in self.meta),
            "comp": tuple(self.compose(game)),
        }

    def __repr__(self) -> str:
        return f"{'.'.join((self.__module__, self.__class__.__qualname__))}(comp={self.comp}, meta={self.meta})"


class Actions(Component):
    @utils.convert_result(np.array, dtype=np.uint16)
    @utils.convert_result(list)
    def __call__(self, board):

        for move in board.legal_moves:
            pt = board.piece_type_at(move.from_square)

            if not board.turn:
                move.from_square ^= 0x38
                move.to_square ^= 0x38

            yield 64 * (64 * (pt - 1) + move.from_square) + move.to_square


class Pieces(Component):
    def __init__(self, relative=True) -> None:
        self.relative = relative
    
    @utils.convert_result(np.array, dtype=np.uint16)
    @utils.convert_result(list)
    def __call__(self, board):
        for sq in chess.scan_reversed(board.occupied):
            piece = board.piece_at(sq)

            if self.relative and not board.turn:
                sq ^= 0x38

            yield 64 * (6 * (int(board.turn) ^ piece.color) + piece.piece_type) + sq


class FEN(Component):
    def __call__(self, board) -> str:
        return board.fen()
