from functions import append_row_to_csv
from Audio import AudioRecorder
from functions import calculate_fingerprint
files = ["recorded_audio.wav"]  # list of all the files names

for name in files:
    recorder = AudioRecorder(file_name=name)
    recorder.data = recorder.get_audio_data()
    recorder.process_audio()
    row = calculate_fingerprint(recorder.data)+['open']+['habiba']
    
# Append DataFrame to a CSV file
append_row_to_csv('training_data.csv', row)

