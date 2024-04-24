def convert_return(dtype):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            return dtype(fn(*args, **kwargs))

        return wrapper

    return decorator
