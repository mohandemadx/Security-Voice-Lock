import wave
import soundfile as sf
import pyaudio
import threading

class AudioRecorder:
    def __init__(self, file_name, duration=5, sample_rate=44100):
        self.duration = duration
        self.sample_rate = sample_rate
        self.file_name = file_name
        self.frames = []

    def start_recording(self):
        recording_thread = threading.Thread(target=self.record_audio)
        recording_thread.start()

    def record_audio(self, label):
        p = pyaudio.PyAudio()

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
        wf = wave.open(self.file_name, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        print(f"Audio saved as {self.file_name}")

    def get_audio_data(self):
        # Load the audio file using soundfile
        data, _ = sf.read(self.file_name, dtype='float32')
        return data