import librosa
import matplotlib.pyplot as plt
import numpy as np
import csv

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
