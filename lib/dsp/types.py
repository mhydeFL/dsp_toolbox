from typing import TypeVar, Tuple, NamedTuple


InputType = TypeVar("InputType", bound=float)
OutputType = TypeVar("OutputType", bound=float)
TimeType = TypeVar("TimeType", bound=float)
T = TypeVar("T", bound=float)
Limits = Tuple[T, T]


class PIDGains(NamedTuple):
    Kp: T = 0
    Ki: T = 0
    Kd: T = 0
