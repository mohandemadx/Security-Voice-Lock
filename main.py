import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
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
        self.ui.radioButton_2.clicked.connect(self.change_mode)
        self.ui.radioButton.clicked.connect(self.change_mode)
        self.recordButton.setIcon(QIcon('icons\mic-svgrepo-com.png'))
        # Create instances of MplWidget for spectrogram
        self.canvas = FigureCanvas(plt.Figure())

        # Set up layouts for spectrogram widgets
        f.addwidget(self.canvas, self.ui.spectoFrame)

        # Create instances of AudioRecorder for recording audio
        self.recorder = AudioRecorder(file_name='recorded_audio.wav')


    def record_audio(self):
        self.recorder.record_audio(label=self.ui.recordingLabel)
        self.recorder.data = self.recorder.get_audio_data()
        self.process_audio()


    def process_audio(self):
        f.show_spectrogram(audio_data=self.recorder.data ,sample_rate=self.recorder.sample_rate, canvas=self.canvas)
        
    def person_access(self):
        pass

    def change_mode(self):
        # Voice Fingerprint Mode
        if self.ui.radioButton_2.isChecked()== True:
            self.comboBox.setEnabled(True)
        
        # Voice Code Mode
        else:
            self.comboBox.setEnabled(False)
            
        
    

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = SecurityVoiceCodeAccessApp()
    mainWin.show()
    sys.exit(app.exec())
