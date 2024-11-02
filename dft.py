from tkinter import filedialog, simpledialog, Toplevel
import numpy as np
import matplotlib.pyplot as plt
from signal_generation import parse_input_file
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def compute_dft_manual(signal):
    """Computes the DFT manually and returns complex result, magnitudes, and phases."""
    N = len(signal)
    dft_result = []
    
    for k in range(N):
        sum_value = 0
        for n in range(N):
            angle = -2j * np.pi * k * n / N
            sum_value += signal[n] * np.exp(angle)
        dft_result.append(sum_value)
    
    # Convert to numpy array for easier processing
    dft_result = np.array(dft_result)
    
    # Calculate magnitudes and phases
    magnitudes = np.abs(dft_result)
    phases = np.angle(dft_result)
    
    return dft_result, magnitudes, phases

def fourier_transform_and_save(root):
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    # Parse the signal from file
    signal_type, is_periodic, indices_or_freqs, amplitudes, phase_shifts = parse_input_file(file_path)
    
    # Get sampling frequency from the user
    sampling_frequency = simpledialog.askfloat("Input", "Enter the sampling frequency in Hz:")
    
    # Apply Fourier Transform (manual DFT)
    dft_result, magnitudes, phases = compute_dft_manual(amplitudes)

    # Save results to a file in the requested format
    save_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

    if save_file_path:
        with open(save_file_path, 'w') as file:
            # Write the first three lines (signal_type, transformed flag (1), n1)
            file.write(f"{signal_type}\n")
            file.write(f"{1}\n")  # Fourier-transformed flag (1)
            file.write(f"{len(amplitudes)}\n")
            
            # Write magnitude and phase for each frequency component
            for magnitude, phase in zip(magnitudes, phases):
                file.write(f"{magnitude:.13f}f {phase:.13f}f\n")

        print(f"Fourier Transform results saved to {save_file_path}")