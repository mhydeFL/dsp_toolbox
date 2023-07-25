from typing import Iterable
from dsp_toolbox.dsp.models.model import BaseModel


class SecondOrderModel(BaseModel):
    def __init__(
        self,
        natural_frequency: float,
        damping_ratio: float,
        initial_condition: float = 0.0
    ) -> None:
        super().__init__()
        self.natural_frequency = natural_frequency
        self.damping_ratio = damping_ratio
        self.initial_condition = initial_condition
        self.prev_error = 0.0
        
        self.pv: Iterable = [self.initial_condition]

    def update(self, u: float) -> float:
        delta_t = 0.01
        error = u - self.pv[-1]
        dy_dt = (
            -2 * self.damping_ratio * self.natural_frequency * self.prev_error
            - self.natural_frequency ** 2 * (self.pv[-1] - u)
        )
        self.prev_error = error
        self.pv.append(self.pv[-1] + dy_dt * delta_t)
        return self.pv[-1]
