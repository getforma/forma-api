import numpy as np
import pandas as pd
import json
from scipy.signal import find_peaks, butter, filtfilt, savgol_filter
from scipy.fft import fft, ifft
from math import radians, cos, sin, asin, sqrt
from scipy.integrate import cumulative_trapezoid

def calculate_session_metrics(final_df, axis):
        """
        Calculate all metrics for a running session and return them in a dictionary
        """
        distance = calculate_distance(final_df)
        speed = calculate_speed(final_df, distance)
        pace = calculate_pace(final_df, speed)
        cadence = calculate_cadence(final_df, axis)
        vertical_oscillation = calculate_vertical_oscillation(final_df, axis)
        stride_length = calculate_stride_length(final_df, axis, distance)
        ground_contact_time = calculate_ground_contact_time(final_df, axis)

        metrics = {
            "start_time": final_df.iloc[0]['time'].isoformat(),
            "end_time": final_df.iloc[-1]['time'].isoformat(),
            "distance": distance,
            "speed": speed,
            "pace": pace,
            "cadence": cadence,
            "vertical_oscillation": vertical_oscillation,
            "stride_length": stride_length,
            "ground_contact_time": ground_contact_time
        }

        return metrics

def is_flat(data):
    # Check if data is already flat by looking for nested fields
    sample_entry = data[0] if isinstance(data, list) and data else data
    return all(key not in sample_entry for key in ['acceleration', 'angular_velocity', 'magnetic_field', 'angle'])

def flatten_data(data):
    # Flatten each entry if necessary
    flattened_data = []
    for entry in data:
        flattened_entry = {
            'time': entry.get('time'),
            'latitude': entry.get('latitude'),
            'longitude': entry.get('longitude'),
            'x_acceleration': entry['acceleration'].get('x') if 'acceleration' in entry else None,
            'y_acceleration': entry['acceleration'].get('y') if 'acceleration' in entry else None,
            'z_acceleration': entry['acceleration'].get('z') if 'acceleration' in entry else None,
            'x_angular_velocity': entry['angular_velocity'].get('x') if 'angular_velocity' in entry else None,
            'y_angular_velocity': entry['angular_velocity'].get('y') if 'angular_velocity' in entry else None,
            'z_angular_velocity': entry['angular_velocity'].get('z') if 'angular_velocity' in entry else None,
            'x_magnetic_field': entry['magnetic_field'].get('x') if 'magnetic_field' in entry else None,
            'y_magnetic_field': entry['magnetic_field'].get('y') if 'magnetic_field' in entry else None,
            'z_magnetic_field': entry['magnetic_field'].get('z') if 'magnetic_field' in entry else None,
            'x_angle': entry['angle'].get('x') if 'angle' in entry else None,
            'y_angle': entry['angle'].get('y') if 'angle' in entry else None,
            'z_angle': entry['angle'].get('z') if 'angle' in entry else None
        }
        flattened_data.append(flattened_entry)
    return flattened_data

def create_dataframe_and_detect_axis(data):
    """
    Converts the input DataFrame into a pandas DataFrame with necessary columns.
    """
    if not is_flat(data):
        data = flatten_data(data)

    # Check if the input data is in JSON format
    df = pd.DataFrame(data)

    # Convert numeric columns to float64 type
    numeric_columns = [
        'x_acceleration', 'y_acceleration', 'z_acceleration',
        'x_angular_velocity', 'y_angular_velocity', 'z_angular_velocity', 
        'x_magnetic_field', 'y_magnetic_field', 'z_magnetic_field',
        'x_angle', 'y_angle', 'z_angle',
        'latitude', 'longitude'
    ]
    df[numeric_columns] = df[numeric_columns].astype(float)
    df['time'] = pd.to_datetime(df['time'], format="%Y-%m-%dT%H:%M:%S.%fZ")
    
    # Sort the dataframe by time in ascending order
    df = df.sort_values(by='time', ascending=True)
    
    # Compute global accelerations
    acc_global = compute_global_accelerations(df)
    df['x_acceleration_global'] = acc_global[:, 0]
    df['y_acceleration_global'] = acc_global[:, 1]
    df['z_acceleration_global'] = acc_global[:, 2]
    
    # Detect the vertical axis (after computing global accelerations)
    axis = detect_up_down_axis(df, global_acc=True)
    
    df, _ = final_clean_data(df, axis, global_acc=True)

    return df, axis


def compute_global_accelerations(data):
    """
    Computes the global accelerations using orientation data.
    Returns an array of global accelerations.
    """
    # Convert acceleration from Gs to m/s^2
    acc_x = data['x_acceleration'].to_numpy() * 9.81
    acc_y = data['y_acceleration'].to_numpy() * 9.81
    acc_z = data['z_acceleration'].to_numpy() * 9.81

    # Convert angles from degrees to radians
    roll = np.deg2rad(data['x_angle'].to_numpy())
    pitch = np.deg2rad(data['y_angle'].to_numpy())
    yaw = np.deg2rad(data['z_angle'].to_numpy())

    # Preallocate array for global accelerations
    acc_global = np.zeros((len(data), 3))

    # Compute rotation matrices and rotate acceleration vectors
    for i in range(len(data)):
        # Rotation matrices
        R_x = np.array([[1, 0, 0],
                        [0, np.cos(roll[i]), -np.sin(roll[i])],
                        [0, np.sin(roll[i]), np.cos(roll[i])]])

        R_y = np.array([[np.cos(pitch[i]), 0, np.sin(pitch[i])],
                        [0, 1, 0],
                        [-np.sin(pitch[i]), 0, np.cos(pitch[i])]])

        R_z = np.array([[np.cos(yaw[i]), -np.sin(yaw[i]), 0],
                        [np.sin(yaw[i]), np.cos(yaw[i]), 0],
                        [0, 0, 1]])

        # Combined rotation matrix
        R = R_z @ R_y @ R_x

        # Acceleration vector in sensor frame
        a_sensor = np.array([acc_x[i], acc_y[i], acc_z[i]])

        # Rotate to global frame
        a_global = R @ a_sensor

        acc_global[i, :] = a_global

    return acc_global

def create_dataframe_from_dynamo_data(data):
    return pd.DataFrame(data)

def detect_up_down_axis(data, global_acc=False):
    """
    Detects the axis with the highest standard deviation, assuming it corresponds to the vertical axis.
    Returns the axis as a string: 'x', 'y', or 'z'.
    """
    # Ensure data exists and convert to float type if needed
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")
    
    for col in ['x_acceleration', 'y_acceleration', 'z_acceleration',
                'x_acceleration_global', 'y_acceleration_global', 'z_acceleration_global']:
        if col in data.columns:
            data[col] = data[col].astype(float)
    if global_acc:
        stds = {
            'x': np.std(data['x_acceleration_global']),
            'y': np.std(data['y_acceleration_global']),
            'z': np.std(data['z_acceleration_global'])
        }
    else:
        stds = {
            'x': np.std(data['x_acceleration']),
            'y': np.std(data['y_acceleration']),
            'z': np.std(data['z_acceleration'])
        }
    return max(stds, key=stds.get)

def filter_non_running_data(data, axis, global_acc=False, threshold=0.2):
    """
    Filters out data where the acceleration magnitude is below a certain threshold.
    This helps in isolating periods of running from the dataset.
    """
    if global_acc:
        data['acceleration_magnitude'] = np.sqrt(
            data['x_acceleration_global']**2 + data['y_acceleration_global']**2 + data['z_acceleration_global']**2
        )
    else:
        data['acceleration_magnitude'] = np.sqrt(
            data['x_acceleration']**2 + data['y_acceleration']**2 + data['z_acceleration']**2
        )
    return data[data['acceleration_magnitude'] > threshold]

def final_clean_data(data, axis, global_acc=False):
    """
    Cleans the data by filtering out non-running data.
    Returns the cleaned data and the detected axis.
    """
    clean_data = filter_non_running_data(data, axis, global_acc=global_acc)
    clean_data['time'] = pd.to_datetime(clean_data['time'], format="%Y-%m-%dT%H:%M:%S.%fZ")
    return clean_data, axis

def apply_fft_with_filter(time, data, threshold=0.1):
    """
    Applies FFT to the data and filters out frequencies below a certain threshold.
    Returns the frequencies and the filtered FFT values.
    """
    time_in_seconds = (time - time.iloc[0]).dt.total_seconds()
    timestep = np.mean(np.diff(time_in_seconds))

    freq = np.fft.fftfreq(len(data), d=timestep)
    fft_values = fft(data)

    # Zero out FFT values below the threshold frequency
    fft_values[np.abs(freq) > threshold] = 0

    reconstructed = ifft(fft_values).real

    return reconstructed

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
    Uses the global acceleration data along the detected vertical axis.
    """
    try:
        acc_column = f'{axis}_acceleration_global'
        time = data['time']
        acceleration_data = data[acc_column].to_numpy()
        
        # Remove gravity
        acceleration_data -= 9.81

        # Apply FFT and filter the signal
        reconstructed_signal = apply_fft_with_filter(time, acceleration_data, threshold=4)

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
    Uses the global acceleration data along the detected vertical axis.
    """
    try:
        # Extract acceleration data
        acc_column = f'{axis}_acceleration_global'
        acc = data[acc_column].to_numpy()
        time = data['time']
        time_in_seconds = (time - time.iloc[0]).dt.total_seconds().to_numpy()

        # Sampling frequency
        fs = 1 / np.mean(np.diff(time_in_seconds))

        # Remove gravity component using a high-pass filter instead of low-pass
        cutoff_freq = 0.8  # Hz
        b, a = butter(2, cutoff_freq / (0.5 * fs), btype='high')
        filtered_acc = filtfilt(b, a, acc)

        # Double integration with proper filtering between steps
        # First integration (acceleration to velocity)
        velocity = cumulative_trapezoid(filtered_acc, time_in_seconds, initial=0)
        
        # Apply high-pass filter to velocity to remove drift
        b, a = butter(2, 0.8 / (0.5 * fs), btype='high')
        velocity_filtered = filtfilt(b, a, velocity)

        # Second integration (velocity to position)
        displacement = cumulative_trapezoid(velocity_filtered, time_in_seconds, initial=0)
        
        # Apply high-pass filter to displacement to remove drift
        b, a = butter(2, 0.8 / (0.5 * fs), btype='high')
        displacement_filtered = filtfilt(b, a, displacement)

        # Find peaks and troughs
        peaks, _ = find_peaks(displacement_filtered, distance=int(fs/3))  # Minimum distance between peaks
        troughs, _ = find_peaks(-displacement_filtered, distance=int(fs/3))

        # Calculate oscillations
        oscillations = []
        for i in range(len(peaks)-1):
            # Find troughs between consecutive peaks
            relevant_troughs = troughs[(troughs > peaks[i]) & (troughs < peaks[i+1])]
            if len(relevant_troughs) > 0:
                peak_to_trough = abs(displacement_filtered[peaks[i]] - displacement_filtered[relevant_troughs[0]])
                oscillations.append(peak_to_trough)

        # Calculate average vertical oscillation (in meters)
        average_vertical_oscillation = np.mean(oscillations) if oscillations else 0.0

        return average_vertical_oscillation
    except Exception as e:
        print(f"Error calculating vertical oscillation: {e}")
        return 0.0

def calculate_stride_length(data, axis, total_distance) -> float:
    """
    Calculates the average stride length.
    Uses the same method to find total steps as in calculate_cadence,
    and computes stride length as distance divided by steps.
    """
    try:
        if total_distance <= 0:
            return 0.0

        acc_column = f'{axis}_acceleration_global'
        time = data['time']
        acceleration_data = data[acc_column].to_numpy()

        # Remove gravity
        acceleration_data -= 9.81

        # Apply FFT and filter the signal (using the same threshold as in calculate_cadence)
        reconstructed_signal = apply_fft_with_filter(time, acceleration_data, threshold=4)

        # Smooth the signal using Savitzky-Golay filter
        reconstructed_signal = savgol_filter(reconstructed_signal, window_length=11, polyorder=2)

        # Find peaks in the reconstructed signal
        prominence_value = np.std(reconstructed_signal) * 0.5
        peaks, _ = find_peaks(reconstructed_signal, prominence=prominence_value)

        # Calculate total steps
        total_steps = len(peaks)

        if total_steps > 0:
            stride_length = total_distance / total_steps
            return stride_length
        else:
            return 0.0
    except Exception as e:
        print(f"Error calculating stride length: {e}")
        return 0.0

def calculate_ground_contact_time(data, axis, fft_threshold=2.2) -> float:
    """
    Calculates the average Ground Contact Time (GCT).
    Uses the global acceleration data along the detected vertical axis.
    """
    try:
        acc_column = f'{axis}_acceleration_global'
        time = data["time"]
        acceleration_data = data[acc_column].to_numpy()

        # Remove gravity
        acceleration_data -= 9.81

        # Apply FFT and filter the signal
        reconstructed_signal = apply_fft_with_filter(time, acceleration_data, threshold=fft_threshold)

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