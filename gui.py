import tkinter as tk
from tkinter import ttk
from signal_generation import generate_signal, plot_signal_from_file
from adder_subtracter import load_and_process_files
from quantization import quantize_and_save_signal
from fourier import dft, idft
from shiftAndFold import sfrun
from DerivativeSignal import DerivativeSignal
from dct import dctrun
from task6 import runCorr, runConv, runMovAvg, runDC
from firresample import run_filter,run_sampling

class SignalVisualizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Signal Verse")
        self.geometry("1000x600")
        self.configure(bg="#F7F9FC")  # Soft Gray Background

        self.style = ttk.Style(self)
        self._set_theme()

        self._create_layout()

    def _set_theme(self):
        """Set the ttk theme and style."""
        self.style.theme_use("clam")

        # Frame Styling
        self.style.configure("TFrame", background="#F7F9FC")
        self.style.configure("Sidebar.TFrame", background="#2C3E50")

        # Button Styling
        self.style.configure(
            "TButton",
            background="#3498DB",
            foreground="white",
            font=("Helvetica", 12),
            borderwidth=0,
            padding=6,
        )
        self.style.map(
            "TButton",
            background=[("active", "#5DADE2"), ("pressed", "#3498DB")],
        )

        # Label Styling
        self.style.configure(
            "TLabel",
            background="#F7F9FC",
            foreground="#2C3E50",
            font=("Helvetica", 12),
        )
        self.style.configure(
            "Title.TLabel",
            font=("Helvetica", 16, "bold"),
            background="#F7F9FC",
            foreground="#2C3E50",
        )
        self.style.configure(
            "Sidebar.TLabel",
            font=("Helvetica", 14, "bold"),
            background="#2C3E50",
            foreground="white",
        )

    def _create_layout(self):
        # Sidebar for navigation
        self.sidebar = ttk.Frame(self, style="Sidebar.TFrame", width=200)
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        self.main_frame = ttk.Frame(self, style="TFrame")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Sidebar Header
        ttk.Label(
            self.sidebar, text="Signal Verse", style="Sidebar.TLabel"
        ).pack(pady=10)

        # Sidebar Buttons
        self._add_sidebar_button("Home", self.show_home_page)
        self._add_sidebar_button("Generate Signal", self.show_generate_signal)
        self._add_sidebar_button("Upload File Options", self.show_upload_options)
        self._add_sidebar_button("Add/Sub Signals", lambda: load_and_process_files(self))
        self._add_sidebar_button("Quantization", lambda: quantize_and_save_signal(self))
        self._add_sidebar_button("FIR Filter", self.show_filter_designer)
        self._add_sidebar_button("ReSampling", self.show_sampling)
        self._add_sidebar_button("DFT", lambda: dft(self))
        self._add_sidebar_button("IDFT", lambda: idft(self))
        self._add_sidebar_button("Shift and Fold", lambda: sfrun(self))
        self._add_sidebar_button("Derivative Signal", lambda: DerivativeSignal(self))
        self._add_sidebar_button("DCT", lambda: dctrun(self))
        self._add_sidebar_button("Correlation", lambda: runCorr(self))
        self._add_sidebar_button("Convolution", lambda: runConv(self))
        self._add_sidebar_button("Moving Avg", lambda: runMovAvg(self))
        self._add_sidebar_button("Remove DC", lambda: runDC(self))

        # Initialize with the home page
        self.show_home_page()

    def _add_sidebar_button(self, text, command):
        """Helper to add buttons to the sidebar."""
        button = ttk.Button(self.sidebar, text=text, style="TButton", command=command)
        button.pack(fill="x", pady=5, padx=10)

    def show_home_page(self):
        """Display the home page."""
        self._clear_main_frame()
        ttk.Label(self.main_frame, text="Welcome to the Signal Verse", style="Title.TLabel").pack(pady=20)
        ttk.Label(
            self.main_frame,
            text="Navigate through the sidebar to access various features.",
            style="TLabel",
        ).pack(pady=10)

    def show_generate_signal(self):
        """Generate Signal Interface."""
        self._clear_main_frame()
        ttk.Label(self.main_frame, text="Generate Signal", style="Title.TLabel").pack(pady=10)

        fields = {
            "Amplitude (A)": tk.StringVar(),
            "Phase Shift (θ in radians)": tk.StringVar(),
            "Analog Frequency (Hz)": tk.StringVar(),
            "Sampling Frequency (Hz)": tk.StringVar(),
        }

        for label, var in fields.items():
            frame = ttk.Frame(self.main_frame)
            frame.pack(fill="x", pady=5)
            ttk.Label(frame, text=label, width=25, anchor="w", style="TLabel").pack(side="left", padx=5)
            ttk.Entry(frame, textvariable=var).pack(side="left", fill="x", expand=True, padx=5)

        signal_type = tk.IntVar(value=0)
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill="x", pady=5)
        ttk.Label(frame, text="Signal Type:", width=25, anchor="w", style="TLabel").pack(side="left", padx=5)
        ttk.Radiobutton(frame, text="Sine", variable=signal_type, value=0).pack(side="left")
        ttk.Radiobutton(frame, text="Cosine", variable=signal_type, value=1).pack(side="left")

        ttk.Button(
            self.main_frame,
            text="Generate",
            command=lambda: generate_signal(
                fields["Amplitude (A)"].get(),
                fields["Phase Shift (θ in radians)"].get(),
                fields["Analog Frequency (Hz)"].get(),
                fields["Sampling Frequency (Hz)"].get(),
                signal_type,
                None,
                self,
            ),
        ).pack(pady=20)

    def show_upload_options(self):
        """File Upload Options Interface."""
        self._clear_main_frame()
        ttk.Label(self.main_frame, text="Upload Signal Options", style="Title.TLabel").pack(pady=10)

        options = [
            ("Draw Signal", 0),
            ("Multiply", 1),
            ("Normalize", 2),
            ("Square", 3),
            ("Accumulate", 4),
        ]

        for label, option in options:
            ttk.Button(
                self.main_frame,
                text=label,
                command=lambda opt=option: plot_signal_from_file(self, opt),
            ).pack(fill="x", pady=5, padx=20)
    def show_sampling(self):
        self._clear_main_frame()
        ttk.Label(self.main_frame, text="Resampling", style="Title.TLabel").pack(pady=10)
        fields = {      
        "UpSampling Factor": tk.StringVar(),
        "DownSampling Factor": tk.StringVar()
        }
        for label, var in fields.items():
            frame = ttk.Frame(self.main_frame)
            frame.pack(fill="x", pady=5)
            ttk.Label(frame, text=label, width=40, anchor="w", style="TLabel").pack(side="left", padx=5)
            ttk.Entry(frame, textvariable=var).pack(side="left", fill="x", expand=True, padx=5)
        
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        ttk.Button(
             button_frame,
             text="upload signal to Resample it",
            command=lambda: run_sampling(self,
            fields["UpSampling Factor"].get(),
            fields["DownSampling Factor"].get(),
            ),
            ).pack(side="left",padx=10)

    def show_filter_designer(self):
        """Filter Designer Interface."""
        self._clear_main_frame()
        ttk.Label(self.main_frame, text="FIR Filter Designer", style="Title.TLabel").pack(pady=10)

        fields = {      
        "Filter Type (lowpass/highpass/bandpass/bandstop)": tk.StringVar(),
        "Sampling Frequency (Hz)": tk.StringVar(),
        "Cutoff Frequency (Hz)": tk.StringVar(),
        "Cutoff Frequency 1 (Hz) [For Band Filters]": tk.StringVar(),
        "Cutoff Frequency 2 (Hz) [For Band Filters]": tk.StringVar(),
        "Transition Bandwidth (Hz)": tk.StringVar(),
        "Stopband Attenuation (dB)": tk.StringVar(),
        }

        for label, var in fields.items():
            frame = ttk.Frame(self.main_frame)
            frame.pack(fill="x", pady=5)

            if label == "Filter Type (lowpass/highpass/bandpass/bandstop)":
            # استخدم Combobox بدلاً من Entry لاختيار نوع الفلتر
                ttk.Label(frame, text=label, width=40, anchor="w", style="TLabel").pack(side="left", padx=5)
                filter_options = ["Low pass", "High pass", "Band pass", "Band stop"]
                filter_combobox = ttk.Combobox(frame, textvariable=var, values=filter_options, state="readonly")
                filter_combobox.pack(side="left", fill="x", expand=True, padx=5)
            else:
                ttk.Label(frame, text=label, width=40, anchor="w", style="TLabel").pack(side="left", padx=5)
                ttk.Entry(frame, textvariable=var).pack(side="left", fill="x", expand=True, padx=5)


# Button Frame for Generate Filter and Upload Signal
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        ttk.Button(
             button_frame,
             text="Generate Filter",
            command=lambda: run_filter(self,0,
            fields["Sampling Frequency (Hz)"].get(),
            fields["Filter Type (lowpass/highpass/bandpass/bandstop)"].get(),
            fields["Cutoff Frequency (Hz)"].get(),
            fields["Cutoff Frequency 1 (Hz) [For Band Filters]"].get(),
            fields["Cutoff Frequency 2 (Hz) [For Band Filters]"].get(),
            fields["Transition Bandwidth (Hz)"].get(),
            fields["Stopband Attenuation (dB)"].get(),
            ),
            ).pack(side="left",padx=10)

        ttk.Button(
        button_frame,
        text="apply filter on Signal",
        command=lambda: run_filter(self,1,
            fields["Sampling Frequency (Hz)"].get(),
            fields["Filter Type (lowpass/highpass/bandpass/bandstop)"].get(),
            fields["Cutoff Frequency (Hz)"].get(),
            fields["Cutoff Frequency 1 (Hz) [For Band Filters]"].get(),
            fields["Cutoff Frequency 2 (Hz) [For Band Filters]"].get(),
            fields["Transition Bandwidth (Hz)"].get(),
            fields["Stopband Attenuation (dB)"].get(),
            ),
            ).pack(side="left",padx=30)
    def _clear_main_frame(self):
        """Clear all widgets from the main frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = SignalVisualizerApp()
    app.mainloop()
