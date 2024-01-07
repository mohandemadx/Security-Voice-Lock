import librosa
import matplotlib.pyplot as plt
import numpy as np
import csv
from sklearn.metrics.pairwise import euclidean_distances
from fastdtw import fastdtw

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


def calc_similarity(spec1, spec2):

    spec1_flat = spec1.flatten()
    spec2_flat = spec2.flatten()

    # Calculate dynamic time warping distance
    _, path = fastdtw(spec1_flat, spec2_flat)

    # Calculate similarity based on the path length
    path_length = len(path)
    max_length = max(len(spec1_flat), len(spec2_flat))
    similarity=((2*max_length)-path_length)/(2*max_length)
    return similarity


