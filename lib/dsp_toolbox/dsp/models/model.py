from abc import ABC
import numpy as np

from dsp_toolbox.dsp.types import T, InputType


class BaseModel(ABC):
    def update(self, u: InputType) -> np.array:
        raise RuntimeError("BaseModel not implemented")
    