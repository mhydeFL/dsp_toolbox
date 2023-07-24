import logging
from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt

from dsp_toolbox.dsp.types import T
from dsp_toolbox.optimization.heuristics import ZNTuning
from dsp_toolbox.dsp.controllers.pid import PIDController
from dsp_toolbox.optimization.binary_search import (
    UBLBBinarySearch,
    BinaryHalf,
)
from dsp_toolbox.optimization.periodic_analyzer import (
    PeriodicCharacteristic,
    PeriodicAnalyzer
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


def test(
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
   
    analyzer = PeriodicAnalyzer(
        data=Tout,
        sampling_frequency_Hz=10,
        roi_threshold=setpoint
    )
    period = analyzer.calculate_period()
    
    if display:
        plt.plot(Tout, label=f"Kp:{round(kp, 3)} Ki:{round(ki, 3)} Kd:{round(kd, 3)}")
        plt.legend()
        plt.show()

    return (analyzer.check_oscillation_stability(0.2, int(period)*10), period)


def search() -> Tuple[PeriodicCharacteristic, T, T]:
    bs = UBLBBinarySearch()
    bs.generate_data(1.0, 25.0, 101)
    response = BinaryHalf.INIT
    
    iterations = 0
    while bs.data_available:
        ku_l, ku_h = bs.step(response)
        result_l, _ = test(ku_l)
        result_h, period_h = test(ku_h)
        match result_h:
            case PeriodicCharacteristic.DAMPED:
                response = BinaryHalf.UPPER
            case PeriodicCharacteristic.STABLE:
                lower_is_damped = result_l == PeriodicCharacteristic.DAMPED
                upper_is_stable = result_h == PeriodicCharacteristic.STABLE
                is_marginal = lower_is_damped and upper_is_stable
                if is_marginal:
                    break
                response = BinaryHalf.LOWER
            case PeriodicCharacteristic.UNSTABLE:
                response = BinaryHalf.LOWER
        iterations += 1

    logging.info(f"Solution found in {iterations} iterations")
    return result_h, ku_h, period_h
 

def main():
    result, ku, period = search()
    if result == PeriodicCharacteristic.STABLE:
        gains = ZNTuning(ku, period, "PI")()
        test(gains.Kp, gains.Ki, gains.Kd, display=True)
    else:
        logging.error("Could not find ultimate gain")
    

if __name__ == "__main__":
    main()
