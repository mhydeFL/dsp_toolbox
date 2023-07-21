from numpy.fft import fft
import numpy as np
import matplotlib.pyplot as plt
from dsp_toolbox.optimization.freqency_generator import generate_waveform
from dsp_toolbox.data.database import Database
from dsp_toolbox.dsp.filters.median_filter import MedianFilter
from dsp_toolbox.dsp.filters.exponential_filter import ExponentialFilter


def check_oscillation_stability(data, window):
    """
    Checks for a stable oscillation by taking the Fourier Transform and looking for a single frequency spike
    data: 1D array of data

    return: True or False
    """


def get_temp_from_sqlite(filepath: str) -> np.array:
    db = Database(filepath=filepath, table_name="Environmental_v3")
    db.load_database()
    # print(db.database.dtypes)

    temp_L = db.database.heater_temperature_left_C
    temp_R = db.database.heater_temperature_right_C
    temp_series = np.array([max(l, r) for l, r in zip(temp_L, temp_R)])
    return temp_series


if __name__ == "__main__":
    # growing_oscillation = generate_waveform()
    # def stable_amp(t):
    #     return 3
    # def stable_small_amp(t):
    #     return 1
    #
    # def growing_amp(t):
    #     return 3 + 0.75 * t
    # def shrinking_amp(t):
    #     return 3 / (2*t+1)
    # stable_oscillation = generate_waveform(amplitude_func=stable_amp)
    # stable_oscillation_less_noise = generate_waveform(amplitude_func=stable_amp, noise_amplitude=0.1)
    # stable_oscillation_smaller_amp = generate_waveform(amplitude_func=stable_small_amp)
    # more_growing_oscillation = generate_waveform(amplitude_func=growing_amp)
    # shrinking = generate_waveform(shrinking_amp)
    #
    # plt.plot(stable_oscillation)
    # plt.plot(stable_oscillation_smaller_amp)
    # # plt.plot(stable_oscillation_less_noise)
    # # plt.plot(growing_oscillation)
    # # plt.plot(more_growing_oscillation)
    # # plt.plot(shrinking)
    # plt.figure()
    #
    # plt.plot(fft(stable_oscillation))
    # plt.plot(fft(stable_oscillation_smaller_amp))
    # # plt.plot(fft(stable_oscillation_less_noise))
    # # plt.plot(fft(growing_oscillation))
    # # plt.plot(fft(more_growing_oscillation))
    # # plt.plot(fft(shrinking))
    # plt.figure()


    temp02 = get_temp_from_sqlite("../../../data/P3M02_1.sqlite")[3260:6150]
    temp03 = get_temp_from_sqlite("../../../data/P3M03_1.sqlite")[6500:9000]
    temp06 = get_temp_from_sqlite("../../../data/P3M06_1.sqlite")[11000:13900]

    filter = MedianFilter(10)
    filtered_temp02 = [filter.update(temp) for temp in temp02][30:]
    filtered_temp03 = [filter.update(temp) for temp in temp03][30:]
    filtered_temp06 = [filter.update(temp) for temp in temp06][30:]


    plt.figure()
    plt.plot(temp02)
    plt.plot(temp03)
    plt.plot(temp06)

    plt.figure()
    plt.plot(filtered_temp02)
    plt.plot(filtered_temp03)
    plt.plot(filtered_temp06)

    plt.figure()
    plt.plot(fft(temp02)[1:])
    plt.plot(fft(temp03)[1:])
    plt.plot(fft(temp06)[1:])

    plt.figure()
    plt.plot(fft(filtered_temp02)[1:])
    plt.plot(fft(filtered_temp03)[1:])
    plt.plot(fft(filtered_temp06)[1:])

    plt.show()




