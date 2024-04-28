import os.path
from pydub import AudioSegment
from scipy.io import wavfile
import numpy as np




#metadata related to the sound file
def checkMetaData(file_path):
    try:
        audio = AudioSegment.from_file(file_path)

        print("Audio Info:")
        print(f"Channels: {audio.channels}")
        print(f"Sample Width: {audio.sample_width} bytes")
        print(f"Frame Rate: {audio.frame_rate} Hz")
        print(f"Frame Width: {audio.frame_width} bytes")
        print(f"Length: {len(audio)} milliseconds")

        return audio.channels, audio.sample_width, audio.frame_rate, audio.frame_width, len(audio)
    except Exception as e:
        print(f"Error checking metadata: {e}")
        return None


#converts to monophonic
def checkStereo(file):
    raw_audio = AudioSegment.from_file(file, format="wav")
    mono_audio = raw_audio.set_channels(1)
    mono_audio.export(file, format="wav")


#array for waveform plot
def makeWavArray(file_path):
    data = wavfile.read(file_path)
    data = np.array(data[1], dtype=np.float32)
    normalized_data = data / np.max(np.abs(data), axis=0)
    return normalized_data

def compute_frequency_spectrum(data, sample_rate):
    # Compute the FFT
    fft_result = np.fft.fft(data)
    magnitude_spectrum = np.abs(fft_result)
    global frequencies
    frequencies = np.fft.fftfreq(len(data), 1 / sample_rate)

    return frequencies[:len(frequencies) // 2], magnitude_spectrum[:len(magnitude_spectrum) // 2]

