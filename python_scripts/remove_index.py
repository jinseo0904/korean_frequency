import pandas as pd

# Load CSV file into a DataFrame
csv_file_path = "korean_frequencies_permil_added.csv"  # Replace with the actual file path
df = pd.read_csv(csv_file_path)

# Remove the index column
df = df.drop(columns=['Unnamed: 0'])  # Replace 'Unnamed: 0' with the actual column name

# Save the modified DataFrame to a new CSV file
output_csv_path = 'modified_file.csv'  # Replace with the desired output file path
df.to_csv(output_csv_path, index=False)

print("Modified DataFrame saved to", output_csv_path)
