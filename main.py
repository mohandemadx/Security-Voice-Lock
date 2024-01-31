import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5 import uic
from PyQt5.QtGui import QIcon


# CLASSES
from Audio import AudioRecorder, RecordThread
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
        self.individuals = ["Habiba", "Mohand", "Carol", "Rana", "Mirna", "Omar", "Person7", "Person8"]
        
        self.ui.recordButton.clicked.connect(self.record_audio)
        self.mode = None
        self.load_ui_elements()


    def load_ui_elements(self):
        self.ui.resultLabel.setText("ACCESS DENIED")
        self.ui.radioButton_2.clicked.connect(self.change_mode)
        self.ui.radioButton.clicked.connect(self.change_mode)
        self.ui.recordButton.setIcon(QIcon('icons\mic-svgrepo-com.png'))
        self.ui.lockbutton.setIcon(QIcon('icons/unlock.png'))
        self.ui.iconWORD.setIcon(QIcon('icons/promo.png'))
        self.ui.iconIND.setIcon(QIcon('icons/coding.png'))
        
        # Create instances of AudioRecorder for recording audio
        self.recorder = AudioRecorder(file_name='recorded_audio.wav')
        self.audio_thread = RecordThread(self.recorder)
        
        
    def record_audio(self):
        self.ui.recordingLabel.setText("Recording...")
        self.ui.recordButton.setIcon(QIcon('icons/recording3.png'))
        self.ui.recordButton.setStyleSheet("border-radius: 40px; background-color: red; color: white;")
        
        # Disconnect the slot if it was previously connected
        try:
            self.audio_thread.finished.disconnect(self.on_finished)
        except TypeError:
            # Ignore the error if the slot was not connected
            pass
        # Connect the slot
        self.audio_thread.finished.connect(self.on_finished)
        self.audio_thread.start()
        
        
    def on_finished(self):
        self.ui.recordButton.setIcon(QIcon('icons/mic-svgrepo-com.png'))
        self.ui.recordButton.setStyleSheet("border-radius: 40px; background-color: black; color: white;")
        self.recorder.get_audio_data()
        self.ui.recordingLabel.setText("Recording Done.")
        
        # Plot Spectogram
        f.show_spectrogram(audio_data=self.recorder.data, sample_rate=self.recorder.sr, frame=self.ui.spectoFrame)
        word, ind, data = self.recorder.process_audio()
        
        f.create_table(data, self.ui.tableFrame)
        
        print("---------------------------------------------------------------")
        print(f"Your Sentence is most Probably: {word}")
        print(f"The Person who said the sentence is most Probably: {ind}")
        
        if self.mode == 1:
            self.person_access(word, ind)
        else:
            self.word_access(word, ind)


    def person_access(self, word, individual):
        if word != "Can't Recogonize your sentence":
            if individual != "Other":
                self.ui.resultLabel.setText(f"Hi {individual}")
                self.ui.lockbutton.setIcon(QIcon('icons/padlock.png'))
            else:
                self.ui.lockbutton.setIcon(QIcon('icons/unlock.png'))
                self.ui.resultLabel.setText("ACCESS DENIED")
        else:
            self.ui.resultLabel.setText("ACCESS DENIED")
            self.ui.lockbutton.setIcon(QIcon('icons/unlock.png'))


    def word_access(self, word, individual):
        if word != "Can't Recogonize your sentence":
            self.ui.resultLabel.setText(f"Hi {individual}")
            self.ui.lockbutton.setIcon(QIcon('icons/padlock.png'))
        else:
            self.ui.resultLabel.setText("ACCESS DENIED")
            self.ui.lockbutton.setIcon(QIcon('icons/unlock.png'))


    def change_mode(self):
        # Voice Fingerprint Mode
        if self.ui.radioButton_2.isChecked()== True:
            self.mode = 1
        
        # Voice Code Mode
        else:
            self.mode = 2
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = SecurityVoiceCodeAccessApp()
    mainWin.show()
    sys.exit(app.exec())
