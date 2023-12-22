import sys
import sounddevice as sd
import numpy as np
import librosa.display
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QThread, QTimer, pyqtSignal, pyqtSlot, QMutex
from scipy.io.wavfile import write

class AudioRecorderThread(QThread):
    recording_finished = pyqtSignal()

    def __init__(self, filename, duration, fs):
        super().__init__()
        self.filename = filename
        self.duration = duration
        self.fs = fs
        self.mutex = QMutex()

    def run(self):
        recording = sd.rec(int(self.duration * self.fs), samplerate=self.fs, channels=1, dtype=np.int16)
        sd.wait()
        write(self.filename, self.fs, recording)
        self.recording_finished.emit()

class AudioRecorderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.record_button = QPushButton('Record Audio', self)
        self.record_button.clicked.connect(self.start_recording)

        self.canvas = FigureCanvas(plt.Figure())
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.record_button)
        vertical_layout.addWidget(self.canvas)

        central_widget = QWidget()
        central_widget.setLayout(vertical_layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Audio Recorder and Spectrogram Plotter')

    def start_recording(self):
        self.filename = 'recorded_audio.wav'
        self.duration = 4  # seconds
        self.fs = 44100  # sample rate

        # Create a separate thread for recording
        self.recording_thread = AudioRecorderThread(self.filename, self.duration, self.fs)
        self.recording_thread.recording_finished.connect(self.plot_spectrogram)
        self.recording_thread.start()

    @pyqtSlot()
    def plot_spectrogram(self):
        audio_data, sample_rate = librosa.load(self.filename, sr=None)
        self.canvas.figure.clf()
        spectrogram = librosa.amplitude_to_db(np.abs(librosa.stft(audio_data)), ref=np.max)
        librosa.display.specshow(spectrogram, sr=sample_rate, x_axis='time', y_axis='log')
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AudioRecorderApp()
    window.show()
    sys.exit(app.exec_())
