'''
Photoplethysmography (PPG) is a technique that measures blood volume changes in the body using a light sensor. It is often used to monitor heart rate and blood circulation. 
A PPG signal shows the regular changes in blood flow caused by each heartbeat and includes important points like the systolic peak, dicrotic notch, and diastolic peak.

In this work, the systolic peaks are detected using the Elgendi method. This method calculates the first derivative of the PPG signal and finds the points where the slope 
changes from positive to negative, which shows the location of systolic peaks. To improve the accuracy of detection, an amplitude threshold and a minimum distance between
peaks are also applied, based on the expected heart rate and the sampling frequency.

In the PPG waveform:

    The systolic peak happens when blood is pumped out of the heart, showing the highest point in the signal.

    The dicrotic notch appears after the systolic peak and is caused by the closure of the aortic valve, making a small dip in the signal.

    The diastolic peak comes after the dicrotic notch and is due to the reflected blood wave from the body, creating a small second rise.

Similarly, the dicrotic notch and diastolic peak can be detected using the first or second derivative of the PPG signal. In the first derivative, the dicrotic notch appears
as a local minimum after the systolic peak, and the diastolic peak appears as a local maximum after the notch. these features could provide important information about heart
activity from PPG signal.
'''

# Required libraries

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks


# Load the PPG signal

ppg = pd.read_csv('/home/nader/Desktop/ml-env/raw_ppg.csv')
ppg = ppg.iloc[:, 0].values

# Parameters

fs = 1000                                       # Sampling frequency (Hz)
window_size = 0.12 * fs                         # Window size for moving average filter (in samples)

save_dir = '/home/nader/Desktop/ml-env'        # Directory of saving final figures



# Moving average filter.
'''
Moving average filter is able to proper edge handling. This method is very fast  and has low computational cost even for large signals that is necessary for embedded devices. 

In this case, that the PPG signal does not have sharp high-frequency content, moving average is totally effective to smooth wander baselines. 

In this vein, we employ padding at start and end of signal because it allows moving average to be centered even at the adges without loosing data, and preserve full signal 
length and better edge behaviour.
'''

def moving_average_filter(signal, window_size):
    window_size = int(window_size)
    
    # Ensure the window size is odd to maintain symmetry
    if window_size % 2  == 0:
        window_size += 1
    half_window = window_size // 2
    
    # Pad the signal at start and end to avoid edge effects
    padded_signal = np.pad(signal, pad_width=half_window, mode='reflect')
    
    window = np.ones(window_size) / window_size    
    filtered_signal = np.convolve(padded_signal, window, mode='valid')
    
    return filtered_signal


## Systolic peak detection

'''
The following function is developed to detect systolic peaks from PPG signals using the Elgendi method.

In this method, for PPG peak detection, the first derivative of the signal is calculated to find points where the slope changes from positive to negative, indicating potential 
systolic peaks. These points correspond to zero-crossings of the first derivative and mark the maxima in the original signal. To ensure accurate detection, only peaks close to 
these zero-crossing points are selected, helping to avoid false detections caused by noise.

Moreover, an amplitude threshold and a minimum distance between peaks are applied to avoid detecting noise. The minimum distance is automatically calculated based on the sampling
frequency (fs) and the maximum expected heart rate (max_hr). 

Since a normal resting heart rate for most people is between 60 and 100 beats per minute (BPM), the max_hr parameter is set to 100 by default to reliably detect physiological 
heartbeats while reducing false detections.
'''

def extract_systolic_peak(signal, fs, max_hr=100):
    div_ppg = np.diff(signal)
    
    zero_crossings = np.where((div_ppg[:-1] > 0) & (div_ppg[1:] < 0))[0] + 1
    if len(zero_crossings) == 0:
        return None
    
    min_distance = int((60 * fs) / max_hr)
    
    peaks_idx = find_peaks(signal, height=0.5, distance=min_distance)[0]
    
    peaks_idx = np.array([peak for peak in peaks_idx if peak in zero_crossings])
    peaks_values = signal[peaks_idx]
    
    if len(peaks_values) == 0:
        return None
    
    return peaks_idx, peaks_values

# Apply moving average filter

filtered_ppg = moving_average_filter(ppg, window_size=window_size)

# Extract systolic peaks

peaks_idx, peaks_values = extract_systolic_peak(filtered_ppg, fs, max_hr=100)



# Plot original and filtered PPG signals

plt.figure(figsize=(16, 8))
plt.plot(ppg, label='Original PPG Signal', alpha=0.5)
plt.plot(filtered_ppg, label='Filtered PPG Signal', color='red', linewidth=2)
plt.title('PPG Signal with Moving Average Filter')
plt.xlabel('Sample Number')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
save_path = os.path.join(save_dir, 'filtered_ppg_signal.png')
plt.savefig(save_path)
plt.show()
plt.close()


# Plot systolic peaks

if peaks_idx is not None:
    plt.figure(figsize=(16, 8))
    plt.plot(filtered_ppg, label='Filtered PPG Signal')
    plt.scatter(peaks_idx, peaks_values, color='red', label='Systolic Peaks')
    plt.title('Systolic Peaks in Filtered PPG Signal')
    plt.xlabel('Sample Number')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)

    save_path = os.path.join(save_dir, 'systolic_peaks_filtered_ppg.png')
    plt.savefig(save_path)
    plt.show()
    plt.close()