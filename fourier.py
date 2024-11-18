from tkinter import filedialog, simpledialog, Toplevel
import numpy as np
import matplotlib.pyplot as plt
from signal_generation import parse_input_file
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from signal_generation import parse_input_file
from comparesignals import SignalSamplesAreEqual
import matplotlib.pyplot as plt
import math

#Use to test the Amplitude of DFT and IDFT
def SignalComapreAmplitude(SignalInput = [] ,SignalOutput= []):
    if len(SignalInput) != len(SignalInput):
        return False
    else:
        for i in range(len(SignalInput)):
            if abs(SignalInput[i]-SignalOutput[i])>0.001:
                return False
            elif SignalInput[i]!=SignalOutput[i]:
                return False
        return True

def RoundPhaseShift(P):
    while P<0:
        p+=2*math.pi
    return float(P%(2*math.pi))

#Use to test the PhaseShift of DFT
def SignalComaprePhaseShift(SignalInput = [] ,SignalOutput= []):
    if len(SignalInput) != len(SignalInput):
        return False
    else:
        for i in range(len(SignalInput)):
            A=round(SignalInput[i])
            B=round(SignalOutput[i])
            if abs(A-B)>0.0001:
                return False
            elif A!=B:
                return False
        return True
def convert(signal,check):
    """Computes the DFT manually and returns complex result, magnitudes, and phases."""
    # check = 1 dft else idft

    N = len(signal)
    result = []
    
    for k in range(N):
        sum_value = 0
        for n in range(N):
            angle = (-1 if check else 1) * 2j * np.pi * k * n / N
            sum_value += signal[n] * np.exp(angle)
        result.append(sum_value/(1 if check else N))
    
    # Convert to numpy array for easier processing
    result = np.array(result)
    if check ==  0:
        return result.real
    # Calculate magnitudes and phases
    magnitudes = np.abs(result)
    phases = np.arctan2(np.imag(result), np.real(result))
    return result, magnitudes, phases

def reconstruct_dft_from_magnitudes_phases(magnitudes, phases):
    """Reconstructs the DFT result from magnitudes and phases."""
    result = []
    
    for magnitude, phase in zip(magnitudes, phases):
        # Compute the real and imaginary parts
        real_part = magnitude * np.cos(phase)
        imag_part = magnitude * np.sin(phase)
        
        # Combine real and imaginary parts to form the complex number
        complex_value = real_part + 1j * imag_part
        result.append(complex_value)
    
    return np.array(result)

def format_number(num):
    """Formats a number to remove unnecessary decimal places if it's an integer."""
    return f"{num:.13f}f" if num != int(num) else f"{int(num)}"
def plot2(root,freq,amplitudes,title) :
    omega = 2*np.pi*freq/len(amplitudes)
    disc_window = Toplevel(root)
    disc_window.title(title)
    fig_disc, ax_disc = plt.subplots()
    sample_indices = range(len(amplitudes))
    frequencies = []
    for i in sample_indices :
        frequencies.append((i+1)*omega)
    k = min(10, len(sample_indices))
    ax_disc.stem(frequencies[:k], amplitudes[:k], linefmt='r--', markerfmt='ro', basefmt='b', label="Discrete Signal")   
    ax_disc.set_xlabel("frequencies")
    ax_disc.set_ylabel(title)
    ax_disc.legend()
    canvas_disc = FigureCanvasTkAgg(fig_disc, master=disc_window)
    canvas_disc.draw()
    canvas_disc.get_tk_widget().pack()
def dft(root):
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    # Parse the signal from file
    signal_type, is_periodic, indices_or_freqs, amplitudes, phase_shifts = parse_input_file(file_path)
    
     # Get sampling frequency from the user
    sampling_frequency = simpledialog.askfloat("Input", "Enter the sampling frequency in Hz:")
    # Apply Fourier Transform (manual DFT)
    dft_result, magnitudes, phases = convert(amplitudes,1)
    plot2(root,sampling_frequency,magnitudes,"magnitudes")
    plot2(root,sampling_frequency,phases,"phases")
   # print(dft_result)
    # Save results to a file in the requested format
    save_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if save_file_path:
        with open(save_file_path, 'w') as file:
             #Write the first three lines (signal_type, transformed flag (1), n1)
            file.write(f"{signal_type}\n")
            file.write(f"{1}\n")  # Fourier-transformed flag (1)
            file.write(f"{len(amplitudes)}\n")
            
             #Write magnitude and phase for each frequency component
            for magnitude, phase in zip(magnitudes, phases):
                file.write(f"{format_number(magnitude)} {format_number(phase)}\n")

        print(f"Fourier Transform results saved to {save_file_path}")
    
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    # Parse the signal from file
    exmagnitudes,exphases = parse_input_file2(file_path)
    print(SignalComaprePhaseShift(exphases ,exphases))
    print(SignalComapreAmplitude(exmagnitudes,magnitudes))
# Function to parse the input file
def parse_input_file2(file_path):
    with open(file_path, 'r') as file:
        signal_type = int(file.readline().strip())
        is_periodic = int(file.readline().strip())
        n1 = int(file.readline().strip())
        amp = []
        phase = []

        for x in range(n1):
            values = file.readline().strip().split(',')
            if len(values) == 2:  # Check if there are exactly 2 values
               amp.append(round(float(values[0].replace('f', '')),10))
               phase.append(round(float(values[1].replace('f', '')),10))  # Remove 'f' if it's there
    return amp,phase
def plot(root,amplitudes) :
    disc_window = Toplevel(root)
    disc_window.title("IDFT result")
    fig_disc, ax_disc = plt.subplots()
    sample_indices = range(len(amplitudes))
    k = min(10, len(sample_indices))
    ax_disc.stem(sample_indices[:k], amplitudes[:k], linefmt='r--', markerfmt='ro', basefmt='b', label="Discrete Signal")   
    ax_disc.set_xlabel("sample index")
    ax_disc.set_ylabel("Amplitude")
    ax_disc.legend()
    canvas_disc = FigureCanvasTkAgg(fig_disc, master=disc_window)
    canvas_disc.draw()
    canvas_disc.get_tk_widget().pack()
def idft(root):
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    # Parse the signal from file
    magnitudes,phases = parse_input_file2(file_path)
    #print(magnitudes,phases)
    # Apply Fourier Transform (manual DFT)
    t =  reconstruct_dft_from_magnitudes_phases(magnitudes, phases)
   # print(t)
    amp = convert(np.array(t),0)
    print([round(i, 2) for i in amp])
    #print(amp)
   # file_path = filedialog.askopenfilename()
    #if not file_path:
     #   return
    #print(SignalSamplesAreEqual(file_path, range(len(amp)), amp))
    #plot(root,amp)