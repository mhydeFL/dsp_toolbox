import numpy as np
import matplotlib.pyplot as plt

from dsp_toolbox.dsp.types import T


class FrequencyGenerator:
    def __init__(
        self,
        amplitude_func,
        sample_rate: T,
        frequency_Hz: T,
        duration_s: T,
        noise_magnitude: T = 0
    ) -> None:
        self.amplitude_func = amplitude_func
        self.sample_rate = sample_rate
        self.frequency_Hz = frequency_Hz
        self.duration_s = duration_s
        self.noise_magnitude = noise_magnitude

    def generate_waveform(self) -> np.array:
        num_samples = int(self.duration_s * self.sample_rate)
        time = np.linspace(0, self.duration_s, num_samples)
        waveform = self.amplitude_func(time) * np.sin(2 * np.pi * self.frequency_Hz * time)
        waveform = self.generate_noise(waveform)
        return waveform
    
    def set_amplitude_func(self, func):
        self.amplitude_func = func
        
    def generate_noise(self, waveform: np.array) -> np.array:
        noise = self.noise_magnitude * np.random.randn(len(waveform))
        return waveform + noise
