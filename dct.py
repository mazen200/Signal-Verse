from tkinter import filedialog, simpledialog, Toplevel
import numpy as np
import matplotlib.pyplot as plt
from signal_generation import parse_input_file
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from signal_generation import parse_input_file
from comparesignals import SignalSamplesAreEqual
import matplotlib.pyplot as plt

def compute_dct(signal):
   
    N = len(signal)
    dct_result = []
    
    for k in range(N):
        sum_value = 0
        for n in range(N):
            angle = np.pi * k * (2 * n + 1) / (2 * N)
            sum_value += signal[n] * np.cos(angle)
        
        # Scale the result for normalization
        coefficient = np.sqrt(2 / N) if k > 0 else np.sqrt(1 / N)
        dct_result.append(coefficient * sum_value)
    
    return dct_result