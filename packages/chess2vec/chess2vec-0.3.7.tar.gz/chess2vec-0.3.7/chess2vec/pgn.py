from typing import TextIO

import chess.pgn


def skip(pgn: TextIO, num_of_games: int):
    """skips `num_of_games` of `pgn`"""
    n = 0

    while n < num_of_games:
        game = chess.pgn.read_game(pgn)

        if not game:
            return False

        n += 1

    return True
