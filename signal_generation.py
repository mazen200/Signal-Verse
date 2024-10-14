import numpy as np
import matplotlib.pyplot as plt
from tkinter import Toplevel, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import interp1d
from scipy.interpolate import make_interp_spline
# Function to generate and plot sinusoidal signals in two windows
def generate_signal(amplitude_entry, phase_entry, analog_freq_entry, sampling_freq_entry, signal_type_var, root):
    try:
        signal_type = signal_type_var.get()
        amplitude = float(amplitude_entry.get())
        phase_shift = float(phase_entry.get())
        analog_freq = float(analog_freq_entry.get())
        sampling_freq = float(sampling_freq_entry.get())

        if sampling_freq < 2 * analog_freq:
            messagebox.showerror("Sampling Error", "Sampling frequency must be at least twice the analog frequency!")
            return

        t_cont = np.linspace(0, 1, 1000) # time continous x
        t_disc = np.arange(0, 1, 1/sampling_freq) # time discrete x

        if signal_type == 0: 
            signal_cont = amplitude * np.sin(2 * np.pi * analog_freq * t_cont + phase_shift)
            signal_disc = amplitude * np.sin(2 * np.pi * analog_freq * t_disc + phase_shift)
        else:                  
            signal_cont = amplitude * np.cos(2 * np.pi * analog_freq * t_cont + phase_shift)
            signal_disc = amplitude * np.cos(2 * np.pi * analog_freq * t_disc + phase_shift)

        #draw continous signal on new window
        cont_window = Toplevel(root)
        cont_window.title("Continuous Signal")
        fig_cont, ax_cont = plt.subplots()
        cubic_interpolation_model = interp1d(t_cont, signal_cont, kind = "cubic")
        ax_cont.plot(t_cont, signal_cont, label="Continuous Signal", color="blue")
        ax_cont.set_xlabel("Time")
        ax_cont.set_ylabel("Amplitude")
        ax_cont.legend()
        canvas_cont = FigureCanvasTkAgg(fig_cont, master=cont_window)
        canvas_cont.draw()
        canvas_cont.get_tk_widget().pack()

        #draw discrete signal on new window
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

        #compare
        print(SignalSamplesAreEqual("CosOutput.txt",range(len(signal_disc)),signal_disc))
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
    elif signal_type == 1:
        time_disc = time[::10]
        signal_disc = signal[::10]
        ax_disc.stem(time_disc, signal_disc, linefmt='r--', markerfmt='ro', basefmt='b', label="Discrete Signal")

    ax_disc.set_xlabel("Time" if signal_type == 0 else "Frequency")
    ax_disc.set_ylabel("Amplitude")
    ax_disc.legend()
    canvas_disc = FigureCanvasTkAgg(fig_disc, master=disc_window)
    canvas_disc.draw()
    canvas_disc.get_tk_widget().pack()


def SignalSamplesAreEqual(file_name,indices,samples):
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
                
    if len(expected_samples)!=len(samples):
        print("Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(expected_samples)):
        if abs(samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Test case failed, your signal have different values from the expected one") 
            return
    print("Test case passed successfully")