from tkinter import filedialog, simpledialog, Toplevel
import numpy as np
import matplotlib.pyplot as plt
from signal_generation import parse_input_file
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import interp1d
from QuanTest import QuantizationTest1,QuantizationTest2
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
    indices = []
    for amplitude in amplitudes: 
        # Find the range index the amplitude falls into
        range_index = int((amplitude - min_amp) // delta)
        # Clamp the index to avoid overflow in the case of exact max_amp
        range_index = min(range_index, levels - 1)
        quantized_amplitudes.append(midpoints[range_index])
        indices.append(range_index + 1)

    return quantized_amplitudes,indices

def calculate_quantization_error(original_amplitudes, quantized_amplitudes):
    """Calculates the quantization error."""
    return [ quantized-original for original, quantized in zip(original_amplitudes, quantized_amplitudes)]
def calc_log(n):
    n-=1
    cnt = 0
    while n > 0:
        cnt+=1
        n = n // 2
    return cnt
def decimal_to_binary(n,bitcount):
    if n == 0:
        return "0".zfill(bitcount)
    binary = ""
    while n > 0:
        binary = str(n % 2) + binary
        n = n // 2
   # print(bitcount)  
    return binary.zfill(bitcount)

def encode_signal(indices,levels):
    bitcount = calc_log(levels)
    return [decimal_to_binary(i-1,bitcount) for i in indices]       

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
    quantized_amplitudes,indices = quantize_signal(amplitudes, levels)

    # Calculate quantization error
    quantization_error = calculate_quantization_error(amplitudes, quantized_amplitudes)

    # Encode the quantized signal
    encoded_signal = encode_signal(indices,levels)
  #  print(encoded_signal)
    # Save results to a file in the requested format

    # Ask the user for test case
    user_input = simpledialog.askinteger("Input", "test case one or two (1 or 2)")

   
    compare_file_path = filedialog.askopenfilename()
    if not compare_file_path:
            return
    
       #     (file_name,Your_IntervalIndices,encoded_signal,quantized_amplitudes,quantization_error)
   # save_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

    #if save_file_path:
     #   with open(save_file_path, 'w') as file:
      #      # Write the first three lines (signal_type, is_periodic, n1)
       #     file.write(f"{signal_type}\n")
        #    file.write(f"{is_periodic}\n")
         #   file.write(f"{len(indices_or_freqs)}\n")

            # Write quantized data: index, encoded value, quantized value, quantization error
          #  for i, (index, q_amp, encoded, error) in enumerate(zip(indices, quantized_amplitudes, encoded_signal, quantization_error)):
           #     file.write(f"{index} {encoded} {q_amp:.3f} {error:.3f}\n")

        #print(f"Quantized signal, quantization error, and encoded signal saved to {save_file_path}")
    if user_input == 1:
       QuantizationTest1(compare_file_path,encoded_signal,quantized_amplitudes)
    else:
        QuantizationTest2(compare_file_path,indices,encoded_signal,quantized_amplitudes,quantization_error)
    
    