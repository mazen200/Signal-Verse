import numpy as np
from tkinter import filedialog, Toplevel, Tk
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from signal_generation import parse_input_file
from comparesignals import SignalSamplesAreEqual
from fourier import convert
def moving_average(signal, window_size):
    """
    Compute moving average y(n) for signal x(n) with the specified window size.
    """
    smoothed_signal = []
    N = len(signal)
    
    for i in range(N):
        start_index = max(0, i - window_size // 2)
        end_index = min(N, i + window_size // 2 + 1)
        window = signal[start_index:end_index]
        smoothed_signal.append(sum(window) / len(window))
    
    return smoothed_signal

def remove_dc_time(signal):
    """
    Removes the DC component (mean) from the signal in the time domain.
    """
    mean_value = sum(signal) / len(signal)
    return [x - mean_value for x in signal]

def remove_dc_frequency(signal):
    """
    Removes the DC component from the signal in the frequency domain.
    """
    # Compute DFT
    N = len(signal)
    dft_result = convert(signal,1)
    
    # Set the DC component (first element) to 0
    dft_result[0] = 0
    
    # Perform IDFT to get back the time-domain signal
    reconstructed_signal = convert(dft_result, 0)
    
    return reconstructed_signal

def convolve_signals(signal1, signal2):
    """
    Computes the convolution of two signals.
    """
    N1 = len(signal1)
    N2 = len(signal2)
    result_length = N1 + N2 - 1
    result = [0] * result_length
    
    for i in range(result_length):
        for j in range(N1):
            if 0 <= i - j < N2:
                result[i] += signal1[j] * signal2[i - j]
    
    return result

def normalized_cross_correlation(signal1, signal2):
    """
    Computes the normalized cross-correlation of two signals.
    """
    N = len(signal1)
    mean1 = sum(signal1) / N
    mean2 = sum(signal2) / N
    
    numerator = sum((signal1[i] - mean1) * (signal2[i] - mean2) for i in range(N))
    denominator = (
        (sum((signal1[i] - mean1) ** 2 for i in range(N)) * 
         sum((signal2[i] - mean2) ** 2 for i in range(N))) ** 0.5
    )
    
    return numerator / denominator if denominator != 0 else 0



