import functools
from typing import Callable, Any, TypeVar, Dict as t_dict
from copy import deepcopy
from .validate import validate

from ..reflection import get_python_version
if get_python_version() < (3, 9):
    from typing_extensions import ParamSpec
else:
    from builtins import dict as t_dict
    from typing import ParamSpec  # type:ignore # pylint: disable=ungrouped-imports
T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore


@validate
def memo(func: FuncT) -> FuncT:
    """decorator to memorize function calls in order to improve performance by using more memory

    Args:
        func (Callable): function to memorize
    """
    cache: t_dict[tuple, Any] = {}

    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        if (args, *kwargs.items()) not in cache:
            cache[(args, *kwargs.items())] = func(*args, **kwargs)
        return deepcopy(cache[(args, *kwargs.items())])
    return wrapper


__all__ = [
    "memo"
]
