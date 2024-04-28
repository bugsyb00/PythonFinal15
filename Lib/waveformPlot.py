import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
import MainStructure
import wavtools

def displayWaveform(file_path):
    audio = AudioSegment.from_file(file_path)

    # Extract raw audio data (numpy array)
    samples = np.array(audio.get_array_of_samples())

    # Normalize samples (between -1 and 1)
    normalized_samples = samples / np.max(np.abs(samples))

    # Plot waveform
    plt.figure(figsize=(10, 4))
    plt.plot(normalized_samples, color='b')
    plt.title('Waveform')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()
