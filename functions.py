import librosa
import matplotlib.pyplot as plt
import numpy as np
import csv
from sklearn.metrics.pairwise import cosine_similarity

def clear(frame):
    layout = frame.layout()
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
                
def addwidget(widget, frame):
    clear(frame)
    layout = frame.layout()
    layout.addWidget(widget)
    
    frame.setLayout(layout)
    
def show_spectrogram(audio_data, sample_rate, canvas):
    plt.close()
    plt.figure()
    plt.specgram(audio_data, Fs=sample_rate, cmap='viridis', aspect='auto')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Spectrogram')
    canvas.figure.clear()
    canvas.figure = plt.gcf()
    canvas.draw()

    
def append_row_to_csv(file_path, new_row):
    try:
        # Open the CSV file in append mode
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)

            # Write the new row to the CSV file
            writer.writerow(new_row)

        print("Row appended to CSV successfully.")
    except Exception as e:
        print(f"Error: {e}")

def get_audio_data(file_name, num_mfcc=13, hop_length = 512, n_fft = 2048):
        # Read the audio file using soundfile
        data, sr = librosa.load(file_name, dtype=np.float32)
        spectogram = np.abs(librosa.stft(y=data, hop_length=hop_length, n_fft=n_fft))
        mfccs = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=num_mfcc)
        return data, sr, spectogram, mfccs

    
def detect_word(spectogram, mfccs):
        _, _, specto1, mfcc1 = get_audio_data('sentence_audio/open_middle_door.wav')
        _, _, specto2, mfcc2 = get_audio_data('sentence_audio/grant_me_access.wav')
        _, _, specto3, mfcc3 = get_audio_data('sentence_audio/unlock_the_gate.wav')
        word_dictionary = {
            'open_middle_door': [specto1, mfcc1],
            'grant_me_access': [specto2, mfcc2],
            'unlock_the_gate': [specto3, mfcc3],
        }
        print(specto1.shape, spectogram.shape)
        
        sim_open_spec = calc_similarity(word_dictionary['open_middle_door'][0], spectogram)
        sim_grant_spec = calc_similarity(word_dictionary['grant_me_access'][0], spectogram)
        sim_unlock_spec = calc_similarity(word_dictionary['unlock_the_gate'][0], spectogram)
        print(f"Similarity SPECTO:{[sim_open_spec, sim_grant_spec, sim_unlock_spec]}")
        
        sim_open_mfcc = calc_similarity(word_dictionary['open_middle_door'][1], mfccs)
        sim_grant_mfcc = calc_similarity(word_dictionary['grant_me_access'][1], mfccs)
        sim_unlock_mfcc = calc_similarity(word_dictionary['unlock_the_gate'][1], mfccs)
        print(f"Similarity MFCCs:{[sim_open_mfcc, sim_grant_mfcc, sim_unlock_mfcc]}")

        max_variable1, max_value1 = max((("Open middle door", sim_open_spec), ("Grant me access", sim_grant_spec), ("Unlock the gate", sim_unlock_spec)), key=lambda x: x[1])
        print(f"Output of SPECTO: {max_variable1, max_value1}")
        
        max_variable2, max_value2 = max((("Open middle door", sim_open_mfcc), ("Grant me access", sim_grant_mfcc), ("Unlock the gate", sim_unlock_mfcc)), key=lambda x: x[1])
        print(f"Output of MFCCs: {max_variable2, max_value2}")
        
        # habiba lma tft7yy zbty l voices bsotek w i recommend enk t3mleehom phases mo5tlfa y3ny wa7da fehom mt't3a 
        # w wa7da takleha kda w wa7da tbd'y 3ltool w zbty b'a l thresholds o3ody el3by bl keywords w 4ofy l terminal
        # trail and error b'a w rbna m3aaky
        
        # if max_variable1 == "Open middle door":
        #     THRES = 0.38
        # else:
        #     sentence = max_variable1
        #     SURE = 80
            
        # if SURE == 100:
        #     return sentence, SURE
        # elif SURE == 80:
        #     return sentence, 
        # else:
        #     return 'no match'
        
def calc_similarity(spec1, spec2):
    spec1_flat = spec1.flatten()
    spec2_flat = spec2.flatten()
    similarity = cosine_similarity([spec1_flat], [spec2_flat])[0][0]
    return similarity


def compute_spectrogram(audio_file, hop_length=512, n_fft=2048):
    y, sr = librosa.load(audio_file)
    spectrogram = np.abs(librosa.stft(y, hop_length=hop_length, n_fft=n_fft))
    return spectrogram


# def create_sentence_templates(sentences):
#     templates = {}
#     for sentence in sentences:
#         template = generate_spectrogram(f'path_to_template_{sentence.replace(" ", "_")}.wav')
#         templates[sentence] = template
#     return templates
#
# def create_individual_templates(individuals):
#     templates = {}
#     for individual in individuals:
#         template = generate_spectrogram(f'path_to_template_{individual}.wav')
#         templates[individual] = template
#     return templates
#
# def template_matching(spectrogram, templates):
#     matches = {}
#     for name, template in templates.items():
#         correlation = correlate2d(spectrogram, template, mode='same')
#         match_position = np.unravel_index(np.argmax(correlation), correlation.shape)
#         matches[name] = match_position
#
#     best_match = min(matches, key=lambda x: matches[x])
#     return best_match, matches[best_match]
