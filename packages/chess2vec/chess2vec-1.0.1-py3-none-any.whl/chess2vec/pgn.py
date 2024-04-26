from typing import Any, Callable

import chess
import chess.pgn


def composition_wrapper(*fn: Callable[[chess.Board], Any]):
    def wrapper(game):
        board = game.board()
        yield list(f(board) for f in fn)

        for move in game.mainline_moves():
            board.push(move)
            yield list(f(board) for f in fn)

    return wrapper


def load_pgn(file: str, composition: Callable[[chess.pgn.Game], Any]):
    pgn = open(file)
    game = chess.pgn.read_game(pgn)

    while game:
        yield list(composition(game))
        game = chess.pgn.read_game(pgn)
