import numpy as np
from tkinter import filedialog, Toplevel, Tk
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from signal_generation import parse_input_file
from comparesignals import SignalSamplesAreEqual,ConvTest,corrtest
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

   # Pre-compute squared sums for normalization
    X1_squared_sum = np.sum(i**2 for i in signal1)
    X2_squared_sum = np.sum(i**2 for i in signal2)
    normalization = np.sqrt(X1_squared_sum * X2_squared_sum)

   
    r12 = []
    for j in range(N):
         numerator = sum(signal1[i] * signal2[(i + j) % N] for i in range(N))  
         r12.append(numerator / normalization)
    return r12
        

## correlation
def runCorr(root) :
    file_path = filedialog.askopenfilename()
    if not file_path:
         return 
   
    signal_type, is_periodic, indices_or_freqs, amplitudes, phase_shifts = parse_input_file(file_path)
    file_path = filedialog.askopenfilename()
    if not file_path:
       return    
    signal_type2, is_periodic2, indices_or_freqs2, amplitudes2, phase_shifts2 = parse_input_file(file_path)
    ans = normalized_cross_correlation(amplitudes, amplitudes2)
##print(ans)
    file_path = filedialog.askopenfilename()
    if not file_path:
         return   
    corrtest(file_path,range(len(ans)),ans)




