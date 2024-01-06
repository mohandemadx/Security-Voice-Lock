import librosa
import numpy as np
import matplotlib.pyplot as plt

def extract_voice_fingerprint(file_path, num_mfcc=13):
    # Load audio file
    audio, sr = librosa.load(file_path)

    # Extract MFCCs
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=num_mfcc)
    print(mfccs.shape)

    return mfccs

def plot_voice_fingerprint(mfccs):
    # Display the voice fingerprint as an image
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mfccs, x_axis='time')
    plt.colorbar()
    plt.title('MFCCs (Mel-Frequency Cepstral Coefficients)')
    plt.xlabel('Time')
    plt.ylabel('MFCC Coefficients')
    plt.show()

# Example usage
file_path = 'recorded_audio.wav'
voice_fingerprint = extract_voice_fingerprint(file_path)
plot_voice_fingerprint(voice_fingerprint)
