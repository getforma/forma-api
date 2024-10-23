# Forma API

## Instructions

1. Create a virtual environment
```bash
python -m venv .venv
```
or

```bash
python3 -m venv .venv
```

2. Activate virtual environment
In MacOS/Linux/Unix:
```bash
source .venv/bin/activate
````

3. Install dependencies
```bash
make install
```

4. Run tests
```
make test
```
# Running Form Analysis

This Python script analyzes accelerometer data collected from a wearable device to estimate key running metrics such as **Ground Contact Time (GCT)**, **Stride Length**, **Vertical Oscillation**, and **Cadence**. The script includes data cleaning procedures, signal filtering using Fourier Transforms, and automatic detection of the up-down axis to ensure accurate analysis, regardless of sensor placement and non-running data points.

## Overview

The purpose of this project is to analyze accelerometer data collected from wearables, in order to calculate metrics that are indicative of running form. This analysis helps athletes monitor their running form, detect inefficiencies, and prevent injury. The data is cleaned and processed to account for variations in sensor placement and to filter out noise using signal processing techniques such as the Fourier Transform and high-pass filters.

The key metrics calculated are:
- **Ground Contact Time (GCT)**: The time your foot spends in contact with the ground during each stride.
- **Stride Length**: The estimated length of each stride based on the speed and airborne time between strides.
- **Vertical Oscillation**: The vertical movement of the runner during the running cycle, calculated using filtered acceleration data and harmonic motion principles.
- **Cadence**: The number of steps per minute, determined by identifying peaks in the reconstructed acceleration signal.

## Features

- **Automatic Axis Detection**: Detects the "up-and-down" axis (which may differ based on sensor placement) by analyzing which axis matches typical running acceleration patterns.
- **Data Cleaning**: Excludes data points before running starts by setting a threshold for acceleration to remove noise.
- **Fourier Transform-Based Signal Filtering**: Uses the Fast Fourier Transform (FFT) to filter noise from the acceleration data, preserving important features while removing irrelevant components.
- **Signal Reconstruction**: Reconstructs the filtered signal using the inverse Fourier Transform, allowing for cleaner and more accurate analysis of peaks and valleys in the data.
- **Ground Contact Time Calculation**: Detects peaks and valleys in the reconstructed signal to calculate GCT.
- **Stride Length Calculation**: Estimates stride length based on airborne time and runner speed.
- **Vertical Oscillation Calculation**: Calculates vertical oscillation using filtered acceleration data, accounting for gravitational forces, and using harmonic motion equations.
- **Cadence Calculation**: Calculates the number of steps per minute by identifying peaks in the reconstructed signal and adjusting for the sampling rate.

## Math Behind the Calculations

### 1. **Fourier Transform**

The **Fourier Transform** is a mathematical tool used to break down a signal (like the accelerometer data) into its constituent frequencies. In this project, the **Fast Fourier Transform (FFT)** is used to convert the acceleration signal from the time domain to the frequency domain. This helps us identify the important frequencies that relate to the running pattern, filtering out noise, and focusing on meaningful data.

The FFT helps in filtering out unwanted noise by setting a threshold and eliminating frequencies below this threshold. The **Inverse Fourier Transform** is then used to reconstruct the cleaned signal from the filtered frequency components.

- **Why it’s useful**: Many signals, such as those generated during running, are noisy. The Fourier Transform allows us to focus on the dominant frequencies that represent the core running motion, helping to improve the accuracy of GCT, stride length, and cadence calculations.

### 2. **Harmonic Motion**

In the context of **Vertical Oscillation**, we treat the runner's vertical motion as a type of simple harmonic motion (like a bouncing spring). The amplitude of the vertical movement is calculated based on the difference between peak and trough accelerations, and the dominant frequency is found using FFT.

- **Equation**: For vertical oscillation, we use the harmonic motion formula:
  
  $$\text{Vertical Oscillation} = \frac{\text{Amplitude}}{(2\pi \times f)^2} \$$

  Where:
  - **Amplitude** is half the difference between the peak and trough accelerations.
  - **f** is the dominant frequency of the vertical motion.
  
  This formula is derived from basic harmonic motion equations where the motion follows a periodic pattern.

- **Why it’s useful**: By treating the runner's vertical movement as harmonic motion, we can approximate the vertical oscillation, which is an important metric for analyzing running efficiency.

### 3. **Newtonian Physics**

Newton's laws of motion come into play in several calculations, particularly when using acceleration data to derive velocity and displacement. Specifically:

- **Acceleration**: The accelerometer measures acceleration, which is the rate of change of velocity.
- **Velocity**: By integrating the acceleration data over time, we estimate the velocity of the runner in the up-down direction. This velocity is then used in calculations such as vertical oscillation and airborne time.
  
  $$\ v(t) = \int a(t) \, dt \$$
  
- **Displacement**: By integrating velocity, we estimate the displacement of the runner's body, which helps in calculating stride length and vertical oscillation.

- **Why it’s useful**: Newton's laws form the foundation of these calculations. Understanding the relationship between acceleration, velocity, and displacement allows us to derive important running metrics from raw accelerometer data.

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/running-form-analysis.git
   cd running-form-analysis

