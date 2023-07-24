import logging
from enum import IntEnum, unique
from typing import Optional
import numpy as np

from dsp_toolbox.dsp.types import FrequencyType, T


@unique
class PeriodicCharacteristic(IntEnum):
    DAMPED = 0
    STABLE = 1
    UNSTABLE = 2


class PeriodicAnalyzer:
    def __init__(
        self,
        data: np.array,
        sampling_frequency_Hz: FrequencyType,
        roi_threshold: Optional[T] = None
    ) -> None:
        self.data = data
        self.sampling_frequency_Hz = sampling_frequency_Hz
        self.roi_threshold = roi_threshold
        
        if roi_threshold:
            self.filter_region_of_interest(self.roi_threshold)
        
    def filter_region_of_interest(self, threshold: T) -> None:
        self.data = self.data[np.argmax(self.data > threshold):]
        
    def calculate_period(self) -> T:
        fourier_transform = np.fft.fft(self.data)
        num_points = len(self.data)
        fourier_transform = fourier_transform[range(int(num_points/2))][1:]
        total_time = num_points / self.sampling_frequency_Hz
        frequencies = np.arange(int(num_points / 2)) / total_time
        peak_frequency = frequencies[np.argmax(fourier_transform)]
        return 1.0 / peak_frequency
    
    def check_oscillation_stability(
        self,
        tolerance: T,
        window_size: int,
        min_windows: int = 4
    ) -> PeriodicCharacteristic:
        amplitudes = []
        num_windows = int(np.floor(len(self.data) / window_size))

        if num_windows < min_windows:
            raise Exception('Not enough data or window_size too large.')

        for i in range(1, num_windows):
            windowed_data = self.data[i*window_size:(i+1)*window_size]
            amplitude = np.absolute(
                (np.max(windowed_data) - np.min(windowed_data)) / 2
            )
            amplitudes.append(amplitude)
        logging.info(f'amplitudes: {amplitudes}')
        if amplitudes[0] < tolerance:
            return PeriodicCharacteristic.DAMPED
        amplitude_diff = amplitudes[-1] - amplitudes[0]
        if amplitude_diff > tolerance:
            return PeriodicCharacteristic.UNSTABLE
        elif amplitude_diff < -tolerance:
            return PeriodicCharacteristic.DAMPED
        
        return PeriodicCharacteristic.STABLE