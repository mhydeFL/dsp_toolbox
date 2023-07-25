import numpy as np
import matplotlib.pyplot as plt

from dsp_toolbox.dsp.simulation import Simulation
from dsp_toolbox.dsp.controllers.pid import PIDController
from dsp_toolbox.dsp.models.first_order_model import FirstOrderModel
from dsp_toolbox.dsp.models.second_order_model import SecondOrderModel


def first_order_test():
    controller = PIDController(
        kp=5.0,
        ki=0.0,
        kd=0.0,
        output_limits=[0, 100]
    )
    model = FirstOrderModel(
        gain=3.5,
        time_constant=1.0,
        initial_condition=0.0
    )
    
    sim = Simulation(
        controller=controller,
        model=model,
        setpoint=10
    )
    
    data = sim.run(500)
    plt.plot(data)
    plt.show()

def second_order_test():
    controller = PIDController(
        kp=3.0,
        ki=0.0,
        kd=0.0,
        output_limits=[0, 100]
    )
    model = SecondOrderModel(
        natural_frequency=1,
        damping_ratio=0.25,
        initial_condition=0.0
    )
    
    sim = Simulation(
        controller=controller,
        model=model,
        setpoint=10
    )
    
    data = sim.run(500)
    plt.plot(data)
    plt.show()
    

def main():
    first_order_test()
    second_order_test()
    
    
if __name__ == "__main__":
    main()