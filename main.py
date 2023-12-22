import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
import speech_recognition as sr

# CLASSES
from Audio import AudioRecorder
import functions as f

class SecurityVoiceCodeAccessApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        self.ui = uic.loadUi('design.ui', self)
        self.setWindowTitle("Security Voice-code Access")
        self.setWindowIcon(QIcon("icons/fingerprint.png"))
        
        self.access_keys = ["open middle door", "unlock the gate", "grant me access"]
        self.access_keys_flag = False
        
        self.fingerprints = []
        self.ui.recordButton.clicked.connect(self.record_audio) 
        self.load_ui_elements()
        

    def load_ui_elements(self):
        self.ui.resultLabel.setText("ACCESS DENIED")

        # Create instances of MplWidget for spectrogram
        self.canvas = FigureCanvas(plt.Figure())

        # Set up layouts for spectrogram widgets
        f.addwidget(self.canvas, self.ui.spectoFrame)

        # Create instances of AudioRecorder for recording audio
        self.recorder = AudioRecorder(file_name='recorded_audio.wav')


    def record_audio(self):
        self.recorder.record_audio()
        self.recorder.data = self.recorder.get_audio_data()
        self.process_audio()


    def process_audio(self):
        self.show_spectrogram(self.recorder.data ,self.recorder.sample_rate)
        
            
    def person_access(self):
        pass

    def show_spectrogram(self,audio_data, sample_rate):
        plt.close()
        plt.figure()
        plt.specgram(audio_data, Fs=sample_rate, cmap='viridis', aspect='auto')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Spectrogram')
        self.canvas.figure.clear()
        self.canvas.figure = plt.gcf()
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = SecurityVoiceCodeAccessApp()
    mainWin.show()
    sys.exit(app.exec())
