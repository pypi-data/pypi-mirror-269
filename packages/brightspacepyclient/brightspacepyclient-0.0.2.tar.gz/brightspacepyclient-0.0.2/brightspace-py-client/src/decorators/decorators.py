from typing import Callable, Type, TypeVar

T = TypeVar('T')


def unwrap(func: Callable[[], Type[T]]):
    def wrapper(self, *args, **kwargs):
        try:
            res = func(self, *args, **kwargs)
            return res.json()
        except:
            print("Failed to deserialize response")
    return wrapper
