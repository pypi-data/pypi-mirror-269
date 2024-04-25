import gzip
import pickle

import numpy as np

def convert_result(_type, **ckwargs):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            return _type(fn(*args, **kwargs), **ckwargs)

        return wrapper

    return decorator


def load_gzip(file):
    with gzip.open(file) as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                return


def dump_gzip(obj, file, mode, batch_size=2**12):
    with gzip.open(file, mode) as f:
        for batch in batched(obj, batch_size):
            pickle.dump(batch, f)


def batched(obj, batch_size):
    for idx in range(0, len(obj), batch_size):
        yield obj[idx : idx + batch_size]


def unbatch(obj):
    yield from (pos for game in obj for pos in game)
    

def norm_l2(a: np.ndarray) -> np.ndarray:
    """computes the l2 (euclidean) norm of the batch `a` of vectors."""
    assert a.ndim == 2
    return np.sqrt(np.sum(a**2, axis=1))


def distance_l2(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """computes the l2 (euclidean) distance between batch `a` and batch `b` of vectors."""
    return norm_l2(a - b)


def cosine(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """computes the cosine similarity between batch `a` and batch `b` of vectors."""
    return np.sum(a * b, axis=1) / (norm_l2(a) * norm_l2(b))
