
import pandas as pd

# Create a sample DataFrame
data = {'Column1': [1, 2, 3, 4, None],
        'Column2': [5, 6, None, 8, 9]}
df = pd.DataFrame(data)

# Display the original DataFrame
print("Original DataFrame:")
print(df)

# Remove rows with NaN values
df_cleaned = df.dropna()

# Display the DataFrame after removing rows with NaN values
print("\nDataFrame after removing rows with NaN values:")
print(df_cleaned)