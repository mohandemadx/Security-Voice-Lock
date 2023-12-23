import matplotlib.pyplot as plt

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