from dsp_toolbox.dsp.types import T
from dsp_toolbox.dsp.controllers.pid import PIDController
from dsp_toolbox.dsp.filters.exponential_filter import ExponentialFilter

import numpy as np
import matplotlib.pyplot as plt


class HeaterModel:
    def __init__(
            self,
            controller: PIDController,
            update_interval_s: T,
            setpoint: T,
            heater_gain: T,
            time_constant: T,
            time_delay: T,
            ambient_temperature: T,
            sample_time
    ) -> None:
        self.controller = controller
        self.update_interval_s = update_interval_s

        self.setpoint_C = setpoint
        self.temperature_C = None
        self.time_of_last_update = 0.0

        self.Kh = heater_gain
        self.theta_t = time_constant
        self.theta_d = time_delay
        self.Tenv = ambient_temperature
        self.Ts = sample_time

    def setpoint(self, setpoint_C: T) -> None:
        self.setpoint_C = setpoint_C

    def update(self, temperature_C: T):
        if self.setpoint_C is None:
            return None
        now = self.time_of_last_update + self.update_interval_s

        self.time_of_last_update = now
        return self.controller.update(temperature_C, self.setpoint_C)

    def run(self) -> []:
        Tstop = 200
        N = int(Tstop / self.Ts)
        Tout = np.zeros(N + 2)
        Tout[0] = 20
        e = np.zeros(N + 2)
        u = np.zeros(N + 2)
        t = np.arange(0, Tstop + 2 * self.Ts, self.Ts)
        for k in range(N + 1):
            print(Tout[k])
            e[k] = self.setpoint_C - Tout[k]
            u[k] = self.update(Tout[k], )
            Tout[k + 1] = Tout[k] + (self.Ts / self.theta_t) * (
                        -Tout[k] + self.Kh * u[int(k - self.theta_d / self.Ts)] + self.Tenv)
            print("t = %2.1f, u = %3.2f, Tout = %3.1f" % (t[k], u[k], Tout[k + 1]))
        return Tout


class PidSimulation:
    def __init__(self,
                 model: HeaterModel,
                 ) -> None:
        self.model = model

    def run(self) -> []:
        print("starting simulator")
        return self.model.run()


def main():
    controller = PIDController(
        kp=5.0,
        ki=0.0,
        kd=0.0,
        output_limits=[0, 5]
    )
    model = HeaterModel(
        controller=controller,
        update_interval_s=0.1,
        setpoint=28,
        heater_gain=3.5,
        time_constant=22,
        time_delay=2,
        ambient_temperature=21.5,
        sample_time=0.1
    )
    simulation = PidSimulation(
        model=model
    )

    model_output = simulation.run()
    plt.plot(model_output)
    plt.show()


if __name__ == "__main__":
    main()
