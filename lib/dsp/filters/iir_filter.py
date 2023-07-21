from typing import Tuple, Iterable, Optional

from dsp.types import (
    InputType,
    OutputType,
    T
)
from dsp.filters.filter import BaseFilter


class IIRFilter(BaseFilter[InputType, OutputType]):
    def __init__(
        self,
        m_a,
        m_b,
        order=1,
        initial_value=None
    ) -> None:
        super().__init__()
        self.buffer: Iterable[Tuple(T, T)]
        self.m_a: Iterable[T] = m_a
        self.m_b: Iterable[T] = m_b
        self.order: int = order
        self.ncoeffs = self.order + 1
        self.initialized: bool = False
        self.initial_value: Optional[T] = initial_value
        self.reset()
        
    def update(self, value: T) -> T:
        if not self.is_initialized:
            self.initializeBuffer(value)
            
        sum_x = 0.0
        sum_y = 0.0
        coeffIdx = 1
        
        for item in self.buffer:
            sum_x += self.m_b[coeffIdx] * item[0]
            sum_y -= self.m_a[coeffIdx] * item[1]
            coeffIdx += 1
            
        y = self.m_b[0] * value + sum_x + sum_y
        self.push_xy(value, y)
        return y
    
    def reset(self):
        self.initialized = False
        if self.initial_value:
            self.initializeBuffer(self.initial_value)
    
    def push_xy(
        self,
        x: T,
        y: T
    ) -> None:
        self.buffer.insert(0, [x, y])
        self.buffer.pop()
    
    def initializeBuffer(
        self,
        value: T
    ) -> None:
        self.buffer = []
        for _ in range(self.order):
            self.buffer.append([value, value])
        self.initialized = True       

    @property
    def is_initialized(self) -> bool:
        return self.initialized
    