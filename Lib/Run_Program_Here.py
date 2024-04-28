import tkinter as tk
from tkinter import filedialog, messagebox
import os
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#Custom Fonts for GUI
custom_font1 = ('Helvetica', 15, 'bold')
custom_font2 = ('Helvetica', 12)
custom_font3 = ('Helvetica', 15)
custom_font4 = ('Helvetica', 12, 'bold')


# Function to calculate the difference in RT60 required to reduce to a target RT60
def calculate_rt60_difference(rt60_original, target_rt60):
    return rt60_original - target_rt60


# Function to estimate the RT60 of an audio signal
def estimate_rt60(audio_data, sample_rate):
    # Calculate the energy decay curve (EDC) from the audio signal
    squared_audio = audio_data ** 2
    edc = np.cumsum(squared_audio[::-1])[::-1]

    # Normalize the EDC
    edc_normalized = edc / np.max(edc)

    # Find the time constant T60 (time to decay to -60 dB)
    t60_idx = np.argmax(edc_normalized < 10 ** (-6))

    # Convert the index to time in seconds (assuming linear spacing of audio samples)
    t60 = t60_idx / sample_rate

    # Calculate RT60 (double the T60 value)
    rt60 = 2 * t60

    return rt60


# Function to calculate the lowest and highest frequencies in an audio signal
def calculate_frequency_range(audio_data, sample_rate):
    # Compute the Fast Fourier Transform (FFT) of the audio data
    fft_result = np.fft.fft(audio_data)

    # Compute the frequency values corresponding to the FFT result
    frequencies = np.fft.fftfreq(len(fft_result), 1 / sample_rate)

    # Find the indices corresponding to positive frequencies
    positive_freq_indices = np.where(frequencies > 0)[0]

    # Get the magnitudes of FFT result for positive frequencies
    magnitudes = np.abs(fft_result[positive_freq_indices])

    # Find the index of the lowest frequency (excluding DC component)
    min_freq_idx = positive_freq_indices[np.argmin(magnitudes)]

    # Find the index of the highest frequency
    max_freq_idx = positive_freq_indices[np.argmax(magnitudes)]

    # Get the corresponding frequencies in Hz
    min_frequency = frequencies[min_freq_idx]
    max_frequency = frequencies[max_freq_idx]

    return min_frequency, max_frequency


# Function to display the waveform plot
def display_waveform_plot(audio_data, sample_rate):
    # Create a new window for the waveform plot
    waveform_window = tk.Toplevel()
    waveform_window.title("Waveform Plot")

    # Calculate time axis for waveform (in seconds)
    time_axis = np.linspace(0, len(audio_data) / sample_rate, len(audio_data))

    # Plot the waveform
    plt.figure(figsize=(8, 4))
    plt.plot(time_axis, audio_data, color='#A232D6')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title("Audio Waveform")
    plt.grid(True)

    # Create a Tkinter canvas to display the waveform plot
    canvas = FigureCanvasTkAgg(plt.gcf(), master=waveform_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Function to plot and display low frequency RT60 values
def display_low_frequency_rt60(audio_data, sample_rate):
    # Calculate the frequency range and RT60 values
    frequencies = np.fft.fftfreq(len(audio_data), 1/sample_rate)
    positive_freq_indices = np.where(frequencies > 0)[0]
    magnitudes = np.abs(np.fft.fft(audio_data)[positive_freq_indices])

    # Find the index corresponding to the lowest frequency
    min_freq_idx = positive_freq_indices[np.argmin(magnitudes)]

    # Compute RT60 for the lowest frequency
    rt60_lowest = estimate_rt60(audio_data[min_freq_idx:], sample_rate)

    # Create a new Tkinter window for the RT60 plot
    rt60_plot_window = tk.Toplevel()
    rt60_plot_window.title("Low Frequency RT60 Plot")

    # Create a figure and plot the RT60 values
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(frequencies[positive_freq_indices], magnitudes, color='#32D67C')  # Magnitude vs. Frequency
    ax.axvline(x=frequencies[min_freq_idx], color='red', linestyle='--', label=f"Lowest Frequency (RT60: {rt60_lowest:.2f} seconds)")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_title("Low Frequency RT60 Plot")
    ax.grid(True)
    ax.legend()

    # Create a Tkinter canvas to display the plot
    canvas = FigureCanvasTkAgg(fig, master=rt60_plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Function to plot and display high frequency RT60 values
def display_high_frequency_rt60(audio_data, sample_rate):
    # Calculate the frequency range and RT60 values
    frequencies = np.fft.fftfreq(len(audio_data), 1/sample_rate)
    positive_freq_indices = np.where(frequencies > 0)[0]
    magnitudes = np.abs(np.fft.fft(audio_data)[positive_freq_indices])

    # Find the index corresponding to the highest frequency
    max_freq_idx = positive_freq_indices[np.argmax(magnitudes)]

    # Compute RT60 for the highest frequency
    rt60_highest = estimate_rt60(audio_data[max_freq_idx:], sample_rate)

    # Create a new Tkinter window for the RT60 plot
    rt60_plot_window = tk.Toplevel()
    rt60_plot_window.title("High Frequency RT60 Plot")

    # Create a figure and plot the RT60 values
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(frequencies[positive_freq_indices], magnitudes, color='#32CCD6')  # Magnitude vs. Frequency
    ax.axvline(x=frequencies[max_freq_idx], color='blue', linestyle='--', label=f"Highest Frequency (RT60: {rt60_highest:.2f} seconds)")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_title("High Frequency RT60 Plot")
    ax.grid(True)
    ax.legend()

    # Create a Tkinter canvas to display the plot
    canvas = FigureCanvasTkAgg(fig, master=rt60_plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Function to plot and display mid frequency RT60 values
def display_mid_frequency_rt60(audio_data, sample_rate):
    # Calculate the frequency range and RT60 values
    frequencies = np.fft.fftfreq(len(audio_data), 1/sample_rate)
    positive_freq_indices = np.where(frequencies > 0)[0]
    magnitudes = np.abs(np.fft.fft(audio_data)[positive_freq_indices])

    # Find the indices corresponding to mid-range frequencies
    mid_freq_indices = positive_freq_indices[(frequencies[positive_freq_indices] >= 1000) & (frequencies[positive_freq_indices] <= 5000)]

    # Compute RT60 for the mid frequencies
    rt60_mid = estimate_rt60(audio_data[mid_freq_indices], sample_rate)

    # Create a new Tkinter window for the RT60 plot
    rt60_plot_window = tk.Toplevel()
    rt60_plot_window.title("Mid Frequency RT60 Plot")

    # Create a figure and plot the RT60 values
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(frequencies[mid_freq_indices], magnitudes[mid_freq_indices], color='#E8BF69')  # Magnitude vs. Frequency
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_title("Mid Frequency RT60 Plot")
    ax.grid(True)
    ax.text(0.5, 0.9, f"Mid Frequency (1000-5000 Hz)\nRT60: {rt60_mid:.2f} seconds", transform=ax.transAxes, ha='center')

    # Create a Tkinter canvas to display the plot
    canvas = FigureCanvasTkAgg(fig, master=rt60_plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Function to plot and display combined frequency RT60 values
def display_combined_frequency_rt60(audio_data, sample_rate):
    # Calculate the frequency range and RT60 values for low, mid, and high frequencies
    frequencies = np.fft.fftfreq(len(audio_data), 1/sample_rate)
    positive_freq_indices = np.where(frequencies > 0)[0]
    magnitudes = np.abs(np.fft.fft(audio_data)[positive_freq_indices])

    # Find the indices corresponding to mid-range frequencies
    mid_freq_indices = positive_freq_indices[(frequencies[positive_freq_indices] >= 1000) & (frequencies[positive_freq_indices] <= 5000)]

    # Find the index corresponding to the lowest frequency
    min_freq_idx = positive_freq_indices[np.argmin(magnitudes)]

    # Find the index corresponding to the highest frequency
    max_freq_idx = positive_freq_indices[np.argmax(magnitudes)]

    # Compute RT60 for the lowest, mid, and highest frequencies
    rt60_lowest = estimate_rt60(audio_data[min_freq_idx:], sample_rate)
    rt60_highest = estimate_rt60(audio_data[max_freq_idx:], sample_rate)
    rt60_mid = estimate_rt60(audio_data[mid_freq_indices], sample_rate)

    # Create a new Tkinter window for the combined RT60 plot
    combined_rt60_plot_window = tk.Toplevel()
    combined_rt60_plot_window.title("Combined Frequency RT60 Plot")

    # Create a figure and plot the RT60 values
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(frequencies[positive_freq_indices], magnitudes, color='#C3F678', label="All Frequencies")  # Magnitude vs. Frequency
    ax.axvline(x=frequencies[min_freq_idx], color='red', linestyle='--', label=f"Lowest Frequency (RT60: {rt60_lowest:.2f} seconds)")
    ax.axvline(x=frequencies[mid_freq_indices[0]], color='green', linestyle='--', label=f"Mid Frequency (RT60: {rt60_mid:.2f} seconds)")
    ax.axvline(x=frequencies[max_freq_idx], color='blue', linestyle='--', label=f"Highest Frequency (RT60: {rt60_highest:.2f} seconds)")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_title("Combined Frequency RT60 Plot")
    ax.grid(True)
    ax.legend()

    # Create a Tkinter canvas to display the plot
    canvas = FigureCanvasTkAgg(fig, master=combined_rt60_plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# Function to calculate the energy decay curve (RT60) from audio data
def calculate_energy_decay_curve(audio_data, sample_rate):
    # Compute amplitude envelope of the audio signal
    envelope = np.abs(audio_data)

    # Calculate the decay curve (RT60) in seconds
    rt60 = -60.0 / (sample_rate * np.log(envelope / np.max(envelope)))

    # Time vector corresponding to each sample
    time_vector = np.arange(len(audio_data)) / sample_rate

    return time_vector, rt60

# Function to display energy decay curve plot in a new window
def display_energy_decay_curve_plot(audio_data, sample_rate):
    # Calculate energy decay curve (RT60)
    time_vector, rt60 = calculate_energy_decay_curve(audio_data, sample_rate)

    # Create a new Tkinter window for the energy decay curve plot
    rt60_plot_window = tk.Toplevel()
    rt60_plot_window.title("Energy Decay Curve (RT60) Plot")

    # Plot the energy decay curve (RT60)
    plt.figure(figsize=(10, 6))
    plt.plot(time_vector, rt60)
    plt.xlabel('Time (seconds)')
    plt.ylabel('RT60 (seconds)')
    plt.title('Energy Decay Curve (RT60)')
    plt.grid(True)
    plt.tight_layout()

    # Create a Tkinter canvas to display the plot
    canvas = FigureCanvasTkAgg(plt.gcf(), master=rt60_plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Function to process audio file and display results
def process_audio_file():
    # Ask user to select an audio file
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])

    if not file_path:
        messagebox.showerror("Error", "No file selected.")
        return

    # Display file name
    filename_label.config(text=f"Selected File: {os.path.basename(file_path)}")

    # Load audio using pydub
    audio = AudioSegment.from_wav(file_path)
    sample_rate = audio.frame_rate
    audio_data = np.array(audio.get_array_of_samples())

    try:
        # Calculate the total length of the audio file in seconds
        audio_length_seconds = len(audio_data) / sample_rate

        # Estimate the RT60 of the audio for lowest and highest frequencies
        rt60_lowest = estimate_rt60(audio_data, sample_rate)
        rt60_highest = estimate_rt60(audio_data[::-1], sample_rate)  # Reverse audio for highest frequency

        # Calculate the lowest and highest frequencies in the audio
        min_frequency, max_frequency = calculate_frequency_range(audio_data, sample_rate)

        # Calculate the RT60 difference needed to reduce to 0.5 seconds
        target_rt60 = 0.5
        rt60_difference = calculate_rt60_difference(rt60_lowest, target_rt60)

        results_text = (
        f"File Name: {os.path.basename(file_path)}\n"
        f"File Length: {audio_length_seconds:.2f} seconds\n"
        f"RT60 Difference (Lowest Frequency): {rt60_difference:.2f} seconds\n"
        f"Lowest Frequency: {min_frequency:.2f} Hz (RT60: {rt60_lowest:.2f} seconds)\n"
        f"Highest Frequency: {max_frequency:.2f} Hz (RT60: {rt60_highest:.2f} seconds)"
        )

        # Display the results with left-aligned text
        resonance_label.config(text=results_text, anchor='w', justify='left')

        # Update waveform_button command to pass audio_data and sample_rate to display_waveform_plot
        waveform_button.config(command=lambda: display_waveform_plot(audio_data, sample_rate))

        # Add button to display low frequency RT60 plot
        low_freq_rt60_button.config(command=lambda: display_low_frequency_rt60(audio_data, sample_rate))

        # Add button to display high frequency RT60 plot
        high_freq_rt60_button.config(command=lambda: display_high_frequency_rt60(audio_data, sample_rate))

        # Add button to display mid frequency RT60 plot
        mid_freq_rt60_button.config(command=lambda: display_mid_frequency_rt60(audio_data, sample_rate))

        # Add button to display combined frequency RT60 plot
        combined_freq_rt60_button.config(command=lambda: display_combined_frequency_rt60(audio_data, sample_rate))

        # Add button to display energy decay curve
        energy_decay_button.config(command=lambda: display_energy_decay_curve_plot(audio_data, sample_rate))


    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# GUI Setup
root = tk.Tk()
root.title("CSProb&Sol Final")
root.geometry('700x700')
# Create GUI components
label = tk.Label(root, text="CS Problem Solving and Solutions Final", font=custom_font1)
label.pack(pady=20)

label2 = tk.Label(root, text="Section 1: Group 2", font=custom_font2)
label2.pack(pady=5)


label4 = tk.Label(root, text="Please select a file of the .WAV format", font=custom_font2)
label4.pack(pady=30)

select_button = tk.Button(root, text="Select Audio File", font=custom_font2, bg='#F85EF6',command=process_audio_file)
select_button.pack(pady=20)

filename_label = tk.Label(root, text="Selected File: None", font=custom_font2)
filename_label.pack()

resonance_label = tk.Label(root, text="Audio Processing Results:", font= custom_font2)
resonance_label.pack(pady=10)

waveform_button = tk.Button(root, text="Waveform Plot", bg='#EEA2F7',command=lambda: None)
waveform_button.pack(pady=10)  # Initially set command to a placeholder lambda function

# Frame to hold the frequency buttons
freq_buttons_frame = tk.Frame(root)
freq_buttons_frame.pack(pady=10)

# Button to display low frequency RT60 plot
low_freq_rt60_button = tk.Button(freq_buttons_frame, text="Low Freq RT60 Plot", bg='#EEA2F7', command=lambda: None)
low_freq_rt60_button.pack(side=tk.LEFT, padx=10)

# Button to display mid frequency RT60 plot
mid_freq_rt60_button = tk.Button(freq_buttons_frame, text="Mid Freq RT60 Plot", bg='#EEA2F7', command=lambda: None)
mid_freq_rt60_button.pack(side=tk.LEFT, padx=10)

# Button to display high frequency RT60 plot
high_freq_rt60_button = tk.Button(freq_buttons_frame, text="High Freq RT60 Plot", bg='#EEA2F7', command=lambda: None)
high_freq_rt60_button.pack(side=tk.LEFT, padx=10)


# Button to display combined frequency RT60 plot
combined_freq_rt60_button = tk.Button(root, text="Combined Frequency RT60 Plot", bg='#EEA2F7', command=lambda: None)
combined_freq_rt60_button.pack(pady=10)  # Initially set command to a placeholder lambda function

# Button to display an energy decay curve
energy_decay_button = tk.Button(root, text="Energy Decay Curve", bg='#EEA2F7', command=lambda: None)
energy_decay_button.pack(pady=10)

# Run the GUI main loop
root.mainloop()
