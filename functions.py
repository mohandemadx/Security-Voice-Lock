import librosa
import matplotlib.pyplot as plt
import numpy as np
import csv

def clear(frame):
    layout = frame.layout()
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
                
def addwidget(widget, frame):
    clear(frame)
    layout = frame.layout()
    layout.addWidget(widget)
    
    frame.setLayout(layout)
    
def show_spectrogram(audio_data, sample_rate, canvas):
    plt.close()
    plt.figure()
    plt.specgram(audio_data, Fs=sample_rate, cmap='viridis', aspect='auto')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Spectrogram')
    canvas.figure.clear()
    canvas.figure = plt.gcf()
    canvas.draw()
        
def calculate_fingerprint(data, sr):
    stft = librosa.stft(data)

    # Calculate chroma features
    chroma = librosa.feature.chroma_stft(S=stft)

    # Calculate Mel-Frequency Cepstral Coefficients (MFCCs)
    mfcc = librosa.feature.mfcc(data, sr=sr)

    # Calculate zero-crossing rate
    zero_crossings = librosa.feature.zero_crossing_rate(data)

    # Calculate energy envelope
    energy = np.sum(np.abs(stft), axis=0)

    # Calculate statistical descriptors
    mean_chroma = np.mean(chroma, axis=1)
    std_mfcc = np.std(mfcc, axis=1)

    # Combine all features into a single fingerprint
    fingerprint = np.concatenate([mean_chroma, std_mfcc, zero_crossings, energy])

    return fingerprint
    
def append_row_to_csv(file_path, new_row):
    try:
        # Open the CSV file in append mode
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)

            # Write the new row to the CSV file
            writer.writerow(new_row)

        print("Row appended to CSV successfully.")
    except Exception as e:
        print(f"Error: {e}")
