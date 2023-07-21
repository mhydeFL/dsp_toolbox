from abc import ABC, abstractmethod
from typing import Generic

from dsp.types import (
    InputType,
    OutputType
)


class BaseFilter(ABC, Generic[InputType, OutputType]):
    @abstractmethod
    def update(
        self,
        value: InputType
    ) -> OutputType:
        raise RuntimeError("Can't call base filter")
    
    @abstractmethod
    def reset(self) -> None:
        raise RuntimeError("Can't call base filter")
    
    @abstractmethod
    @property
    def is_initialized(self) -> bool:
        raise RuntimeError("Can't call base filter")