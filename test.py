import os
import pandas as pd

def append_to_csv(file_path, data_frame):
    # Check if the file exists
    file_exists = os.path.exists(file_path)
    
    # Append DataFrame to the CSV file
    data_frame.to_csv(file_path, mode='a', header=not file_exists, index=False, columns=data_frame.columns)

# Example usage:
# Create a DataFrame
data = {'Name': ['John', 'Alice', 'Bob'],
        'Age': [25, 30, 35],
        'City': ['New York', 'San Francisco', 'Los Angeles']}
df = pd.DataFrame(data)

# Append DataFrame to a CSV file
append_to_csv('example.csv', df)
