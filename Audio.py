import wave
import pyaudio
import librosa

class AudioRecorder:
    def __init__(self, file_name , duration=5, sample_rate=44100):
        self.duration = duration
        self.sample_rate = sample_rate
        self.file_name = file_name
        self.data = None

    def record_audio(self, duration=4, channels=1, sample_rate=44100, chunk_size=1024):
        p = pyaudio.PyAudio()

        # Open stream
        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

        print("Recording...")

        frames = []

        for _ in range(0, int(sample_rate / chunk_size * duration)):
            data = stream.read(chunk_size)
            frames.append(data)

        print("Recording done.")

        # Stop stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save the recorded audio as a WAV file
        with wave.open(self.file_name, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
        
            
    def get_audio_data(self):
        # Load the audio file
        data, _ = librosa.load(self.file_name, sr=self.sample_rate)
        return data

