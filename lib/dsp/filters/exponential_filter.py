from typing import Optional

from dsp.types import (
    InputType,
    OutputType,
    T
)
from dsp.filters.filter import BaseFilter


class ExponentialFilter(BaseFilter[InputType, OutputType]):
    def __init__(
        self,
        alpha: float
    ) -> None:
        super().__init__()
        self.buffer: T
        self.alpha: T = alpha
        self.initialized: bool = False
        self.initial_value: Optional[T] = None
        self.reset()
        
    def update(
        self,
        value: T
    ) -> T:
        if not self.initialized:
            self.buffer = value
            self.initialized = True
            return value
        ret = (self.alpha * value) + ((1 - self.alpha) * self.buffer)
        self.buffer = ret
        return ret
    
    def reset(self):
        self.buffer = 0
        self.initialized = False
    
    @property
    def is_initialized(self) -> bool:
        return self.initialized