from dsp_toolbox.dsp.types import T
from dsp_toolbox.dsp.controllers.pid import PIDController
from dsp_toolbox.dsp.filters.exponential_filter import ExponentialFilter

import numpy as np
import matplotlib.pyplot as plt


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
    

class HeaterModel:
    def __init__(
        self,
        heater_gain: T,
        time_constant: T,
        time_delay: T,
        ambient_temperature: T,
        sample_time,
        initial_temp
    ) -> None:
        self.Kh = heater_gain
        self.theta_t = time_constant
        self.theta_d = time_delay
        self.Tenv = ambient_temperature
        self.Ts = sample_time
        self.initial_temp = initial_temp
        self.prev_temp = initial_temp

    def update(self, u: T) -> T:
        temp = self.prev_temp + (self.Ts/self.theta_t) * (-self.prev_temp + self.Kh*u + self.Tenv)
        self.prev_temp = temp
        return temp


def main():
    from dsp_toolbox.optimization.oscillation_checker import calculate_period, check_oscillation_stability, find_region_of_interest
    pid = PIDController(
        kp=4.2,
        ki=0.0,
        kd=0.0,
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
    t = np.arange(0,Tstop+2*Ts,Ts)
    for k in range(N+1):
        print(Tout[k])
        e[k] = controller.setpoint_C - Tout[k]
        u[k] = controller.update(Tout[k], )
        Tout[k+1] = Tout[k] + (Ts/theta_t) * (-Tout[k] + Kh*u[int(k-theta_d/Ts)] + Tenv)
        print("t = %2.1f, u = %3.2f, Tout = %3.1f" %(t[k], u[k], Tout[k+1]))
    
    plt.plot(Tout)
    plt.show()
    
    starting_idx = find_region_of_interest(Tout, setpoint)
    Tout = Tout[starting_idx:]
    period = calculate_period(Tout, 10)
    print(period)
    print(check_oscillation_stability(Tout, int(period)*10))
    


if __name__ == "__main__":
    main()
