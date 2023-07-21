from dsp_toolbox.dsp.types import T
from dsp_toolbox.dsp.controllers.pid import PIDController
from dsp_toolbox.dsp.filters.exponential_filter import ExponentialFilter

import matplotlib.pyplot as plt


class TemperatureController:
    def __init__(
        self,
        controller: PIDController,
        filter: ExponentialFilter,
        update_interval_s: T
    ) -> None:
        self.controller = controller
        self.filter = filter
        self.update_interval_s = update_interval_s
        
        self.setpoint_C = None
        self.filtered_temperature_C = None
        self.time_of_last_update = 0.0
        
    def setpoint(self, setpoint_C: T) -> None:
        self.setpoint_C = setpoint_C
        
    def update(self, temperature_C: T):
        if self.setpoint_C is None:
            return None
        now = self.time_of_last_update + self.update_interval_s

        self.time_of_last_update = now
        self.filtered_temperature_C = self.filter.update(temperature_C)
        return self.controller.update(self.filtered_temperature_C, self.setpoint_C)
    

class HeaterModel:
    def __init__(
        self,
        heater_gain: T = 3.5,
        time_constant: T = 22,
        time_delay: T = 2,
        ambient_temperature: T = 21.5,
        sample_time = 0.1,
        initial_temp: T = 0.0
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
    # Air Heater System
    import numpy as np
    import matplotlib.pyplot as plt
    # Model Parameters
    Kh = 3.5
    theta_t = 22
    theta_d = 2
    Tenv = 21.5
    # Simulation Parameters
    Ts = 0.1 # Sampling Time
    Tstop = 200 # End of Simulation Time
    N = int(Tstop/Ts) # Simulation length
    Tout = np.zeros(N+2) # Initialization the Tout vector
    Tout[0] = 20 # Initial Vaue
    # PI Controller Settings
    Kp = 1
    Ti = 30
    r = 28 # Reference value [degC]
    e = np.zeros(N+2) # Initialization
    u = np.zeros(N+2) # Initialization
    t = np.arange(0,Tstop+2*Ts,Ts) #Create the Time Series
    # Simulation
    for k in range(N+1):
        # Controller
        e[k] = r - Tout[k]
        u[k] = u[k-1] + Kp*(e[k] - e[k-1]) + (Kp/Ti)*e[k] #PI Controller
        if u[k]>5:
            u[k] = 5
        # Process Model
        Tout[k+1] = Tout[k] + (Ts/theta_t) * (-Tout[k] + Kh*u[int(k-theta_d/Ts)] + Tenv)
        print("t = %2.1f, u = %3.2f, Tout = %3.1f" %(t[k], u[k], Tout[k+1]))
    plt.plot(Tout)
    plt.show()


if __name__ == "__main__":
    main()
