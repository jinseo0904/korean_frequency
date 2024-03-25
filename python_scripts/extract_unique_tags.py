import pandas as pd

# Read the CSV file
csv_file_path = "/Users/jinseokim/LDC_Analysis/bareun_tokenizer/test_lines.csv"  # Replace with your CSV file path
df = pd.read_csv(csv_file_path)

# Select the second column "POS_Tag"
pos_tag_column = df["POS_Tag"]

# Get distinct values from the "POS_Tag" column
distinct_pos_tags = pos_tag_column.unique()

# Create a DataFrame with distinct values
distinct_pos_tags_df = pd.DataFrame(distinct_pos_tags, columns=["Distinct POS_Tag"])

# Save distinct values to a separate CSV file
output_csv_file = 'distinct_pos_tags.csv'
distinct_pos_tags_df.to_csv(output_csv_file, index=False)

print("Distinct POS tags saved to:", output_csv_file)
