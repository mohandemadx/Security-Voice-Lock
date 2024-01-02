import wave
import librosa
import soundfile as sf
import pyaudio
import threading
import numpy as np

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
        wf = wave.open(self.file_name, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        print(f"Audio saved as {self.file_name}")

    def get_audio_data(self):
        # Read the audio file using soundfile
        self.data, self.sr = librosa.load(self.file_name)
    
    def calculate_fingerprint(self):
        try:
            if self.data is not None:
                stft = librosa.stft(y=self.data)

                # Calculate chroma features
                chroma = librosa.feature.chroma_stft(S=stft)
                # Mean Chroma
                mean_chroma = np.mean(chroma, axis=1)

                # Calculate zero-crossing rate (applied to the time-domain signal)
                zero_crossings = librosa.feature.zero_crossing_rate(self.data)

                
                # Calculate Mel-Frequency Cepstral Coefficients (MFCCs)
                mfcc = librosa.feature.mfcc(sr=self.sr, S=stft)
                std_mfcc = np.std(mfcc, axis=1)

                # Calculate energy envelope
                energy = np.sum(np.abs(stft), axis=0)

                print(np.angle(mean_chroma).shape, np.abs(mean_chroma).shape, std_mfcc.shape, zero_crossings.flatten().shape, energy.shape)
                
                # Combine all features into a single fingerprint
                fingerprint = np.concatenate([np.angle(mean_chroma), np.abs(mean_chroma), std_mfcc, zero_crossings.flatten(), energy])
                print(fingerprint.shape)
                
                return fingerprint
            else:
                print("Audio data is None. Please call get_audio_data() first.")

        except Exception as e:
            print(f"Error calculating fingerprint: {e}")

            # # Calculate statistical descriptors
            
            # std_mfcc = np.std(mfcc, axis=1)
            # print(mean_chroma.shape(), std_mfcc.shape(), zero_crossings.shape(), energy.shape())
            # # Combine all features into a single fingerprint
            # fingerprint = np.concatenate([mean_chroma, std_mfcc, zero_crossingsflatten(), energy])


        
