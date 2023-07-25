from typing import Iterable
from dsp_toolbox.dsp.models.model import BaseModel

class FirstOrderModel(BaseModel):
    def __init__(
        self, gain: float,
        time_constant: float,
        initial_condition: float = 0.0
    ) -> None:
        super().__init__()
        self.gain = gain
        self.time_constant = time_constant
        self.initial_condition = initial_condition
        
        self.pv: Iterable = [self.initial_condition]

    def update(self, u: float) -> float:
        delta_t = 0.01
        dy_dt = (-self.pv[-1] + self.gain * u) / self.time_constant
        self.pv.append(self.pv[-1] + dy_dt * delta_t)
        return self.pv[-1]
