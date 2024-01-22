from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances
from fastdtw import fastdtw
import matplotlib.pyplot as plt


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

    
def show_spectrogram(audio_data, sample_rate, frame):
    # Create instances of MplWidget for spectrogram
    canvas = FigureCanvas(plt.Figure())
    
    
    # Set up layouts for spectrogram widgets
    addwidget(canvas, frame)
    
    
    plt.close()
    plt.figure()
    plt.specgram(audio_data, Fs=sample_rate, cmap='viridis', aspect='auto')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Spectrogram')
    canvas.figure.clear()
    canvas.figure = plt.gcf()
    canvas.draw()


def create_table(data, frame):
    canvas = FigureCanvas(plt.Figure())
    addwidget(canvas, frame)
    
    fig, ax = plt.subplots()

    # Create a table and add it to the axes
    table = ax.table(cellText=data, loc='center', cellLoc='center', colLabels=['Individual/Sentence', 'Match %'])

    # Style the table
    table.auto_set_font_size(True)
    table.set_fontsize(14)
    table.scale(1, 3)  # Adjust the size of the table

    # Set cell colors for a light modern color scheme
    for i in range(len(data) + 1):
        for j in range(len(data[0])):
            if i == 0:  # Header row
                color = 'lightblue'
            else:  # Even rows
                color = 'whitesmoke'
            
            table[(i, j)].set_facecolor(color)

    # Remove the axes
    ax.axis('off')

    canvas.figure.clear()
    canvas.figure = plt.gcf()
    canvas.draw()