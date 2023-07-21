from abc import ABC, abstractmethod
from typing import Generic, Optional, Tuple, TypeVar


InputType = TypeVar("InputType", bound=float)
OutputType = TypeVar("OutputType", bound=float)
TimeType = TypeVar("TimeType", bound=float)
T = TypeVar("T", bound=float)
Limits = Tuple[T, T]


class BaseController(ABC, Generic[InputType, OutputType, TimeType]):
    """An abstract base class for controllers to implement

    This is modeled after Common/General/DSP/Controllers/I_Controller.h.

    See the documentation for child classes for example usage.
    """

    @abstractmethod
    def reset(self) -> None:
        """Reset the controller to its initial state

        The previous and summed errors are cleared. When the next update arrives, the
        controller will act as if it was freshly constructed.
        """
        raise RuntimeError("Can't call base controller")

    @abstractmethod
    def __call__(
        self,
        value: InputType,
        setpoint: InputType,
        t: Optional[TimeType] = None,
    ) -> OutputType:
        """Compute a new output given a fresh input and the set point

        t represents the current time. If not specified, time.monotonic() is used.
        """
        raise RuntimeError("Can't call base controller")

    def update(
        self,
        value: InputType,
        setpoint: InputType,
        t: Optional[TimeType] = None,
    ) -> OutputType:
        """Alias for __call__()"""
        return self(value=value, setpoint=setpoint, t=t)

    @staticmethod
    def limit(value: T, limits: Optional[Limits[T]]) -> T:
        """Clamp the value to an optional range

        If limits is None, the input value is returned unchanged.
        Otherwise, limits must be a (low, high) pair defining the allowble range that
        the output must fall within.
        """
        if limits is None:
            return value
        return min(max(value, limits[0]), limits[1])
