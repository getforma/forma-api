import numpy as np
import pandas as pd
from scipy.signal import find_peaks, butter, filtfilt
from scipy.fft import fft, ifft

# Speed value to be updated when GPS data is integrated
speed = 3.4  # Placeholder value

def detect_up_down_axis(data):
    """
    Detects the axis with the highest standard deviation, assuming it corresponds to the vertical axis.
    Returns the axis as a string: 'X', 'Y', or 'Z'.
    """
    stds = {
        'X': np.std(data['AccX(g)']),
        'Y': np.std(data['AccY(g)']),
        'Z': np.std(data['AccZ(g)'])
    }
    return max(stds, key=stds.get)

def filter_non_running_data(data, threshold=1.0):
    """
    Filters out data where the acceleration magnitude is below a certain threshold.
    This helps in isolating periods of running from the dataset.
    """
    data['acceleration_magnitude'] = np.sqrt(
        data['AccX(g)']**2 + data['AccY(g)']**2 + data['AccZ(g)']**2
    )
    return data[data['acceleration_magnitude'] > threshold]

def final_clean_data(data):
    """
    Cleans the data by detecting the vertical axis and filtering out non-running data.
    Returns the cleaned data and the detected axis.
    """
    axis = detect_up_down_axis(data)
    clean_data = filter_non_running_data(data)
    return clean_data, axis

def apply_fft_with_filter(time, data, threshold=0.1):
    """
    Applies FFT to the data and filters out frequencies below a certain threshold.
    Returns the frequencies and the filtered FFT values.
    """
    time_in_seconds = (time - time.iloc[0]).dt.total_seconds()
    timestep = np.mean(np.diff(time_in_seconds))

    freq = np.fft.fftfreq(len(data), d=timestep)
    fft_values = fft(data.to_numpy())

    # Zero out FFT values below the threshold
    fft_values[np.abs(fft_values) < np.max(np.abs(fft_values)) * threshold] = 0

    return freq, fft_values

def reconstruct_signal_from_fft(fft_filtered):
    """
    Reconstructs the signal from the filtered FFT values.
    """
    return ifft(fft_filtered).real

def calculate_cadence(data) -> float:
    """
    Calculates the average cadence in steps per minute.
    Uses the acceleration data along the detected vertical axis.
    """
    # Get the cleaned data and detected axis
    clean_data, axis = final_clean_data(data)
    acc_column = f'Acc{axis}(g)'
    time = clean_data['time']
    acceleration_data = clean_data[acc_column]

    # Apply FFT and filter the signal
    freq, fft_filtered = apply_fft_with_filter(time, acceleration_data, threshold=0.1)
    reconstructed_signal = reconstruct_signal_from_fft(fft_filtered)

    # Calculate sampling rate
    sampling_interval = np.mean(time.diff().dt.total_seconds())
    sampling_rate = 1 / sampling_interval

    # Estimate expected step frequency
    expected_cadence = 180  
    expected_step_frequency = expected_cadence / 60  
    expected_samples_between_steps = sampling_rate / expected_step_frequency

    # Find peaks in the reconstructed signal
    peaks, _ = find_peaks(reconstructed_signal, distance=expected_samples_between_steps * 0.5)

    # Calculate total time in minutes
    total_time = (time.iloc[-1] - time.iloc[0]).total_seconds() / 60.0

    # Calculate cadence
    total_steps = len(peaks)
    cadence = total_steps / total_time  # Steps per minute

    return cadence

def calculate_distance(data) -> float:
    """
    Placeholder function for calculating distance.
    To be implemented when GPS data is available.
    """
    return 0.0

def calculate_speed(data) -> float:
    """
    Placeholder function for calculating speed.
    To be implemented when GPS data is available.
    """
    return 0.0

def calculate_vertical_oscillation(data) -> float:
    """
    Calculates the average vertical oscillation.
    Uses the acceleration data along the detected vertical axis.
    """
    # Get the cleaned data and detected axis
    clean_data, axis = final_clean_data(data)
    acc_column = f'Acc{axis}(g)'
    acc_z = clean_data[acc_column].to_numpy() * 9.81  # Convert to m/s^2
    time = (clean_data['time'] - clean_data['time'].iloc[0]).dt.total_seconds().to_numpy()

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

    # Calculate amplitude
    peak_acceleration = np.max(acc_z_filtered)
    trough_acceleration = np.min(acc_z_filtered)
    amplitude = (peak_acceleration - trough_acceleration) / 2

    # Calculate vertical oscillation using the harmonic motion formula
    if dominant_freq > 0:
        vertical_oscillation = amplitude / ((2 * np.pi * dominant_freq) ** 2)
        return vertical_oscillation
    else:
        return None

def calculate_stride_length(data, speed) -> float:
    """
    Calculates the average stride length.
    Uses zero crossings of the acceleration data along the detected vertical axis.
    """
    # Get the cleaned data and detected axis
    clean_data, axis = final_clean_data(data)
    acc_column = f'Acc{axis}(g)'
    acceleration_data = clean_data[acc_column].to_numpy()
    time = clean_data['time']

    # Find zero crossings in the acceleration data
    zero_crossings = np.where(np.diff(np.signbit(acceleration_data)))[0]

    # Calculate airborne times between zero crossings
    airborne_times = []
    for z1, z2 in zip(zero_crossings[:-1], zero_crossings[1:]):
        t1 = time.iloc[z1]
        t2 = time.iloc[z2]
        airborne_times.append((t2 - t1).total_seconds())

    # Calculate stride lengths
    stride_lengths = [speed * t for t in airborne_times]

    # Return the average stride length
    return np.mean(stride_lengths) if stride_lengths else None

def calculate_ground_contact_time(data, time_column='time', fft_threshold=0.1) -> float:
    """
    Calculates the average Ground Contact Time (GCT).
    Uses the acceleration data along the detected vertical axis.
    """
    # Get the cleaned data and detected axis
    clean_data, axis = final_clean_data(data)
    acc_column = f'Acc{axis}(g)'
    time = clean_data[time_column]
    acceleration_data = clean_data[acc_column]

    # Apply FFT and filter the signal
    freq, fft_filtered = apply_fft_with_filter(time, acceleration_data, threshold=fft_threshold)
    reconstructed_signal = reconstruct_signal_from_fft(fft_filtered)

    # Find peaks and valleys in the reconstructed signal
    peaks, _ = find_peaks(reconstructed_signal)
    valleys, _ = find_peaks(-reconstructed_signal)

    # Calculate GCT values
    gct_values = []
    for v in valleys:
        subsequent_peaks = peaks[peaks > v]
        if subsequent_peaks.size > 0:
            peak = subsequent_peaks[0]
            # Ground Contact Time in milliseconds
            gct = (time.iloc[peak] - time.iloc[v]).total_seconds() * 1000
            gct_values.append(gct)
    return np.mean(gct_values) if gct_values else None

def calculate_pace(data) -> float:
    """
    Placeholder function for calculating pace.
    To be implemented when GPS data is available.
    """
    return 0.0

