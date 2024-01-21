import threading
import wave
import librosa
import pyaudio
import numpy as np
from pyAudioAnalysis import audioTrainTest as aT
from PyQt5.QtCore import QThread, pyqtSignal


class AudioRecorder:
    
    def __init__(self, file_name, duration=3, sample_rate=44100):
        self.duration = duration
        self.sample_rate = sample_rate
        self.file_name = file_name
        self.frames = []
        self.data = None
        self.sr = None
        self.threshold_words = 0.9
        self.threshold_ind = 0.7

    def start_recording(self):
        recording_thread = threading.Thread(target=self.record_audio)
        recording_thread.start()
          
    def record_audio(self):
        p = pyaudio.PyAudio()
        self.frames = []
        # Open stream
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=self.sample_rate,
                        input=True,
                        frames_per_buffer=1024)
        
        
        
        print("Recording...")

        for _ in range(0, int(self.sample_rate / 1024 * self.duration)):
            data = stream.read(1024)
            self.frames.append(data)
        
        
        print("Recording done.")

        # Stop stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        self.save_audio()

    def save_audio(self):
        wf = wave.open(self.file_name, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        print(f"Audio saved as {self.file_name}")

    def get_audio_data(self):
        # Read the audio file using linrosa
        self.data, self.sr = librosa.load(self.file_name, dtype=np.float32)
        
    def process_audio(self):
        # Individual Prediction
        c_ind, p_ind, p_nam_ind = aT.file_classification('recorded_audio.wav', "svm_model", "svm_rbf")
        print(f'P({p_nam_ind[0]}={p_ind[0]})')
        print(f'P({p_nam_ind[1]}={p_ind[1]})')
        print(f'P({p_nam_ind[2]}={p_ind[2]})')
        print(f'P({p_nam_ind[3]}={p_ind[3]})')
        
        # Word Prediction
        c_word, p_word, p_nam_word = aT.file_classification('recorded_audio.wav', "svm_model_words", "svm_rbf")
        print(f'P({p_nam_word[0]}={p_word[0]})')
        print(f'P({p_nam_word[1]}={p_word[1]})')
        print(f'P({p_nam_word[2]}={p_word[2]})')
        
        max_variable_word, max_value_word = max((("Open middle door", p_word[0]), ("Grant me access", p_word[1]),
                                        ("Unlock the gate", p_word[2])), key=lambda x: x[1])
        max_variable_ind, max_value_ind = max((("Habiba", p_ind[0]), ("Carole", p_ind[1]),
                                        ("Rana", p_ind[2]), ("Mohand", p_ind[3])), key=lambda x: x[1])
        
        
        if max_value_word > self.threshold_words:
            word = max_variable_word
        else:
            word = "Can't Recogonize your sentence"
            
        if max_value_ind > self.threshold_ind:
            ind = max_variable_ind
        else:
            ind = "Other"
        
        return word, ind


class RecordThread(QThread):
    finished = pyqtSignal()

    def __init__(self, audio_recorder):
        super().__init__()
        self.audio_recorder = audio_recorder

    def run(self):
        self.audio_recorder.record_audio()
        self.finished.emit()