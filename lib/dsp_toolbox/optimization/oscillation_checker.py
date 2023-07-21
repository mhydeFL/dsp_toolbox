from numpy.fft import fft
import numpy as np
import matplotlib.pyplot as plt
from dsp_toolbox.optimization.frequency_generator import generate_waveform
from dsp_toolbox.data.database import Database
from dsp_toolbox.dsp.filters.median_filter import MedianFilter
from dsp_toolbox.dsp.filters.exponential_filter import ExponentialFilter


UNSTABLE = 1
STABLE = 0
DAMPED = -1


MIN_WINDOWS = 4


def calculate_period(data, sampling_freq_Hz):
    """

    """
    fourier_transform = fft(data)
    num_points = len(data)
    # crop to exclude sampling frequency
    fourier_transform = fourier_transform[range(int(num_points/2))]

    total_time = num_points / sampling_freq_Hz
    frequencies = np.arange(int(num_points / 2)) / total_time

    peak_frequency = frequencies[np.argmax(fourier_transform)]
    period = 1.0 / peak_frequency
    return period


def check_oscillation_stability(data, window_size, tol=0.2):
    """
    Checks if the response has a unstable oscillation, damped oscillation, or stable oscillation.
    data: 1D array of oscillations. any ramp-up should be cropped out
    window_size: should be at least the period of the oscillation
    tolerance: how much amplitude difference is considered stable

    returns UNSTABLE, STABLE, or DAMPED
    """

    amplitudes = []
    num_windows = np.floor(len(data) / window_size)

    if num_windows < MIN_WINDOWS:
        raise Exception('Not enough data or window_size too large.')

    for i in num_windows:
        windowed_data = data[i*window_size:(i+1)*window_size]
        amplitude = np.absolute(
            (np.max(windowed_data) - np.min(windowed_data)) / 2
        )
        amplitudes.append(amplitude)
    print(f'amplitudes: {amplitudes}')
    amplitude_diff = np.diff(amplitudes)
    average_amplitude_diff = np.mean(amplitude_diff)
    if average_amplitude_diff > tol:
        return UNSTABLE
    elif average_amplitude_diff < -tol:
        return DAMPED
    else:
        return STABLE


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




