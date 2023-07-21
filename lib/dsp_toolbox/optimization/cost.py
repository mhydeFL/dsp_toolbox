from typing import Iterable
import numpy as np

from dsp_toolbox.dsp.types import T


def PIDCost(
    error_weight: float,
    command_weight: float,
    setpoint: Iterable[T],
    process_value: Iterable[T],
    output_value: Iterable[T]
) -> float:
    """
    Simple cost function to minimize composed of the sum of the setpoint error, the sum of the
    changes in output variable per controller step, and the initial controller output.
    
    J = sum((stp[i] - v[i])^2*t[i])*We + sum((command[i+1] - command[i])^2)*Wu + command[0]^2*Wu
    """
    error_term = error_weight * np.sum(np.square(setpoint - process_value))
    command_term = command_weight * np.sum(np.square(np.diff(output_value)))
    bias_term = command_weight * output_value[0]**2
    
    return error_term + command_term + bias_term