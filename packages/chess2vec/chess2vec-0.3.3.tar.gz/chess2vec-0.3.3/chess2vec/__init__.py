import pickle
from typing import Iterable, TextIO

import chess
import chess.pgn
from tqdm import tqdm

from chess2vec import components


class Loader:
    def __init__(self, composition: components.Composition) -> None:
        self.composition = composition
        self.data = []

    @property
    def size(self) -> int:
        return len(self.data)

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

            self.data.append(self.composition(game))

            if status:
                bar.update(1)

            n += 1

        if status:
            bar.close()

        return True

    def __getitem__(self, idx):
        return self.data[idx]
    
    @property
    def meta(self):
        return tuple(g['meta'] for g in self.data)
    
    @property
    def comp(self):
        return tuple(g['comp'] for g in self.data)
    
    def batched(self, batch_size):
        for idx in range(0, self.size, batch_size):
            yield self.data[idx : idx + batch_size]

    def save(self, file: str, *, batch_size=2**20) -> None:
        with open(file, "wb") as f:
            for batch in self.batched(batch_size):
                pickle.dump(batch, f)

    def load(self, file: str) -> None:
        with open(file, "rb") as f:
            while True:
                try:
                    self.data += pickle.load(f)

                except EOFError:
                    return

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(composition={self.composition}, size={self.size})"
