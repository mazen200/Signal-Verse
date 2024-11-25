from tkinter import filedialog, simpledialog, Toplevel
import numpy as np
import matplotlib.pyplot as plt
from signal_generation import parse_input_file
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from signal_generation import parse_input_file
from comparesignals import SignalSamplesAreEqual
import matplotlib.pyplot as plt
from tkinter import Toplevel, messagebox, filedialog , simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import interp1d
from scipy.interpolate import make_interp_spline
import math

def plot(root,amplitudes,title):
    cont_window = Toplevel(root)
    cont_window.title(title)
    fig_cont, ax_cont = plt.subplots()
    indices_or_freqs = [i+1 for i in range(len(amplitudes))]
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

def compute_dct(signal):
   
    result = 0
    final = 0
    k_list = [] 

    for k in range(len(signal)):
        for n in range(len(signal)):
            sum1 = (180 / (4 * len(signal))) * (2 * n - 1) * (2 * k - 1)
            c = math.cos(math.radians(sum1))
            result += signal[n] * c
            final = math.sqrt(2 / len(signal)) * result

        k_list.append(float(final))
        result = 0
    
    
    return k_list
def dctrun(root):
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    # Parse the signal from file
    signal_type, is_periodic, indices_or_freqs, amplitudes, phase_shifts = parse_input_file(file_path)
    ans = compute_dct(amplitudes)
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    SignalSamplesAreEqual(file_path,[0 for i in range(len(amplitudes))],ans)
    plot(root,amplitudes,"DCT")
    #print(ans)
#run()