import numpy as np
import pandas as pd
from scipy.signal import find_peaks, butter, filtfilt
from scipy.fft import fft, ifft

speed = 3.4 #will update when I figure out the gps shit

def detect_up_down_axis(data):
    stds = {
        'X': np.std(data['AccX(g)']),
        'Y': np.std(data['AccY(g)']),
        'Z': np.std(data['AccZ(g)'])
    }
    return max(stds, key=stds.get)

def filter_non_running_data(data, threshold=1.0):
    data['acceleration_magnitude'] = np.sqrt(
        data['AccX(g)']**2 + data['AccY(g)']**2 + data['AccZ(g)']**2
    )
    return data[data['acceleration_magnitude'] > threshold]

def adjust_data_orientation(data, axis):
    if axis == 'X':
        data = data.copy() 
        data['AccZ(g)'] = data['AccX(g)']
    elif axis == 'Y':
        data = data.copy()
        data['AccZ(g)'] = data['AccY(g)']
    return data

def apply_fft_with_filter(time, data, threshold=0.1):
    time_in_seconds = (time - time.iloc[0]).dt.total_seconds()
    timestep = np.mean(np.diff(time_in_seconds))

    freq = np.fft.fftfreq(len(data), d=timestep)
    fft_values = fft(data.to_numpy())
    fft_values[np.abs(fft_values) < np.max(np.abs(fft_values)) * threshold] = 0

    return freq, fft_values

def reconstruct_signal_from_fft(fft_filtered):
    return ifft(fft_filtered).real

def calculate_cadence(data) -> float:
    time = data['time']
    acceleration_data = data['AccZ(g)']
    freq, fft_filtered = apply_fft_with_filter(time, acceleration_data, threshold=0.1)
    reconstructed_signal = reconstruct_signal_from_fft(fft_filtered)

    sampling_interval = np.mean(time.diff().dt.total_seconds())
    sampling_rate = 1 / sampling_interval

    expected_cadence = 180  
    expected_step_frequency = expected_cadence / 60  
    expected_samples_between_steps = sampling_rate / expected_step_frequency

    peaks, _ = find_peaks(reconstructed_signal, distance=expected_samples_between_steps * 0.5)

    total_time = (time.iloc[-1] - time.iloc[0]).total_seconds() / 60.0

    total_steps = len(peaks)

    cadence = total_steps / total_time  # Steps per minute

    return cadence

def calculate_distance(data) -> float:
    return 0.0

def calculate_speed(data) -> float:
    return 0.0

def calculate_vertical_oscillation(data) -> float:
    acc_z = data['AccZ(g)'].to_numpy() * 9.81
    time = (data['time'] - data['time'].iloc[0]).dt.total_seconds().to_numpy()

    # High-pass filter to remove gravity component (cut-off frequency can be adjusted)
    sampling_rate = 1 / np.mean(np.diff(time))
    cutoff_frequency = 0.5  # Hz
    b, a = butter(2, cutoff_frequency / (0.5 * sampling_rate), btype='highpass')
    acc_z_filtered = filtfilt(b, a, acc_z)

    # Find dominant frequency using FFT
    freq_domain = np.fft.rfftfreq(len(acc_z_filtered), d=1/sampling_rate)
    fft_magnitude = np.abs(np.fft.rfft(acc_z_filtered))
    dominant_freq_index = np.argmax(fft_magnitude)
    dominant_freq = freq_domain[dominant_freq_index]

    peak_acceleration = np.max(acc_z_filtered)
    trough_acceleration = np.min(acc_z_filtered)
    amplitude = (peak_acceleration - trough_acceleration) / 2

    # Calculate vertical oscillation using the harmonic motion formula
    if dominant_freq > 0:
        vertical_oscillation = amplitude / ((2 * np.pi * dominant_freq) ** 2)
        return vertical_oscillation
    else:
        return None

def calculate_stride_length(data) -> float:
    zero_crossings = np.where(np.diff(np.signbit(data['AccZ(g)'].to_numpy())))[0]
    airborne_times = []
    for z1, z2 in zip(zero_crossings[:-1], zero_crossings[1:]):
        t1 = data['time'].iloc[z1]
        t2 = data['time'].iloc[z2]
        airborne_times.append((t2 - t1).total_seconds())
    stride_lengths = [speed * t for t in airborne_times]
    return np.mean(stride_lengths) if stride_lengths else None

def calculate_ground_contact_time(data, time_column='time', acc_column='AccZ(g)', fft_threshold=0.1) -> float:
    time = data[time_column]
    acceleration_data = data[acc_column]

    freq, fft_filtered = apply_fft_with_filter(time, acceleration_data, threshold=fft_threshold)
    reconstructed_signal = reconstruct_signal_from_fft(fft_filtered)

    peaks, _ = find_peaks(reconstructed_signal)
    valleys, _ = find_peaks(-reconstructed_signal)

    gct_values = []
    for v in valleys:
        subsequent_peaks = peaks[peaks > v]
        if subsequent_peaks.size > 0:
            peak = subsequent_peaks[0]
            gct = (time.iloc[peak] - time.iloc[v]).total_seconds() * 1000
            gct_values.append(gct)

def calculate_pace(data) -> float:
    return 0.0
