import numpy as np
import matplotlib.pyplot as plt
import math

# FIR Filter Implementation
def calculate_fir_coefficients(filter_type, fc1, fc2=None, sampling_frequency=1, window_type="hamming", transition_band=0.1):
    """
    Calculate FIR filter coefficients using the window method.

    Args:
        filter_type (str): Type of the filter (lowpass, highpass, bandpass, bandstop).
        fc1 (float): Cutoff frequency or the first frequency for band filters (normalized).
        fc2 (float): Second frequency for band filters (normalized).
        sampling_frequency (float): Sampling frequency of the input signal.
        window_type (str): Type of the window (hamming, hanning, rectangular, blackman).
        transition_band (float): Transition bandwidth (normalized).

    Returns:
        np.array: FIR filter coefficients.
    """
    # Adjust frequencies for transition band
    if filter_type in ["lowpass", "highpass"]:
        fc1 = fc1 / sampling_frequency
    elif filter_type in ["bandpass", "bandstop"]:
        fc1 = fc1 / sampling_frequency
        fc2 = fc2 / sampling_frequency

    delta_f = transition_band / sampling_frequency

    # Calculate filter order N
    N = int(math.ceil((4 / delta_f)))  # Approximation for Blackman window length
    if N % 2 == 0:
        N += 1  # Make sure N is odd

    # Generate ideal impulse response (h_d(n))
    h_d = []
    M = (N - 1) / 2  # Midpoint of the filter

    for n in range(N):
        if n == M:  # Center coefficient
            if filter_type == "lowpass":
                h_d.append(2 * fc1)
            elif filter_type == "highpass":
                h_d.append(1 - 2 * fc1)
            elif filter_type == "bandpass":
                h_d.append(2 * (fc2 - fc1))
            elif filter_type == "bandstop":
                h_d.append(1 - 2 * (fc2 - fc1))
        else:
            n_minus_M = n - M
            if filter_type == "lowpass":
                h_d.append(math.sin(2 * math.pi * fc1 * n_minus_M) / (math.pi * n_minus_M))
            elif filter_type == "highpass":
                h_d.append(-math.sin(2 * math.pi * fc1 * n_minus_M) / (math.pi * n_minus_M))
            elif filter_type == "bandpass":
                h_d.append((math.sin(2 * math.pi * fc2 * n_minus_M) - math.sin(2 * math.pi * fc1 * n_minus_M)) / (math.pi * n_minus_M))
            elif filter_type == "bandstop":
                h_d.append((math.sin(2 * math.pi * fc1 * n_minus_M) - math.sin(2 * math.pi * fc2 * n_minus_M)) / (math.pi * n_minus_M))

    # Apply windowing function
    if window_type == "hamming":
        window = [0.54 - 0.46 * math.cos((2 * math.pi * n) / (N - 1)) for n in range(N)]
    elif window_type == "hanning":
        window = [0.5 - 0.5 * math.cos((2 * math.pi * n) / (N - 1)) for n in range(N)]
    elif window_type == "blackman":
        window = [
            0.42
            - 0.5 * math.cos((2 * math.pi * n) / (N - 1))
            + 0.08 * math.cos((4 * math.pi * n) / (N - 1))
            for n in range(N)
        ]
    else:  # Rectangular window
        window = [1 for _ in range(N)]

    h = np.array([h_d[i] * window[i] for i in range(N)])
    return h

# Resampling Function
def resample_signal(signal, sampling_frequency, M, L, transition_band):
    """
    Resample the signal by applying up-sampling or down-sampling.

    Args:
        signal (np.array): Input signal.
        sampling_frequency (float): Original sampling frequency.
        M (int): Down-sampling factor.
        L (int): Up-sampling factor.
        transition_band (float): Transition bandwidth.

    Returns:
        np.array: Resampled signal.
    """
    if M == 0 and L == 0:
        raise ValueError("Both M and L cannot be zero.")

    # Low-pass filter for anti-aliasing or interpolation
    filter_coefficients = calculate_fir_coefficients(
        "lowpass", fc1=(0.5 / (max(M, L))), sampling_frequency=sampling_frequency, transition_band=transition_band
    )

    if M > 0 and L > 0:  # Fractional resampling
        # Up-sample by L
        upsampled_signal = np.zeros(len(signal) * L)
        upsampled_signal[::L] = signal
        filtered_signal = np.convolve(upsampled_signal, filter_coefficients, mode="same")

        # Down-sample by M
        resampled_signal = filtered_signal[::M]
    elif M > 0:  # Down-sample only
        filtered_signal = np.convolve(signal, filter_coefficients, mode="same")
        resampled_signal = filtered_signal[::M]
    else:  # Up-sample only
        upsampled_signal = np.zeros(len(signal) * L)
        upsampled_signal[::L] = signal
        resampled_signal = np.convolve(upsampled_signal, filter_coefficients, mode="same")

    return resampled_signal

# Test and visualization
if __name__ == "__main__":
    # Example input signal
    t = np.linspace(0, 1, 500, endpoint=False)
    input_signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 15 * t)

    # FIR filter example
    fir_coeffs = calculate_fir_coefficients(
        filter_type="lowpass", fc1=0.2, sampling_frequency=1, window_type="hamming", transition_band=0.1
    )
    filtered_signal = np.convolve(input_signal, fir_coeffs, mode="same")

    # Resampling example
    resampled_signal = resample_signal(input_signal, sampling_frequency=1, M=2, L=0, transition_band=0.1)

    # Plot results
    plt.figure(figsize=(12, 6))

    plt.subplot(3, 1, 1)
    plt.title("Original Signal")
    plt.plot(t, input_signal)

    plt.subplot(3, 1, 2)
    plt.title("Filtered Signal")
    plt.plot(t, filtered_signal)

    plt.subplot(3, 1, 3)
    plt.title("Resampled Signal")
    plt.plot(resampled_signal)

    plt.tight_layout()
    plt.show()
