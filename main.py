import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Function to generate and plot sinusoidal signals in two windows
def generate_signal():
    try:
        signal_type = signal_type_var.get()
        amplitude = float(amplitude_entry.get())
        phase_shift = float(phase_entry.get())
        analog_freq = float(analog_freq_entry.get())
        sampling_freq = float(sampling_freq_entry.get())

        if sampling_freq < 2 * analog_freq:
            messagebox.showerror("Sampling Error", "Sampling frequency must be at least twice the analog frequency!")
            return

        # Time array for continuous signal (fine resolution for smooth plot)
        t_cont = np.linspace(0, 1, 1000)  # Continuous time
        # Time array for discrete signal (samples based on sampling frequency)
        t_disc = np.arange(0, 1, 1/sampling_freq)

        if signal_type == 0:  # Sine wave
            signal_cont = amplitude * np.sin(2 * np.pi * analog_freq * t_cont + phase_shift)
            signal_disc = amplitude * np.sin(2 * np.pi * analog_freq * t_disc + phase_shift)
        else:  # Cosine wave
            signal_cont = amplitude * np.cos(2 * np.pi * analog_freq * t_cont + phase_shift)
            signal_disc = amplitude * np.cos(2 * np.pi * analog_freq * t_disc + phase_shift)

        # Create a new window for continuous signal
        cont_window = Toplevel(root)
        cont_window.title("Continuous Signal")
        fig_cont, ax_cont = plt.subplots()
        ax_cont.plot(t_cont, signal_cont, label="Continuous Signal", color="blue")
        ax_cont.set_xlabel("Time")
        ax_cont.set_ylabel("Amplitude")
        ax_cont.legend()
        canvas_cont = FigureCanvasTkAgg(fig_cont, master=cont_window)
        canvas_cont.draw()
        canvas_cont.get_tk_widget().pack()

        # Create a new window for discrete signal
        disc_window = Toplevel(root)
        disc_window.title("Discrete Signal")
        fig_disc, ax_disc = plt.subplots()
        ax_disc.stem(t_disc, signal_disc, linefmt='r--', markerfmt='ro', basefmt='b', label="Discrete Samples")
        ax_disc.set_xlabel("Time")
        ax_disc.set_ylabel("Amplitude")
        ax_disc.legend()
        canvas_disc = FigureCanvasTkAgg(fig_disc, master=disc_window)
        canvas_disc.draw()
        canvas_disc.get_tk_widget().pack()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values for all fields.")

# Function to parse the input file
def parse_input_file(file_path):
    with open(file_path, 'r') as file:
        signal_type = int(file.readline().strip())  # 0 for Time domain, 1 for Frequency domain
        is_periodic = int(file.readline().strip())  # 0 or 1
        n1 = int(file.readline().strip())  # Number of samples
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
def plot_signal_from_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    
    signal_type, is_periodic, indices_or_freqs, amplitudes, phase_shifts = parse_input_file(file_path)

    # Create continuous signal window
    cont_window = Toplevel(root)
    cont_window.title("Continuous Signal from File")
    fig_cont, ax_cont = plt.subplots()
    
    if signal_type == 0:  # Time domain
        ax_cont.plot(indices_or_freqs, amplitudes, label="Continuous Signal")
    elif signal_type == 1:  # Frequency domain
        time = np.linspace(0, 1, 500)
        signal = np.zeros_like(time)
        for freq, amp, phase in zip(indices_or_freqs, amplitudes, phase_shifts):
            signal += amp * np.cos(2 * np.pi * freq * time + phase)
        ax_cont.plot(time, signal, label="Continuous Signal")

    ax_cont.set_xlabel("Time" if signal_type == 0 else "Frequency")
    ax_cont.set_ylabel("Amplitude")
    ax_cont.legend()
    canvas_cont = FigureCanvasTkAgg(fig_cont, master=cont_window)
    canvas_cont.draw()
    canvas_cont.get_tk_widget().pack()

    # Create discrete signal window
    disc_window = Toplevel(root)
    disc_window.title("Discrete Signal from File")
    fig_disc, ax_disc = plt.subplots()

    if signal_type == 0:  # Time domain
        ax_disc.stem(indices_or_freqs, amplitudes, linefmt='r--', markerfmt='ro', basefmt='b', label="Discrete Signal")
    elif signal_type == 1:  # Frequency domain
        time_disc = time[::10]
        signal_disc = signal[::10]
        ax_disc.stem(time_disc, signal_disc, linefmt='r--', markerfmt='ro', basefmt='b', label="Discrete Signal")

    ax_disc.set_xlabel("Time" if signal_type == 0 else "Frequency")
    ax_disc.set_ylabel("Amplitude")
    ax_disc.legend()
    canvas_disc = FigureCanvasTkAgg(fig_disc, master=disc_window)
    canvas_disc.draw()
    canvas_disc.get_tk_widget().pack()

# Function to create signal generation interface
def task_one_interface():
    for widget in root.winfo_children():
        widget.destroy()

    global left_frame
    left_frame = tk.Frame(root, bg="#97CADB")
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Left Frame: User input signal generation
    tk.Label(left_frame, text="Amplitude (A):", bg="#97CADB", fg="white", font=("Helvetica", 12)).pack(pady=10)
    global amplitude_entry
    amplitude_entry = tk.Entry(left_frame)
    amplitude_entry.pack(pady=5)

    tk.Label(left_frame, text="Phase Shift (θ in radians):", bg="#97CADB", fg="white", font=("Helvetica", 12)).pack(pady=10)
    global phase_entry
    phase_entry = tk.Entry(left_frame)
    phase_entry.pack(pady=5)

    tk.Label(left_frame, text="Analog Frequency (Hz):", bg="#97CADB", fg="white", font=("Helvetica", 12)).pack(pady=10)
    global analog_freq_entry
    analog_freq_entry = tk.Entry(left_frame)
    analog_freq_entry.pack(pady=5)

    tk.Label(left_frame, text="Sampling Frequency (Hz):", bg="#97CADB", fg="white", font=("Helvetica", 12)).pack(pady=10)
    global sampling_freq_entry
    sampling_freq_entry = tk.Entry(left_frame)
    sampling_freq_entry.pack(pady=5)

    tk.Label(left_frame, text="Signal Type:", bg="#97CADB", fg="white", font=("Helvetica", 12)).pack(pady=10)
    global signal_type_var
    signal_type_var = tk.IntVar(value=0)
    tk.Radiobutton(left_frame, text="Sine", variable=signal_type_var, value=0, bg="#97CADB", fg="#1569C7").pack()
    tk.Radiobutton(left_frame, text="Cosine", variable=signal_type_var, value=1, bg="#97CADB", fg="#1569C7").pack()

    generate_button = tk.Button(left_frame, text="Generate Signal", bg="#1569C7", fg="white", font=("Helvetica", 12), command=generate_signal)
    generate_button.pack(pady=20)

    # Right Frame: File-based signal plotting
    tk.Button(left_frame, text="Upload Signal File", bg="#1569C7", fg="white", font=("Helvetica", 12), command=plot_signal_from_file).pack(pady=20)

    # Add Back to Home button
    back_button = tk.Button(left_frame, text="Back to Home", bg="#1569C7", fg="white", font=("Helvetica", 12), command=home_page)
    back_button.pack(pady=20)

# Function to show the home page
def home_page():
    for widget in root.winfo_children():
        widget.destroy()

    welcome_label = tk.Label(root, text="Welcome to Visualizer", bg="#1569C7", fg="white", font=("Helvetica", 24))
    welcome_label.pack(pady=50, fill=tk.X)

    task_one_button = tk.Button(root, text="Task One", bg="white", fg="#1569C7", font=("Helvetica", 14), command=task_one_interface)
    task_one_button.pack(pady=20)

# Initialize Tkinter window
root = tk.Tk()
root.title("Signal Visualizer")
root.geometry("800x600")
root.configure(bg="#1569C7")

# Show home page
home_page()

root.mainloop()
