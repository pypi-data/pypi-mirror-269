from typing import Iterable, TextIO

import chess
import chess.pgn
from tqdm import tqdm

import pickle

from chess2vec import vectorizers as _vec


class PositionLoader:
    def __init__(self, vectorizers: Iterable[_vec.BaseVectorizer]) -> None:
        self.vectorizers = vectorizers
        self.data = []
        self.game_id = 0

    @property
    def size(self) -> int:
        return len(self.data)

    def add(self, board: chess.Board) -> None:
        self.data.append([v(board) for v in self.vectorizers] + [self.game_id])
        self.game_id += 1

    def load_pgn(
        self, pgn: TextIO, num_of_games: int = None, status: bool = False
    ) -> bool:
        if num_of_games is None:
            num_of_games = float("inf")

        if status:
            bar = tqdm(total=num_of_games)

        n = 0

        while n < num_of_games:
            game = chess.pgn.read_game(pgn)

            if not game:
                return False

            board = game.board()
            self.add(board)

            for move in game.mainline_moves():
                board.push(move)
                self.add(board)

            if status:
                bar.update(1)

            n += 1

        if status:
            bar.close()

        return True

    def get_position(self, idx):
        return self.data[idx]

    def get_vector(self, idx):
        return list(zip(*self.data))[idx]

    def batched(self, batch_size: int):
        for idx in range(0, self.size, batch_size):
            yield self.data[idx : idx + batch_size]

    def save_raw(self, file: str, *, batch_size=2**20) -> None:
        with open(file, 'ab') as f:
            for batch in self.batched(batch_size):
                pickle.dump(batch, f)

    def load(self, file: str) -> None:
        with open(file, 'rb') as f:
            self.data += pickle.load(f)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(size={self.size}, vectorizers={self.vectorizers})"
