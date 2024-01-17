import wave
import librosa
import soundfile as sf
import pyaudio
import threading
import numpy as np
import functions as f

class AudioRecorder:
    def __init__(self, file_name, duration=3, sample_rate=44100):
        self.duration = duration
        self.sample_rate = sample_rate
        self.file_name = file_name
        self.frames = []
        self.data = None
        self.sr = None

    def start_recording(self):
        recording_thread = threading.Thread(target=self.record_audio)
        recording_thread.start()

    def record_audio(self, label):
        p = pyaudio.PyAudio()
        self.frames = []
        # Open stream
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=self.sample_rate,
                        input=True,
                        frames_per_buffer=1024)
        
        label.setText("Recording...")
        
        print("Recording...")

        for _ in range(0, int(self.sample_rate / 1024 * self.duration)):
            data = stream.read(1024)
            self.frames.append(data)
        
        label.setText("Recording Done.")
        
        print("Recording done.")

        # Stop stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        self.save_audio()

    def save_audio(self):
        # # Convert the byte string to a numpy array
        # audio_data = np.frombuffer(b''.join(self.frames), dtype=np.int16)
        #
        # # Trim leading and trailing silence
        # trimmed_audio, _ = librosa.effects.trim(audio_data)
        wf = wave.open(self.file_name, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        print(f"Audio saved as {self.file_name}")

    def get_audio_data(self, file_name):
        # Read the audio file using soundfile
        try:
            self.data, self.sr = librosa.load(file_name, dtype=np.float32)
            mfcc = librosa.feature.mfcc(y=self.data, sr=self.sr, n_mfcc=60)
            spectogram = np.abs(librosa.stft(y=self.data))
            return self.data, self.sr, spectogram, mfcc

        except Exception as e:
            # Handle the exception, you can print an error message or log it
            print(f"Error here: {e}")

    