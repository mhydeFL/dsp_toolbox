from typing import TypeVar, Tuple


InputType = TypeVar("InputType", bound=float)
OutputType = TypeVar("OutputType", bound=float)
TimeType = TypeVar("TimeType", bound=float)
T = TypeVar("T", bound=float)
Limits = Tuple[T, T]
