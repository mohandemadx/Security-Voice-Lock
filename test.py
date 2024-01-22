import matplotlib.pyplot as plt
from matplotlib.table import Table

def create_table(data):
    fig, ax = plt.subplots()

    # Create a table and add it to the axes
    table = ax.table(cellText=data, loc='center', cellLoc='center', colLabels=['Column 1', 'Column 2', 'Column 3'])

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)  # Adjust the size of the table

    # Set cell colors for a light modern color scheme
    for i in range(len(data) + 1):
        for j in range(len(data[0])):
            if i == 0:  # Header row
                color = 'lightgray'
            elif i % 2 == 0:  # Even rows
                color = 'whitesmoke'
            else:  # Odd rows
                color = 'lightgray'
            
            table[(i, j)].set_facecolor(color)

    # Remove the axes
    ax.axis('off')

    plt.show()

# Sample data
data = [
    ['A1', 'B1', 'C1'],
    ['A2', 'B2', 'C2'],
    ['A3', 'B3', 'C3']
]

create_table(data)
