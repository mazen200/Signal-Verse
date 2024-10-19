import numpy as np
from tkinter import filedialog, Toplevel, Tk
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from signal_generation import parse_input_file
from comparesignals import SignalSamplesAreEqual
import tkinter as tk
# Function to add and subtract two signals
def add_subtract_signals(signal1, signal2):
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
    subtracted_amplitudes = [amplitudes_2[i] - amplitudes_1[i] for i in range(sz)]
    
    return added_amplitudes, subtracted_amplitudes

# Function to plot signals (added and subtracted)
def plot_added_subtracted_signals(root, added_amplitudes, subtracted_amplitudes, indices_or_freqs):
    add_window = Toplevel(root)
    add_window.title("Added Signal")
    fig_add, ax_add = plt.subplots()
    ax_add.stem(indices_or_freqs, added_amplitudes, linefmt='g--', markerfmt='go', basefmt='b', label="Added Signal")
    ax_add.set_xlabel("Sample Index")
    ax_add.set_ylabel("Amplitude")
    ax_add.legend()
    canvas_add = FigureCanvasTkAgg(fig_add, master=add_window)
    canvas_add.draw()
    canvas_add.get_tk_widget().pack()

    sub_window = Toplevel(root)
    sub_window.title("Subtracted Signal")
    fig_sub, ax_sub = plt.subplots()
    ax_sub.stem(indices_or_freqs, subtracted_amplitudes, linefmt='m--', markerfmt='mo', basefmt='b', label="Subtracted Signal")
    ax_sub.set_xlabel("Sample Index")
    ax_sub.set_ylabel("Amplitude")
    ax_sub.legend()
    canvas_sub = FigureCanvasTkAgg(fig_sub, master=sub_window)
    canvas_sub.draw()
    canvas_sub.get_tk_widget().pack()

# Function to load two files, add, subtract, and plot signals
def load_and_process_files(root):

    root2 = tk.Tk()
    root2.title("Signal Visualizer")
    root2.configure(bg="#1569C7")
    for widget in root2.winfo_children():
        widget.destroy()
    tk.Label(root2, text="compare with file ?", bg="#1569C7", fg="#E7DECC", font=("Helvetica", 12)).pack(pady=10)
    cmpbool = tk.IntVar(value=0)
    tk.Radiobutton(root2, text="NO", variable=cmpbool, value=0, bg="#1569C7", fg="black").pack()
    tk.Radiobutton(root2, text="YES", variable=cmpbool, value=1, bg="#1569C7", fg="black").pack()
    tk.Button(root2, text="Next", bg="#E7DECC", fg="#1569C7", font=("Helvetica", 12), command=lambda: start_process(root2,root,cmpbool.get())).pack(pady=10)

    
def start_process(root2,root,cmpbool):
    root2.destroy()
    file_path_1 = filedialog.askopenfilename(title="Select First Signal File")
    if not file_path_1:
        return
    file_path_2 = filedialog.askopenfilename(title="Select Second Signal File")
    if not file_path_2:
        return

    signal1 = parse_input_file(file_path_1)
    signal2 = parse_input_file(file_path_2)

    added_amplitudes, subtracted_amplitudes = add_subtract_signals(signal1, signal2)

    
    plot_added_subtracted_signals(root, added_amplitudes, subtracted_amplitudes, signal1[2])
    print(cmpbool)
    
    file_path = filedialog.askopenfilename()
    if not file_path:
       return
    print("add operation : " )
    SignalSamplesAreEqual(file_path, range(len(added_amplitudes)), added_amplitudes)
    file_path = filedialog.askopenfilename()
    if not file_path:
       return
    print("subtract operation : " )
    SignalSamplesAreEqual(file_path, range(len(subtracted_amplitudes)), subtracted_amplitudes)
     
     



