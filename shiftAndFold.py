from tkinter import filedialog, simpledialog, Toplevel
import numpy as np
import matplotlib.pyplot as plt
from signal_generation import parse_input_file
from signal_generation import parse_input_file
from comparesignals import Shift_Fold_Signal

def fold_signal(indices, amplitudes):
    #dictionary 
    folded_indices = {}

    for i, index in enumerate(indices):
        folded_index = -index  # Fold around the 0 index
        if folded_index not in folded_indices:
            folded_indices[folded_index] = 0
        folded_indices[folded_index] += amplitudes[i]

    # Convert the dictionary back to sorted lists
    folded_indices_sorted = sorted(folded_indices.keys())
    folded_amplitudes_sorted = [folded_indices[idx] for idx in folded_indices_sorted]

    return folded_indices_sorted, folded_amplitudes_sorted

def shift_signal(indices, amplitudes, shift_value, shift_right=True):

    shifted_indices = []
    for index in indices:
        if shift_right:
            shifted_indices.append(index + shift_value)
        else:
            shifted_indices.append(index - shift_value)

    return shifted_indices, amplitudes
 
def sfrun(root):
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    # Parse the signal from file
    signal_type, is_periodic, indices_or_freqs, amplitudes, phase_shifts = parse_input_file(file_path)
    # Get sampling frequency from the user
    fold = simpledialog.askinteger("Input", "do you need to fold ? enter 0 or 1")
    shift = simpledialog.askinteger("Input", "do you need to shift ? enter 0  or shift value(INT)")
    sign = 1
    if fold==1 :
        sign = -1
        indices_or_freqs,amplitudes = fold_signal(indices_or_freqs,amplitudes)
    elif fold!=0 :
      raise ValueError("the input of fold must be 0 or 1")
    if shift != 0 :
        sign *= shift
        indices_or_freqs,amplitudes = shift_signal(indices_or_freqs, amplitudes, abs(shift), shift_right=(sign<0))
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    Shift_Fold_Signal(file_path,indices_or_freqs,amplitudes)


    
