import numpy as np
import matplotlib.pyplot as plt

from dsp_toolbox.dsp.types import T
from dsp_toolbox.optimization.heuristics import ZNTuning
from dsp_toolbox.dsp.controllers.pid import PIDController
from dsp_toolbox.optimization.algorithms import (
    BinarySearch,
    BinaryHalf,
    PeriodicCharacteristic,
    find_region_of_interest,
    calculate_period,
    check_oscillation_stability
)


class TemperatureController:
    def __init__(
        self,
        controller: PIDController,
        update_interval_s: T
    ) -> None:
        self.controller = controller
        self.update_interval_s = update_interval_s
        
        self.setpoint_C = None
        self.temperature_C = None
        self.time_of_last_update = 0.0
        
    def setpoint(self, setpoint_C: T) -> None:
        self.setpoint_C = setpoint_C
        
    def update(self, temperature_C: T):
        if self.setpoint_C is None:
            return None
        now = self.time_of_last_update + self.update_interval_s

        self.time_of_last_update = now
        return self.controller.update(temperature_C, self.setpoint_C)


def search(
    kp: float,
    ki: float = 0,
    kd: float = 0,
    display: bool = False
):
    pid = PIDController(
        kp=kp,
        ki=ki,
        kd=kd,
        output_limits=[0, 5]
    )
    controller = TemperatureController(
        controller=pid,
        update_interval_s=0.1
    )
    setpoint = 28
    controller.setpoint(setpoint)
    
    Kh = 3.5
    theta_t = 22
    theta_d = 2
    Tenv = 21.5
    Ts = 0.1
    Tstop = 200
    N = int(Tstop/Ts)
    Tout = np.zeros(N+2)
    Tout[0] = 20
    e = np.zeros(N+2)
    u = np.zeros(N+2)
    for k in range(N+1):
        e[k] = controller.setpoint_C - Tout[k]
        u[k] = controller.update(Tout[k])
        Tout[k+1] = Tout[k] + (Ts/theta_t) * (-Tout[k] + Kh*u[int(k-theta_d/Ts)] + Tenv)
    
    if display:
        plt.plot(Tout, label=f"Kp:{kp} Ki:{ki} Kd:{kd}")
        plt.legend()
        plt.show()
    
    starting_idx = find_region_of_interest(Tout, setpoint)
    Tout = Tout[starting_idx:]
    period = calculate_period(Tout, 10)
    
    return (check_oscillation_stability(Tout, int(period)*10), period)
    

def main():
    bs = BinarySearch()
    bs.generate_data(3.0, 10.0, 2000)
    
    result = -10
    response = BinaryHalf.INIT
    while True:
        ku = bs.step(response)
        print(ku)
        if ku is None:
            break
        result, period = search(ku)
        
        match result:
            case PeriodicCharacteristic.DAMPED:
                response = BinaryHalf.UPPER
            case PeriodicCharacteristic.STABLE:
                break
            case PeriodicCharacteristic.UNSTABLE:
                response = BinaryHalf.LOWER

    gains = ZNTuning(ku, period, "PI")()
    search(gains.Kp, gains.Ki, gains.Kd, display=True)
    

if __name__ == "__main__":
    main()
