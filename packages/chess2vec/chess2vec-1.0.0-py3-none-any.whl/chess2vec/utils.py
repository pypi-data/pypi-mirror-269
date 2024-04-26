import gzip
import pickle
import numpy as np

from tqdm import tqdm


def lambda_wrapper(lambda_fn):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            return lambda_fn(fn(*args, **kwargs))

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


def unbatched(obj, depth=1):
    if depth == 0:
        yield from obj
        return
        
    yield from (pos for game in unbatched(obj, depth - 1) for pos in game)


def batch_generator(obj, batch_size, status=True):
    batch = []
    
    if status:
        bar = tqdm(total=batch_size)

    for item in obj:
        batch.append(item)
        
        if status:
            bar.update()

        if len(batch) == batch_size:
            yield batch
            batch.clear()

    if status:
        bar.close()
        

def arr_from_indices(indices, size, value=1, dtype=np.uint8) -> np.ndarray:
    arr = np.zeros(size, dtype=dtype)
    arr[indices] = value
    return arr
