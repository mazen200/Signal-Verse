import numpy as np
from scipy.signal import firwin, freqz, lfilter
import matplotlib.pyplot as plt
from comparesignals import SignalSamplesAreEqual
from tkinter import Toplevel, messagebox, filedialog , simpledialog
import math
from signal_generation import parse_input_file
from DerivativeSignal import plot
from task6 import convolve_signals
# Reinitialize Parameters for Verification
Fs = 8000  # Sampling Frequency
Fc = 1500  # Cutoff Frequency (Hz)
Transition_Band = 500  # Transition Bandwidth (Hz)
StopBandAttenuation = 50  # Stopband Attenuation (dB)
filter_type = "lowpass"  # Filter type

def  getHVal(filter, n, fs, f1, f2 = 0):
    fc = f1
    angle = n * 2 * fc * math.pi 
    w1 = 2 * math.pi * f1 
    w2 = 2 * math.pi * f2 
    if filter == 'Low pass':
        return 2 * fc * (np.sin(angle)) / (angle) if n != 0 else 2 * fc
    
    elif filter == "High pass":
        return -2 * fc * (np.sin(angle) / angle) if n != 0 else 1 - 2 * fc
    
    elif filter == "Band pass":
        if n != 0:
            return (2 * f2 * (np.sin(n * w2) / (n * w2))) - (2 * f1 * (np.sin(n * w1) / (n * w1)))
        else:
            return 2 * (f2 - f1)
        
    elif filter == "Band stop":
        if n != 0:
            return (2 * f1 * (np.sin(n * w1) / (n * w1))) - (2 * f2 * (np.sin(n * w2) / (n * w2)))
        else:
            return 1 - 2 * (f2 - f1)


def getWindowVal(window, n, N):
    if window =="rectangular":
        return 1
    elif window == "hanning":
        return 0.5 + 0.5 * np.cos((2 * np.pi * n) / N)
    elif window == "hamming":
        return 0.54 + 0.46 * np.cos((2 * np.pi * n) / N)
    elif window == "blackman":
        return 0.42 + 0.5 * np.cos((2 * np.pi * n) / (N - 1)) + 0.08 * np.cos((4 * np.pi * n) / (N - 1))

    
def getCoeffNumber(window, deltaF):
    if window == "rectangular":
        num = math.ceil(0.9/deltaF)
    elif window == "hanning":
        num = math.ceil(3.1/deltaF)
    elif window == "hamming":
        num = math.ceil(3.3/deltaF) 
    elif window == "blackman":
        num = math.ceil(5.5/deltaF) 
    return num if num % 2 == 1 else num + 1 
 

def getWindowFunction(stopband):
    if stopband <= 21:
        return "rectangular"
    elif stopband <= 44:
        return "hanning"
    elif stopband <= 53:
        return "hamming"
    elif stopband <= 74:
        return "blackman"
    else:
        None

def calculate_FIR(sampling_freq, filter_type, cutoff_freq, cutoff1, cutoff2, transition_band, stopband_atten):
        coeff = []
        f1 = 0
        f2 = 0
        if filter_type == 'Low pass':
            f1 = (cutoff_freq + transition_band / 2) / sampling_freq
  
        elif filter_type == "High pass":
            f1 = (cutoff_freq - transition_band / 2) / sampling_freq

        elif filter_type == "Band pass":
            f1 = (cutoff1 - transition_band / 2) / sampling_freq
            f2 = (cutoff2 + transition_band / 2) / sampling_freq

        elif filter_type == "Band stop":
            f1 = (cutoff1 + transition_band / 2) / sampling_freq
            f2 = (cutoff2 - transition_band / 2) / sampling_freq
        deltaF = transition_band / sampling_freq
        window = getWindowFunction(stopband_atten)
        N = getCoeffNumber(window, deltaF)
        edge = int((N-1)/2)
        # coeff = getCoeff(edge, filter_type, window, sampling_freq, f1, N, f2)
        for i in range(0, int(edge)+1):
             coeff.append(round(getHVal(filter_type, i, sampling_freq, f1, f2) * getWindowVal(window, i, N), 11))

        negativeVal = coeff[1:]
        negativeVal.reverse()
        coeff = negativeVal + coeff   
        indicies = [i for i in range(-1*edge, edge+1)]
        return indicies,coeff
       


def run_filter(root,check, sampling_freq, filter_type, cutoff_freq, cutoff1, cutoff2, transition_band, stopband_atten):
    # check = 1 signal
    #check = 0 no signal
    if check == 1:
        file_path = filedialog.askopenfilename()
        if not file_path:
           return
        signal_type, is_periodic, indices_or_freqs, amplitudes, phase_shifts = parse_input_file(file_path)

    ind , coff  = calculate_FIR(int(sampling_freq), filter_type, int(cutoff_freq), int(cutoff1),int( cutoff2), int(transition_band), int(stopband_atten))
    if check == 0 :
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        SignalSamplesAreEqual(file_path, ind, coff)
        plot(root,coff,"FIR coffecients")
    else :
        indi,ans = convolve_signals(indices_or_freqs, amplitudes,ind, coff)
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        SignalSamplesAreEqual(file_path, indi,ans)
        plot(root,ans,"Filterd signal")

