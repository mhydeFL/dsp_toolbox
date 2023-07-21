import numpy as np
import matplotlib.pyplot as plt

from dsp_toolbox.dsp.types import T


class FrequencyGenerator:
    def __init__(
        self,
        amplitude_func,
        sampling_rate: T,
        frequency_Hz: T,
        duration_s: T,
        noise_amplitude: T = 0
    ) -> None:
        self.amplitude_func = amplitude_func
        self.sampling_rate = sampling_rate
        self.frequency_Hz = frequency_Hz
        self.duration_s = duration_s
        self.noise_amplitude = noise_amplitude

    def generate_waveform(self) -> np.array:
        num_samples = int(self.duration_s * self.sampling_rate)
        time = np.linspace(0, self.duration_s, num_samples)
        waveform = self.amplitude_func(time) * np.sin(2 * np.pi * self.frequency_Hz * time)
        waveform = self.generate_noise(waveform)
        return waveform
    
    def set_amplitude_func(self, func):
        self.amplitude_func = func
        
    def generate_noise(self, waveform: np.array) -> np.array:
        noise = self.noise_amplitude * np.random.randn(len(waveform))
        return waveform + noise


if __name__ == "__main__":
    def amplitude_func(t):
        return 3 + 0.25*t
    frequency_gen = FrequencyGenerator(
        amplitude_func=amplitude_func,
        sampling_rate=100,
        frequency_Hz=1,
        duration_s=10,
        noise_amplitude=0.3
    )

    waveform = frequency_gen.generate_waveform()

    plt.plot(waveform)
    plt.show()