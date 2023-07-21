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
        step_response: T = 1,
        initial_temp: T = 0.0
    ) -> None:
        self.Kh = heater_gain
        self.theta_t = time_constant
        self.theta_d = time_delay
        self.Tenv = ambient_temperature
        self.Ts = sample_time
        self.uk = step_response
        self.prev_temp = initial_temp

    def update(self) -> T:
        temp = self.prev_temp + (self.Ts/self.theta_t) * (-self.prev_temp + self.Kh*self.uk + self.Tenv)
        self.prev_temp = temp
        return temp


def main():
    exp_filter = ExponentialFilter(0.3)
    controller = PIDController(
        kp=1.0,
        ki=0.0,
        kd=0.0,
        output_limits=[0,100]
    )
    
    temp_controller = TemperatureController(
        controller=controller,
        filter=exp_filter,
        update_interval_s=1
    )
    
    heater = HeaterModel()
    
    temps = [heater.update() for _ in range(1000)]
    plt.plot(temps)
    plt.show()


if __name__ == "__main__":
    main()
