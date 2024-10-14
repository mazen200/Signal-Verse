import numpy as np
import matplotlib.pyplot as plt
from tkinter import Toplevel, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import interp1d
from scipy.interpolate import make_interp_spline
from comparesignals import SignalSamplesAreEqual
# Function to generate and plot sinusoidal signals in two windows
def generate_signal(amplitude_entry, phase_entry, analog_freq_entry, sampling_freq_entry, signal_type_var, cmpbool, root):
    try:
        signal_type = signal_type_var.get()
        amplitude = float(amplitude_entry.get())
        phase_shift = float(phase_entry.get())
        analog_freq = float(analog_freq_entry.get())
        sampling_freq = float(sampling_freq_entry.get())
        cmptemp = cmpbool.get()

        if sampling_freq < 2 * analog_freq:
            messagebox.showerror("Sampling Error", "Sampling frequency must be at least twice the analog frequency!")
            return

        num_samples_cont = 1000  # Number of continuous sample points for a smooth curve
        num_samples_disc = int(sampling_freq)  # Number of discrete samples based on sampling frequency

        # Generate continuous signal using time values
        t_cont = np.linspace(0, 1, num_samples_cont)  # Continuous time over 1 second
        sample_indices_disc = np.arange(num_samples_disc)  # Sample indices for discrete signal
        t_disc = sample_indices_disc / sampling_freq  # Discrete time based on sampling frequency

        # Generate signals based on type (sine or cosine)
        if signal_type == 0: 
            signal_cont = amplitude * np.sin(2 * np.pi * analog_freq * t_cont + phase_shift)
            signal_disc = amplitude * np.sin(2 * np.pi * analog_freq * t_disc + phase_shift)
        else:
            signal_cont = amplitude * np.cos(2 * np.pi * analog_freq * t_cont + phase_shift)
            signal_disc = amplitude * np.cos(2 * np.pi * analog_freq * t_disc + phase_shift)

        # Plot continuous signal with time on the x-axis
        cont_window = Toplevel(root)
        cont_window.title("Continuous Signal")
        fig_cont, ax_cont = plt.subplots()
        ax_cont.plot(t_cont, signal_cont, label="Continuous Signal", color="blue")
        ax_cont.set_xlabel("Time (seconds)")
        ax_cont.set_ylabel("Amplitude")
        ax_cont.legend()
        canvas_cont = FigureCanvasTkAgg(fig_cont, master=cont_window)
        canvas_cont.draw()
        canvas_cont.get_tk_widget().pack()

        # Plot discrete signal with sample indices on the x-axis
        disc_window = Toplevel(root)
        disc_window.title("Discrete Signal")
        fig_disc, ax_disc = plt.subplots()
        ax_disc.stem(sample_indices_disc, signal_disc, linefmt='r--', markerfmt='ro', basefmt='b', label="Discrete Samples")
        ax_disc.set_xlabel("Sample Index")
        ax_disc.set_ylabel("Amplitude")
        ax_disc.legend()
        canvas_disc = FigureCanvasTkAgg(fig_disc, master=disc_window)
        canvas_disc.draw()
        canvas_disc.get_tk_widget().pack()

        if cmptemp == 1:
            file_path = filedialog.askopenfilename()
            if not file_path:
                return
            print(SignalSamplesAreEqual(file_path, range(len(signal_disc)), signal_disc))

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values for all fields.")


# Function to parse the input file
def parse_input_file(file_path):
    with open(file_path, 'r') as file:
        signal_type = int(file.readline().strip())
        is_periodic = int(file.readline().strip())
        n1 = int(file.readline().strip())
        indices_or_freqs = []
        amplitudes = []
        phase_shifts = [] if signal_type == 1 else None

        for x in range(n1):
            line = file.readline().strip().split()
            index = int(line[0])
            amplitude = float(line[1])
            indices_or_freqs.append(index)
            amplitudes.append(amplitude)

            if signal_type == 1:
                phase_shift = float(line[2])
                phase_shifts.append(phase_shift)

    return signal_type, is_periodic, indices_or_freqs, amplitudes, phase_shifts

# Function to plot signal from file in two windows
def plot_signal_from_file(root):
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    
    signal_type, is_periodic, indices_or_freqs, amplitudes, phase_shifts = parse_input_file(file_path)

    cont_window = Toplevel(root)
    cont_window.title("Continuous Signal from File")
    fig_cont, ax_cont = plt.subplots()
    cubic_interpolation_model = interp1d(indices_or_freqs, amplitudes, kind = "cubic")
    x_cubic = np.linspace(min(indices_or_freqs), max(indices_or_freqs), 500)
    y_cubic = cubic_interpolation_model(x_cubic)
    if signal_type == 0:
        ax_cont.plot(x_cubic, y_cubic, label="Continuous Signal")

    ax_cont.set_xlabel("Time" if signal_type == 0 else "Frequency")
    ax_cont.set_ylabel("Amplitude")
    ax_cont.legend()
    canvas_cont = FigureCanvasTkAgg(fig_cont, master=cont_window)
    canvas_cont.draw()
    canvas_cont.get_tk_widget().pack()

    disc_window = Toplevel(root)
    disc_window.title("Discrete Signal from File")
    fig_disc, ax_disc = plt.subplots()

    if signal_type == 0:
        ax_disc.stem(indices_or_freqs, amplitudes, linefmt='r--', markerfmt='ro', basefmt='b', label="Discrete Signal")
    
    ax_disc.set_xlabel("Time" if signal_type == 0 else "Frequency")
    ax_disc.set_ylabel("Amplitude")
    ax_disc.legend()
    canvas_disc = FigureCanvasTkAgg(fig_disc, master=disc_window)
    canvas_disc.draw()
    canvas_disc.get_tk_widget().pack()