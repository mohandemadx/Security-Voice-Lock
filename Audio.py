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
        wf = wave.open(self.file_name, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        print(f"Audio saved as {self.file_name}")

    def get_audio_data(self, file_name):
        # Read the audio file using soundfile
        self.data, self.sr = librosa.load(file_name, dtype=np.float32)
        spectrogram = np.abs(librosa.stft(y, hop_length=hop_length, n_fft=n_fft))
        return spectrogram

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
                mfcc = librosa.feature.mfcc(y=self.data,sr=self.sr,n_mfcc=40).flatten()
                delta = librosa.feature.delta(mfcc).flatten()
                delta2 = librosa.feature.delta(mfcc,order=2).flatten()
                feature_vector = np.concatenate([mfcc,delta,delta2])

                # Transpose the feature vector to have frames as columns
                fingerprint = feature_vector


                # Calculate energy envelope
                # energy = np.sum(np.abs(stft), axis=0)

                # print(np.angle(mean_chroma).shape, np.abs(mean_chroma).shape, std_mfcc.shape, zero_crossings.flatten().shape, energy.shape)
                
                # Combine all features into a single fingerprint
                # fingerprint = np.concatenate([mfcc, delta, delta2])
                print(fingerprint.shape)
                # (12,) (12,) (20,) (130,) (130,) (304,)
                
                return fingerprint
            else:
                print("Audio data is None. Please call get_audio_data() first.")

        except Exception as e:
            print(f"Error calculating fingerprint: {e}")

    def detect_word(self, spectogram):
        specto1 = get_audio_data('open_middle_door.wav')
        specto2 = get_audio_data('grant_me_access.wav')
        specto3 = get_audio_data('unlock_the_gate.wav')
        word_dictionary = {
            open_middle_door: specto1,
            grant_me_access: specto2,
            unlock_the_gate: specto3,
        }
        sim_open = f.calc_similarity(word_dictionary[open_middle_door], spectogram)
        sim_grant = f.calc_similarity(word_dictionary[grant_me_access], spectogram)
        sim_unlock = f.calc_similarity(word_dictionary[unlock_the_gate], spectogram)

        max_variable, max_value = max((("Open middle door", sim_open), ("Grant me access", sim_grant), ("Unlock the gate", sim_unlock)), key=lambda x: x[1])
        if max_value > THRES:
            return max_variable
        else:
            return 'no match'

