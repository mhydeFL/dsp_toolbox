import numpy as np

from dsp_toolbox.dsp.controllers.controller import BaseController
from dsp_toolbox.dsp.models.model import BaseModel

class Simulation:
    def __init__(
        self,
        controller: BaseController,
        model: BaseModel
    ) -> None:
        self.controller = controller
        self.model = model
        
    def run(self) -> np.array:
        pass
