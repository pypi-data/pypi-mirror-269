import numpy as np
import chess
from chess2vec import utils


def create_triplets(games):
    rng = np.random.default_rng(42)
    rng.shuffle(games)

    for game, next_game in zip(games[:-1], games[1:]):
        for pos, next_pos in zip(game[:-1], game[1:]):
            yield pos, next_pos, rng.choice(next_game)


@utils.lambda_wrapper(lambda x: np.array(tuple(x), dtype=np.uint16))
def actions(board):
    for move in board.legal_moves:
        pt = board.piece_type_at(move.from_square)

        if not board.turn:
            move.from_square ^= 0x38
            move.to_square ^= 0x38

        yield 64 * (64 * (pt - 1) + move.from_square) + move.to_square


@utils.lambda_wrapper(lambda x: np.array(tuple(x), dtype=np.uint16))
def pieces(board):
    for sq in chess.scan_reversed(board.occupied):
        piece = board.piece_at(sq)

        if not board.turn:
            sq ^= 0x38

        yield 64 * (6 * (int(board.turn) ^ piece.color) + piece.piece_type) + sq


def fen(board):
    return board.fen()
