import numpy as np
from tkinter import filedialog, Toplevel, Tk
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from signal_generation import parse_input_file
from comparesignals import SignalSamplesAreEqual
from tkinter import simpledialog
import tkinter as tk

def normalize_signal(amplitudes, mode):
    """Normalizes the signal amplitudes to the range -1 to 1 or 0 to 1."""
    min_amp = min(amplitudes)
    max_amp = max(amplitudes)

    if mode == "0 to 1":
        # Normalize to [0, 1]
        return [(amplitude - min_amp) / (max_amp - min_amp) for amplitude in amplitudes]
    elif mode == "-1 to 1":
        # Normalize to [-1, 1]
        return [2 * (amplitude - min_amp) / (max_amp - min_amp) - 1 for amplitude in amplitudes]

def normalize_and_plot_signal(root):
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    # Parse the signal from file
    signal_type, is_periodic, indices_or_freqs, amplitudes, phase_shifts = parse_input_file(file_path)

    # Ask the user for normalization range choice
    mode = simpledialog.askstring("Input", "Enter normalization mode (0 to 1 or -1 to 1):")
    if mode not in ["0 to 1", "-1 to 1"]:
        return  # Exit if invalid mode is provided

    # Normalize the signal's amplitudes
    amplitudes = normalize_signal(amplitudes, mode)

    # Continuous signal plotting
    cont_window = Toplevel(root)
    cont_window.title(f"Continuous Signal (Normalized {mode})")
    fig_cont, ax_cont = plt.subplots()
    cubic_interpolation_model = interp1d(indices_or_freqs, amplitudes, kind="cubic")
    x_cubic = np.linspace(min(indices_or_freqs), max(indices_or_freqs), 500)
    y_cubic = cubic_interpolation_model(x_cubic)

    if signal_type == 0:
        ax_cont.plot(x_cubic, y_cubic, label=f"Continuous Signal (Normalized {mode})")

    ax_cont.set_xlabel("Time" if signal_type == 0 else "Frequency")
    ax_cont.set_ylabel("Amplitude")
    ax_cont.legend()
    canvas_cont = FigureCanvasTkAgg(fig_cont, master=cont_window)
    canvas_cont.draw()
    canvas_cont.get_tk_widget().pack()

    # Discrete signal plotting
    disc_window = Toplevel(root)
    disc_window.title(f"Discrete Signal (Normalized {mode})")
    fig_disc, ax_disc = plt.subplots()

    # Plotting against sample index
    sample_indices = range(len(amplitudes))
    ax_disc.stem(sample_indices, amplitudes, linefmt='r--', markerfmt='ro', basefmt='b', label=f"Discrete Signal (Normalized {mode})")

    ax_disc.set_xlabel("Sample Index")
    ax_disc.set_ylabel("Amplitude")
    ax_disc.legend()
    canvas_disc = FigureCanvasTkAgg(fig_disc, master=disc_window)
    canvas_disc.draw()
    canvas_disc.get_tk_widget().pack()
