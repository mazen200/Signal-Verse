from tkinter import filedialog, simpledialog, Toplevel
import numpy as np
import matplotlib.pyplot as plt
from signal_generation import parse_input_file
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import interp1d
def quantize_signal(amplitudes, levels):
    """Quantizes the signal amplitudes to the specified number of levels using range midpoints."""
    min_amp = min(amplitudes)
    max_amp = max(amplitudes)

    # Define delta
    delta = (max_amp - min_amp) / levels

    # Calculate midpoints for each range
    midpoints = [(min_amp + delta * (i + 0.5)) for i in range(levels)]

    # Assign each amplitude to the closest midpoint based on which range it falls into
    quantized_amplitudes = []
    for amplitude in amplitudes:
        # Find the range index the amplitude falls into
        range_index = int((amplitude - min_amp) // delta)
        # Clamp the index to avoid overflow in the case of exact max_amp
        range_index = min(range_index, levels - 1)
        quantized_amplitudes.append(midpoints[range_index])

    return quantized_amplitudes

def calculate_quantization_error(original_amplitudes, quantized_amplitudes):
    """Calculates the quantization error."""
    return [original - quantized for original, quantized in zip(original_amplitudes, quantized_amplitudes)]

def encode_signal(quantized_amplitudes, levels):
    """Encodes the quantized signal into binary starting from 0 up to n-1."""
    num_bits = int(np.ceil(np.log2(levels)))  # Calculate bits from levels
    level_map = {value: i for i, value in enumerate(sorted(set(quantized_amplitudes)))}
    encoded_signal = [format(level_map[amp], f'0{num_bits}b') for amp in quantized_amplitudes]

    return encoded_signal

def quantize_and_save_signal(root):
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    # Parse the signal from file
    signal_type, is_periodic, indices_or_freqs, amplitudes, phase_shifts = parse_input_file(file_path)

    # Ask the user for quantization levels or bits
    user_input = simpledialog.askstring("Input", "Enter number of levels or bits (prefix bits with 'b', e.g., 'b3'):")

    if user_input.startswith('b'):
        num_bits = int(user_input[1:])
        levels = 2 ** num_bits  # Calculate levels from bits
    else:
        levels = int(user_input)

    # Quantize the signal
    quantized_amplitudes = quantize_signal(amplitudes, levels)

    # Calculate quantization error
    quantization_error = calculate_quantization_error(amplitudes, quantized_amplitudes)

    # Encode the quantized signal
    encoded_signal = encode_signal(quantized_amplitudes, levels)

    # Save results to a file in the requested format
    save_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

    if save_file_path:
        with open(save_file_path, 'w') as file:
            # Write the first three lines (signal_type, is_periodic, n1)
            file.write(f"{signal_type}\n")
            file.write(f"{is_periodic}\n")
            file.write(f"{len(indices_or_freqs)}\n")

            # Write quantized data: index, encoded value, quantized value, quantization error
            for i, (index, q_amp, encoded, error) in enumerate(zip(indices_or_freqs, quantized_amplitudes, encoded_signal, quantization_error)):
                file.write(f"{index} {encoded} {q_amp:.3f} {error:.3f}\n")

        print(f"Quantized signal, quantization error, and encoded signal saved to {save_file_path}")