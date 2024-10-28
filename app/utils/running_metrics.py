import numpy as np
import pandas as pd
from scipy.signal import find_peaks, butter, filtfilt, savgol_filter
from scipy.fft import fft, ifft
from math import radians, cos, sin, asin, sqrt

def create_dataframe_and_detect_axis(data):
    """
    Converts the input JSON data into a pandas DataFrame.
    """
    records = {
        'time': [entry['time'] for entry in data],
        'latitude': [entry['latitude'] for entry in data],
        'longitude': [entry['longitude'] for entry in data],
        'x_acceleration': [entry['acceleration']['x'] for entry in data],
        'y_acceleration': [entry['acceleration']['y'] for entry in data],
        'z_acceleration': [entry['acceleration']['z'] for entry in data],
        'x_angular_velocity': [entry['angular_velocity']['x'] for entry in data],
        'y_angular_velocity': [entry['angular_velocity']['y'] for entry in data],
        'z_angular_velocity': [entry['angular_velocity']['z'] for entry in data],
        'x_magnetic_field': [entry['magnetic_field']['x'] for entry in data],
        'y_magnetic_field': [entry['magnetic_field']['y'] for entry in data],
        'z_magnetic_field': [entry['magnetic_field']['z'] for entry in data],
        'x_angle': [entry['angle']['x'] for entry in data],
        'y_angle': [entry['angle']['y'] for entry in data],
        'z_angle': [entry['angle']['z'] for entry in data]
    }
    
    df = pd.DataFrame(records)
    df['time'] = pd.to_datetime(df['time'], format="%Y-%m-%dT%H:%M:%S.%f")
    # Sort the dataframe by time in ascending order
    df, axis = final_clean_data(df)
    df = df.sort_values(by='time', ascending=True)
    return df, axis

def detect_up_down_axis(data):
    """
    Detects the axis with the highest standard deviation, assuming it corresponds to the vertical axis.
    Returns the axis as a string: 'X', 'Y', or 'Z'.
    """
    stds = {
        'x': np.std(data['x_acceleration']),
        'y': np.std(data['y_acceleration']),
        'z': np.std(data['z_acceleration'])
    }
    return max(stds, key=stds.get)

def filter_non_running_data(data, threshold=0.2):
    """
    Filters out data where the acceleration magnitude is below a certain threshold.
    This helps in isolating periods of running from the dataset.
    """
    data['acceleration_magnitude'] = np.sqrt(
        data['x_acceleration']**2 + data['y_acceleration']**2 + data['z_acceleration']**2
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

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculates the great-circle distance between two points on the Earth surface.
    Input coordinates are in decimal degrees.
    Returns distance in meters.
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    R = 6371000  

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    distance = R * c
    return distance

def calculate_distance(df) -> float:
    """
    Calculates the total distance covered using latitude and longitude data.
    Returns the distance in meters.
    """
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        return 0.0

    data = df.dropna(subset=['latitude', 'longitude'])

    data = data.reset_index(drop=True)

    distances = []
    for i in range(1, len(data)):
        lat1, lon1 = data.loc[i - 1, ['latitude', 'longitude']]
        lat2, lon2 = data.loc[i, ['latitude', 'longitude']]
        distance = haversine(lon1, lat1, lon2, lat2)
        distances.append(distance)

    total_distance = sum(distances)
    return total_distance

def calculate_speed(data, total_distance=None) -> float:
    """
    Calculates the average speed over the data interval.
    Returns the speed in meters per second.
    """
    if total_distance is None:
        total_distance = calculate_distance(data)

    if 'time' not in data.columns or len(data) < 2:
        return 0.0
    
    total_time = (data['time'].iloc[-1] - data['time'].iloc[0]).total_seconds()

    if total_time > 0:
        average_speed = total_distance / total_time 
        return average_speed
    else:
        return 0.0

def calculate_pace(data, average_speed=None) -> float:
    """
    Calculates the average pace over the data interval.
    Returns the pace in minutes per kilometer.
    """
    if average_speed is None:
        average_speed = calculate_speed(data) 

    if average_speed > 0:
        pace = (1000 / average_speed) / 60  
        return pace
    else:
        return 0.0

def calculate_cadence(data, axis) -> float:
    """
    Calculates the average cadence in steps per minute.
    Uses the acceleration data along the detected vertical axis.
    """
    try:
        acc_column = f'{axis}_acceleration'
        time = data['time']
        acceleration_data = data[acc_column]
        
        # Apply FFT and filter the signal
        freq, fft_filtered = apply_fft_with_filter(time, acceleration_data, threshold=0.1)
        reconstructed_signal = reconstruct_signal_from_fft(fft_filtered)
        
        reconstructed_signal = savgol_filter(reconstructed_signal, window_length=11, polyorder=2)
        
        prominence_value = np.std(reconstructed_signal) * 0.5
        peaks, _ = find_peaks(reconstructed_signal, prominence=prominence_value)
        
        # Calculate total time in minutes
        total_time = (time.iloc[-1] - time.iloc[0]).total_seconds() / 60.0
        
        # Calculate cadence
        total_steps = len(peaks)
        if total_time > 0:
            cadence = total_steps / total_time  
            return cadence
        else:
            return 0.0
    except Exception as e:
        print(f"Error calculating cadence: {e}")
        return 0.0



def calculate_vertical_oscillation(data, axis) -> float:
    """
    Calculates the average vertical oscillation.
    Uses the acceleration data along the detected vertical axis.
    """
    try:
        acc_column = f'{axis}_acceleration'
        acc_z = data[acc_column].to_numpy() * 9.81  # Convert to m/s^2
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
    except Exception as e:
        print(f"Error calculating vertical oscillation: {e}")
        return 0.0

def calculate_stride_length(data, axis, average_speed=None) -> float:
    """
    Calculates the average stride length.
    Uses zero crossings of the acceleration data along the detected vertical axis.
    """
    try:
        if average_speed is None:
            average_speed = calculate_speed(data) 

        if average_speed <= 0:
            return 0.0

        acc_column = f'{axis}_acceleration'
        acceleration_data = data[acc_column].to_numpy()
        time = data['time']

        zero_crossings = np.where(np.diff(np.signbit(acceleration_data)))[0]

        airborne_times = []
        for z1, z2 in zip(zero_crossings[:-1], zero_crossings[1:]):
            t1 = time.iloc[z1]
            t2 = time.iloc[z2]
            airborne_times.append((t2 - t1).total_seconds())

        stride_lengths = [average_speed * t for t in airborne_times]

        return np.mean(stride_lengths) if stride_lengths else 0.0
    except Exception as e:
        print(f"Error calculating stride length: {e}")
        return 0.0

def calculate_ground_contact_time(data, axis, fft_threshold=0.1) -> float:
    """
    Calculates the average Ground Contact Time (GCT).
    Uses the acceleration data along the detected vertical axis.
    """
    try:
        acc_column = f'{axis}_acceleration'
        time = data["time"]
        acceleration_data = data[acc_column]

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
        return np.mean(gct_values) if gct_values else 0.0
    except Exception as e:
        print(f"Error calculating ground contact time: {e}")
        return 0.0