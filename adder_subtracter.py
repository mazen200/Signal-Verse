import numpy as np
from tkinter import filedialog, Toplevel, Tk
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from signal_generation import parse_input_file
from comparesignals import SignalSamplesAreEqual
import tkinter as tk


def subtract_signals(signal1, signal2):
    indices_or_freqs_1, amplitudes_1 = signal1[2], signal1[3]
    indices_or_freqs_2, amplitudes_2 = signal2[2], signal2[3]
    #print(len(amplitudes_1))
    #print(len(amplitudes_2))
    while len(amplitudes_1) < len(amplitudes_2) :
        amplitudes_1.append(0)
    while len(amplitudes_2) < len(amplitudes_1) :
        amplitudes_2.append(0)    
    #  print(len(amplitudes_1))
    # print(len(amplitudes_2))
    sz = len(amplitudes_2)
    subtracted_amplitudes = [amplitudes_2[i] - amplitudes_1[i] for i in range(sz)]   
    return subtracted_amplitudes

def add_signals(signal1,signal2) :
    indices_or_freqs_1, amplitudes_1 = signal1[2], signal1[3]
    indices_or_freqs_2, amplitudes_2 = signal2[2], signal2[3]
    #print(len(amplitudes_1))
    #print(len(amplitudes_2))
    while len(amplitudes_1) < len(amplitudes_2) :
        amplitudes_1.append(0)
    while len(amplitudes_2) < len(amplitudes_1) :
        amplitudes_2.append(0)    
    #  print(len(amplitudes_1))
    # print(len(amplitudes_2))
    sz = len(amplitudes_2)
    added_amplitudes = [amplitudes_1[i] + amplitudes_2[i] for i in range(sz)]
    return added_amplitudes

# Function to plot signals (added and subtracted)
def plot_added_subtracted_signals(root,amplitudes, indices_or_freqs):
    cont_window = Toplevel(root)
    cont_window.title("Continuous Signal from File")
    fig_cont, ax_cont = plt.subplots()
    cubic_interpolation_model = interp1d(indices_or_freqs, amplitudes, kind = "cubic")
    x_cubic = np.linspace(min(indices_or_freqs), max(indices_or_freqs), 500)
    y_cubic = cubic_interpolation_model(x_cubic)
    
    ax_cont.plot(x_cubic, y_cubic, label="Continuous Signal")

    ax_cont.set_xlabel("Time")
    ax_cont.set_ylabel("Amplitude")
    ax_cont.legend()
    canvas_cont = FigureCanvasTkAgg(fig_cont, master=cont_window)
    canvas_cont.draw()
    canvas_cont.get_tk_widget().pack()

    disc_window = Toplevel(root)
    disc_window.title("Discrete Signal from File")
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

# Function to load two files, add, subtract, and plot signals
def load_and_process_files(root):

    root2 = tk.Tk()
    root2.title("Signal Visualizer")
    root2.configure(bg="#1569C7")
    for widget in root2.winfo_children():
        widget.destroy()
    tk.Button(root2, text="add", bg="#E7DECC", fg="#1569C7", font=("Helvetica", 12), command=lambda: start_process(root2,root,1)).pack(pady=10)
    tk.Button(root2, text="subtract", bg="#E7DECC", fg="#1569C7", font=("Helvetica", 12), command=lambda: start_process(root2,root,0)).pack(pady=10)

    
def start_process(root2,root,add):
    root2.destroy()
    file_path_1 = filedialog.askopenfilename(title="Select First Signal File")
    if not file_path_1:
        return
    file_path_2 = filedialog.askopenfilename(title="Select Second Signal File")
    if not file_path_2:
        return

    signal1 = parse_input_file(file_path_1)
    signal2 = parse_input_file(file_path_2)

    amplitudes= add_signals(signal1, signal2) if add == 1 else subtract_signals(signal1 , signal2)

    
    plot_added_subtracted_signals(root, amplitudes, signal1[2])
    
    
    file_path = filedialog.askopenfilename()
    if not file_path:
       return
    SignalSamplesAreEqual(file_path, range(len(amplitudes)), amplitudes)
    
    
     
     



