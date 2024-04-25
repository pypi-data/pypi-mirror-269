from typing import TextIO

import chess
import chess.pgn
from tqdm import tqdm

from chess2vec import components, utils


class Loader:
    def __init__(self, composition: components.Composition) -> None:
        self.composition = composition
        self.data = []

    @property
    def size(self) -> int:
        return len(self.data)

    def __len__(self) -> int:
        return self.size

    def load_pgn(self, pgn: TextIO, n_games: int = None, status: bool = False) -> bool:
        if n_games is None:
            n_games = float("inf")

        if status:
            bar = tqdm(total=n_games)

        n = 0

        while n < n_games:
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
        return tuple(g["meta"] for g in self.data)

    @property
    def comp(self):
        return tuple(g["comp"] for g in self.data)

    def batched(self, batch_size):
        yield from utils.batched(self.data, batch_size)

    def save(self, file: str, new: bool = True, batch_size=2**16) -> None:
        mode = "wb" if new else "ab"
        utils.dump_gzip(self.data, file, mode, batch_size)

    def load_gzip(self, file: str) -> None:
        self.data += list(utils.load_gzip(file))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(composition={self.composition}, size={self.size})"
