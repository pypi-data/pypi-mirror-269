import gzip
import pickle


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


def dump_gzip(obj, file, mode, batch_size=2**16):
    with gzip.open(file, mode) as f:
        for batch in batched(obj, batch_size):
            pickle.dump(batch, f)


def batched(obj, batch_size):
    for idx in range(0, len(obj), batch_size):
        yield obj[idx : idx + batch_size]
