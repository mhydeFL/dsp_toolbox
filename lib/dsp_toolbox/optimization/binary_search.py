from typing import Optional, Tuple
from enum import IntEnum, unique
import numpy as np

from dsp_toolbox.dsp.types import T


@unique
class BinaryHalf(IntEnum):
    INIT = 0
    LOWER = 1
    UPPER = 2
 

class BinarySearch:
    def __init__(
        self,
        data: Optional[np.array] = None
    ) -> None:
        self.data: np.array = data
        self.low_idx: int = 0
        self.mid_idx: int = 0
        if self.data:
            self.data.sort()
            self.high_idx: int = self.data.size()

    def step(self, reduce: BinaryHalf) -> T:
        match reduce:
            case BinaryHalf.INIT:
                pass
            case BinaryHalf.LOWER:
                self.high_idx = self.mid_idx
            case BinaryHalf.UPPER:
                self.low_idx = self.mid_idx
        self.mid_idx = (self.low_idx + self.high_idx) // 2
        return self.data[self.mid_idx]
    
    def generate_data(self, min: T, max: T, resolution: T) -> None:
        self.data = np.linspace(min, max, resolution)
        self.configure_data()
    
    def configure_data(self) -> None:
        self.data.sort()
        self.high_idx = self.data.size
        
    @property
    def data_available(self) -> bool:
        return self.high_idx > self.low_idx + 1
    

class UBLBBinarySearch(BinarySearch):
    """
    Upper-Bound Lower-Bound Binary Search Algorithm to
    find adjacent indexes where the upper satisfies a
    condition but the lower does not
    """
    def __init__(
        self,
        data: Optional[np.array] = None
    ) -> None:
        super().__init__(data)
        
    def step(self, reduce: BinaryHalf) -> Tuple[T]:
        match reduce:
            case BinaryHalf.INIT:
                pass
            case BinaryHalf.LOWER:
                self.high_idx = self.mid_idx
            case BinaryHalf.UPPER:
                self.low_idx = self.mid_idx
        self.mid_idx = (self.low_idx + self.high_idx) // 2
        return (self.data[self.mid_idx-1], self.data[self.mid_idx])
