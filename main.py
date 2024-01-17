import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from pyAudioAnalysis import audioTrainTest as aT
import os
import pandas as pd
import joblib
import numpy as np

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
        
        self.access_keys = ["Open middle door", "Unlock the gate", "Grant me access"]
        self.access_keys_flag = False
        self.individuals = ["Person1", "Person2", "Person3", "Person4", "Person5", "Person6", "Person7", "Person8"]
        self.threshold = 0.5
        
        self.fingerprints = []
        self.ui.recordButton.clicked.connect(self.record_audio) 
        self.mode = None
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
        try:
            self.recorder.record_audio(label=self.recordingLabel)
            self.audio_data, self.sr, self.spectrogram, self.mfccs= self.recorder.get_audio_data('recorded_audio.wav')
            word, ind = self.process_audio()
            
            if self.mode == 1:
                self.person_access(word, ind)
            else:
                self.word_access(word, ind)
                
        except Exception as e:
            # Handle the exception, you can print an error message or log it
            print(f"Error in record_audio: {e}")

    def process_audio(self):
        try:
            # Plot Spectogram
            f.show_spectrogram(audio_data=self.recorder.data, sample_rate=self.recorder.sample_rate, canvas=self.canvas)
            
            # Individual Prediction
            c, p_ind, p_nam_ind = aT.file_classification('recorded_audio.wav', "svm_model", "svm_rbf")
            print(f'P({p_nam_ind[0]}={p_ind[0]})')
            print(f'P({p_nam_ind[1]}={p_ind[1]})')
            print(f'P({p_nam_ind[2]}={p_ind[2]})')
            
            # Word Prediction
            c_word, p_word, p_nam_word = aT.file_classification('recorded_audio.wav', "svm_model_words", "svm_rbf")
            print(f'P({p_nam_word[0]}={p_word[0]})')
            print(f'P({p_nam_word[1]}={p_word[1]})')
            print(f'P({p_nam_word[2]}={p_word[2]})')
            
            max_variable_word, max_value_word = max((("Open middle door", p_word[0]), ("Grant me access", p_word[1]),
                                         ("Unlock the gate", p_word[2])), key=lambda x: x[1])
            max_variable_ind, max_value_ind = max((("Habiba", p_ind[0]), ("Carole", p_ind[1]),
                                         ("Rana", p_ind[2])), key=lambda x: x[1])
            
            
            if max_value_word > 0.9:
                word = max_variable_word
            else:
                word = "Can't Recogonize your sentence"
                
            if max_value_ind > 0.95:
                ind = max_variable_ind
            else:
                ind = "Other"
            
            return word, ind

        except Exception as e:
            # Handle the exception, you can print an error message or log it
            print(f"Error in process_audio: {e}")

    def person_access(self, word, individual):
        if word != "Can't Recogonize your sentence":
            if individual != "Other":
                self.ui.resultLabel.setText("ACCESS DENIED")
            else:
                self.ui.resultLabel.setText(f"Hi {individual}")
        else:
            self.ui.resultLabel.setText("ACCESS DENIED")

    def word_access(self, word, individual):
        if word != "Can't Recogonize your sentence":
            self.ui.resultLabel.setText(f"Hi {individual}")
        else:
            self.ui.resultLabel.setText("ACCESS DENIED")
    
    def change_mode(self):
        # Voice Fingerprint Mode
        if self.ui.radioButton_2.isChecked()== True:
            self.comboBox.setEnabled(True)
            self.mode = 1
        
        # Voice Code Mode
        else:
            self.comboBox.setEnabled(False)
            self.mode = 2

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = SecurityVoiceCodeAccessApp()
    mainWin.show()
    sys.exit(app.exec())
