def ensure_open(func):
    def wrapper(self, *args, **kwargs):
        if self._closed:
            raise RuntimeError("Cache storage is closed")
        return func(self, *args, **kwargs)

    return wrapper
