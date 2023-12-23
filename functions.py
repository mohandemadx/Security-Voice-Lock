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
        
def calculate_fingerprint(audio_data):
        # Fingerprint calculation using mean and standard deviation
        mean = np.mean(audio_data)
        std_dev = np.std(audio_data)
        fingerprint = [mean, std_dev]
        print(fingerprint)
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
