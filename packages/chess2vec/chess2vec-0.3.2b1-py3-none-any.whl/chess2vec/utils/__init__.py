def convert_result(_type, **ckwargs):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            return _type(fn(*args, **kwargs), **ckwargs)

        return wrapper

    return decorator
