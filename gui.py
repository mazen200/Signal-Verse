import tkinter as tk
from signal_generation import generate_signal, plot_signal_from_file

# Function to create signal generation interface
def task_one_interface(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="white")  # Set the background color to white

    left_frame = tk.Frame(root, bg="white")  # Change frame background to white
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Back to Home button at the top left
    back_button = tk.Button(left_frame, text="Back to Home", bg="#1569C7", fg="white", font=("Helvetica", 12), command=lambda: home_page(root))
    back_button.pack(anchor="nw", pady=10, padx=10)

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

    tk.Button(left_frame, text="Upload Signal File", bg="#1569C7", fg="white", font=("Helvetica", 12), command=lambda: plot_signal_from_file(root)).pack(pady=20)


# Function to show the home page
def home_page(root):
    for widget in root.winfo_children():
        widget.destroy()

    welcome_label = tk.Label(root, text="Welcome to Visualizer", bg="#1569C7", fg="white", font=("Helvetica", 24))
    welcome_label.pack(pady=50, fill=tk.X)

    task_one_button = tk.Button(root, text="Task One", bg="white", fg="#1569C7", font=("Helvetica", 14), command=lambda: task_one_interface(root))
    task_one_button.pack(pady=20)
