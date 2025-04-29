### PPG-Signal-Processing-and-Systolic-Peak-Detection-using-Elgendi's-Method

This repository contains code for preprocessing a **Photoplethysmography (PPG)** signal, smoothing it using a **moving average filter**, and detecting systolic peaks using the **Elgendi's method**.

# Introduction

Photoplethysmography (PPG) is a non-invasive technique that measures blood volume changes in the body using a light sensor.

PPG signals are widely used for monitoring heart rate and circulatory health.

A typical PPG waveform includes:

    * Systolic Peak: The highest point, representing blood ejection from the heart.

    * Dicrotic Notch: A small dip after the systolic peak, caused by closure of the aortic valve.

    * Diastolic Peak: A secondary rise after the notch, caused by the reflected blood wave.

In this project, systolic peaks are detected using the Elgendi's method, which analyzes the first derivative of the PPG signal to find points where the slope changes from positive to negative.

# Methodology

## Data Acquisition

The PPG signal was sampled at 1000 Hz and loaded from a CSV file.

## Preprocessing: Moving Average Filter

* A moving average filter is applied to remove baseline wander.

* Padding with reflection is used to handle the edges properly and maintain the full signal length.

* This is an efficient method for smoothing because the signal does not contain significant high-frequency noise.

## Systolic Peak Detection (Elgendi Method)

* The first derivative of the filtered signal is computed.

* Zero-crossings where the slope changes from positive to negative are identified as candidate systolic peaks.

* An amplitude threshold and minimum distance between peaks are applied to reduce false detections.

* The minimum distance is dynamically calculated based on the sampling frequency and the maximum expected heart rate (default 100 BPM).

# Results

Two main results are represented as followed:

* Original and Filtered PPG Signal


* Detected Systolic Peaks

The filtered signal shows that baseline wander is removed, and the detected systolic peaks clearly correspond to heartbeat events.

# Project Structure

```python
Federated-Learning-Pipeline/
  ├── peak_detection_script.py     # Main Python script for filtering and peak detection
  ├── requirements.txt             # Dependencies to run the code
  ├── filtered_ppg_signal.png      # Saved figure: Original vs. Filtered PPG
  ├── systolic_peaks_filtered_ppg.png          # Saved figure: Systolic Peaks Detection
  └── README.md            # Configuration files for the simulation (base.yaml)
```




