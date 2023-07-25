from typing import Iterable

from dsp_toolbox.dsp.types import T
from dsp_toolbox.dsp.controllers.controller import BaseController
from dsp_toolbox.dsp.models.model import BaseModel

class Simulation:
    def __init__(
        self,
        controller: BaseController,
        model: BaseModel,
        setpoint: T
    ) -> None:
        self.controller = controller
        self.model = model
        self.setpoint = setpoint
        
    def run(self, num_samples: int) -> Iterable:
        for i in range(num_samples):
            u = self.controller.update(self.model.pv[i], self.setpoint)
            self.model.update(u)
            
        return self.model.pv
            
