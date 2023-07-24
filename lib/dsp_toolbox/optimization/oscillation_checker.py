import logging
from enum import IntEnum, unique
import numpy as np
from numpy.fft import fft

from dsp_toolbox.dsp.types import (
    TimeType,
    FrequencyType,
    T
)


@unique
class PeriodicCharacteristic(IntEnum):
    DAMPED = -1
    STABLE = 0
    UNSTABLE = 1

def find_region_of_interest(data: np.array, threshold: T) -> int:
    return np.argmax(data>threshold)

def calculate_period(data: np.array, sampling_freq_Hz: FrequencyType) -> TimeType:
    fourier_transform = fft(data)
    num_points = len(data)
    fourier_transform = fourier_transform[range(int(num_points/2))][1:]
    total_time = num_points / sampling_freq_Hz
    frequencies = np.arange(int(num_points / 2)) / total_time
    peak_frequency = frequencies[np.argmax(fourier_transform)]
    return 1.0 / peak_frequency


def check_oscillation_stability(
    data: np.array,
    window_size: int,
    tol: T=0.2,
    min_windows: int=4
) -> PeriodicCharacteristic:
    amplitudes = []
    num_windows = int(np.floor(len(data) / window_size))

    if num_windows < min_windows:
        raise Exception('Not enough data or window_size too large.')

    for i in range(1, num_windows):
        windowed_data = data[i*window_size:(i+1)*window_size]
        amplitude = np.absolute(
            (np.max(windowed_data) - np.min(windowed_data)) / 2
        )
        amplitudes.append(amplitude)
    logging.info(f'amplitudes: {amplitudes}')
    if amplitudes[0] < tol:
        return PeriodicCharacteristic.DAMPED
    amplitude_diff = amplitudes[-1] - amplitudes[0]
    if amplitude_diff > tol:
        return PeriodicCharacteristic.UNSTABLE
    elif amplitude_diff < -tol:
        return PeriodicCharacteristic.DAMPED
    
    return PeriodicCharacteristic.STABLE
