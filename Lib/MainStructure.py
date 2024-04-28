import tkinter as tk
from tkinter.filedialog import askopenfile
from tkinter import filedialog
from pydub import AudioSegment
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.io import wavfile
import numpy as np
from mutagen import File
import os
import wavtools
import frequencyPlot
from wavtools import checkStereo, checkMetaData
#Custom Fonts for GUI
custom_font1 = ('Helvetica', 15, 'bold')
custom_font2 = ('Helvetica', 12)
custom_font3 = ('Helvetica', 15)
custom_font4 = ('Helvetica', 12, 'bold')

def getFile():
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        print("Selected file:", file_path)

        # Check if the selected file is in WAV format
        if file_path.lower().endswith('.wav'):
            print("File is already in WAV format.")

        else:
            # Convert the file to WAV format
            try:
                audio = AudioSegment.from_file(file_path)
                wav_file_path = os.path.splitext(file_path)[0] + '.wav'
                audio.export(wav_file_path, format='wav')
                print(f"File converted to WAV: {wav_file_path}")

            except Exception as e:
                print(f"Error converting file to WAV: {e}")
        metadata = checkMetaData(file_path)
        if metadata:
            channels, sample_width, frame_rate, frame_width, duration_ms = metadata
            print(f"Channels: {channels}")
            print(f"Sample Width: {sample_width} bytes")
            print(f"Frame Rate: {frame_rate} Hz")
            print(f"Frame Width: {frame_width} bytes")
            print(f"Duration: {duration_ms} milliseconds")

            # Remove metadata if present (specifically for WAV files)
            if file_path.lower().endswith('.wav'):
                audio = AudioSegment.from_file(file_path)
                audio = audio.set_frame_rate(frame_rate).set_channels(channels)
                audio.export("output.wav", format="wav", tags={})  # Export without metadata
                print("Metadata removed from the WAV file.")

            # Calculate duration in seconds
            duration_sec = duration_ms / 1000
            print(f"Duration: {duration_sec} seconds")
        else:
            print("Failed to retrieve metadata.")

def display_file_details(metadata):
    # Create a new tkinter window for file details
    details_window = tk.Toplevel()
    details_window.title("File Details")
    details_window.geometry('800x600')

    # Display metadata
    metadata_label = tk.Label(details_window, text="File Details", font=('Helvetica', 16))
    metadata_label.pack(pady=20)

    for key, value in metadata.items():
        detail_label = tk.Label(details_window, text=f"{key}: {value}")
        detail_label.pack()

def display_file_details_page():
    # Create a new tkinter window for file details
    details_window = tk.Toplevel()
    details_window.title("File Details")
    details_window.geometry('800x600')

    # Placeholder text for file details (replace with actual details)
    details_label = tk.Label(details_window, text="File Details:", font=('Helvetica', 16))
    details_label.pack(pady=20)


if __name__ == "__main__":
    main()

# Create the main window
root = tk.Tk()
root.geometry('700x400')
root.title("CS Prob Solving & Solutions Final")

label = tk.Label(root, text="CS Problem Solving and Solutions Final", font=custom_font1)
label.pack(pady=20)

label2 = tk.Label(root, text="Section 1", font=custom_font2)
label2.pack(pady=5)

label3 = tk.Label(root, text="Group 2", font=custom_font2)
label3.pack(pady=5)

label4 = tk.Label(root, text="Please select a file of the .WAV format", font=custom_font2)
label4.pack(pady=30)

button_select_file = tk.Button(root, text='Select File', command=getFile)
button_select_file.pack(pady=20)

button_open_details = tk.Button(root, text='View File Details', command=display_file_details_page)
button_open_details.pack(pady=20)
# Run the main event loop
root.mainloop()
