import tkinter as tk
from signal_generation import generate_signal, plot_signal_from_file
from adder_subtracter import load_and_process_files
from quantization import quantize_and_save_signal
from fourier import dft, idft
from shiftAndFold import sfrun
from DerivativeSignal import DerivativeSignal
from dct import dctrun
from task6 import runCorr,runConv
# Function to create signal generation interface
def task_one_interface():
    root = tk.Tk()
    root.title("Signal Visualizer")
    root.geometry("400x550")
    root.configure(bg="#1569C7")
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="white")  # Set the background color to white

    left_frame = tk.Frame(root, bg="white")  # Change frame background to white
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Labels with the same color as buttons
    tk.Label(left_frame, text="Amplitude (A):", bg="white", fg="#1569C7", font=("Helvetica", 12)).pack(pady=10)
    amplitude_entry = tk.Entry(left_frame)
    amplitude_entry.pack(pady=5)

    tk.Label(left_frame, text="Phase Shift (θ in radians):", bg="white", fg="#1569C7", font=("Helvetica", 12)).pack(pady=10)
    phase_entry = tk.Entry(left_frame)
    phase_entry.pack(pady=5)

    tk.Label(left_frame, text="Analog Frequency (Hz):", bg="white", fg="#1569C7", font=("Helvetica", 12)).pack(pady=10)
    analog_freq_entry = tk.Entry(left_frame)
    analog_freq_entry.pack(pady=5)

    tk.Label(left_frame, text="Sampling Frequency (Hz):", bg="white", fg="#1569C7", font=("Helvetica", 12)).pack(pady=10)
    sampling_freq_entry = tk.Entry(left_frame)
    sampling_freq_entry.pack(pady=5)

    tk.Label(left_frame, text="Signal Type:", bg="white", fg="#1569C7", font=("Helvetica", 12)).pack(pady=10)
    signal_type_var = tk.IntVar(value=0)
    tk.Radiobutton(left_frame, text="Sine", variable=signal_type_var, value=0, bg="white", fg="#1569C7").pack()
    tk.Radiobutton(left_frame, text="Cosine", variable=signal_type_var, value=1, bg="white", fg="#1569C7").pack()
    
    tk.Label(left_frame, text="compare with file ?", bg="white", fg="#1569C7", font=("Helvetica", 12)).pack(pady=10)
    cmpbool = tk.IntVar(value=0)
    tk.Radiobutton(left_frame, text="NO", variable=cmpbool, value=0, bg="white", fg="#1569C7").pack()
    tk.Radiobutton(left_frame, text="YES", variable=cmpbool, value=1, bg="white", fg="#1569C7").pack()

    generate_button = tk.Button(left_frame, text="Generate Signal", bg="#1569C7", fg="white", font=("Helvetica", 12),
                                command=lambda: generate_signal(amplitude_entry, phase_entry, analog_freq_entry, sampling_freq_entry, signal_type_var,cmpbool, root))
    generate_button.pack(pady=20)   

# Function to create signal generation interface
def upload_signal_options():
    root = tk.Tk()
    root.title("upload_signal_options")
    root.configure(bg="#E7DECC")
    for widget in root.winfo_children():
        widget.destroy()
    tk.Button(root, text="only draw Signal",bg="#1569C7", fg="#E7DECC", font=("Helvetica", 12), command=lambda: plot_signal_from_file(root,0)).pack(pady=10)
    tk.Button(root, text="multiply",bg="#1569C7", fg="#E7DECC", font=("Helvetica", 12), command=lambda: plot_signal_from_file(root,1)).pack(pady=10)
    tk.Button(root, text="normalize",bg="#1569C7", fg="#E7DECC", font=("Helvetica", 12), command=lambda: plot_signal_from_file(root,2)).pack(pady=10)
    tk.Button(root, text="square",bg="#1569C7", fg="#E7DECC", font=("Helvetica", 12), command=lambda: plot_signal_from_file(root,3)).pack(pady=10)
    tk.Button(root, text="accumlate",bg="#1569C7", fg="#E7DECC", font=("Helvetica", 12), command=lambda: plot_signal_from_file(root,4)).pack(pady=10)
# Function to show the home page
def home_page(root):

    for widget in root.winfo_children():
        widget.destroy()

    welcome_label = tk.Label(root, text="Welcome to Visualizer", bg="#1569C7", fg="white", font=("Helvetica", 24))
    welcome_label.pack(pady=20, fill=tk.X)

    button_frame = tk.Frame(root, bg="#1569C7")
    button_frame.pack(pady=20)

    buttons = [
        ("Upload Signal File", lambda: upload_signal_options()),
        ("Generate Signal", lambda: task_one_interface()),
        ("Add and Sub 2 Signals", lambda: load_and_process_files(root)),
        ("Quantization", lambda: quantize_and_save_signal(root)),
        ("DFT", lambda: dft(root)),
        ("IDFT", lambda: idft(root)),
        ("Shift and Fold", lambda: sfrun(root)),
        ("Derivative Signal", lambda: DerivativeSignal(root)),
        ("DCT", lambda: dctrun(root)),
        ("correlation", lambda: runCorr(root)),
        ("Convolution",lambda:runConv(root))
    ]

    for i, (text, command) in enumerate(buttons):
        tk.Button(
            button_frame, text=text, bg="#E7DECC", fg="#1569C7", font=("Helvetica", 12), command=command
        ).grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="ew")

    for col in range(3):
        button_frame.grid_columnconfigure(col, weight=1)
   
   
