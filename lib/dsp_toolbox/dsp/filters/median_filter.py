from dsp_toolbox.dsp.types import (
    InputType,
    OutputType,
    T
)
from dsp_toolbox.dsp.filters.filter import BaseFilter


class MedianFilter(BaseFilter[InputType, OutputType]):
    def __init__(
        self,
        window_size
    ) -> None:
        super().__init__()
        self.window_size = window_size
        self.buffer = []
        self.initialized: bool = True
        self.reset()
    
    def update(
        self,
        value: T
    ) -> T:
        self.buffer.append(value)
        if len(self.buffer) > self.window_size:
            self.buffer.pop(0)
    
        sorted_buffer = sorted(self.buffer)
        median_index = len(sorted_buffer) // 2
        return sorted_buffer[median_index]
    
    def reset(self):
        self.buffer = []

    @property
    def is_initialized(self) -> bool:
        return self.initialized
