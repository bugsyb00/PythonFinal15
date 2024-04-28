import tkinter as tk
from tkinter.filedialog import askopenfile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.io import wavfile
import numpy as np
import os
file_path = None

def getFile():
    file = askopenfile(mode='r')
    if file:
        global file_path
        file_path = file.name
        file_name = os.path.basename(file_path)
        fileDisplay.insert(tk.END, file_name)
        checkType(file_path)
        checkStereo(file_path)
        length = checkMetaData(file_path)
        lengthSec = length / 1000

        fileDisplay.insert(tk.END, f"File length: {lengthSec} seconds")

        wavArray = makeWavArray(file_path)
        plotWaveform(length, wavArray)

        rt1, max1, test1 = plotrt60(file_path, 250, "Low Frequency")
        rt2, max2, test2 = plotrt60(file_path, 1000, "Mid Frequency")
        rt3, max3, test3 = plotrt60(file_path, 10000, "High Frequency")

        rt1 = abs(rt1)
        rt2 = abs(rt2)
        rt3 = abs(rt3)
        rtdif = (rt1 + rt2 + rt3) / 3
        rtdif -= 0.5
        fileDisplay.insert(tk.END, f"RT60 Difference: {rtdif:.3f} seconds")
        fileDisplay.insert(tk.END, f"Low Frequency RT60: {rt1:.3f} seconds")
        fileDisplay.insert(tk.END, f"Maximum Frequency: {max(max1, max2, max3):.3f} kHz")
        fileDisplay.insert(tk.END, f"High Frequency RT60: {rt3:.3f} seconds")
        fileDisplay.insert(tk.END, f"Mid Frequency RT60: {rt2:.3f} seconds")

        sample_rate, data = wavfile.read(file_path)
        frequencies, spectrum = compute_frequency_spectrum(data, sample_rate)


        file.close()
        # opens up file details page in gui
        showFileDetailsPage()