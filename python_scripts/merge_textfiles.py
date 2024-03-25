# Specify the paths to the files
file1_path = 'free_chat_elderly_validation_clean_korean_only.txt'
file2_path = 'free_chat_elderly_training_clean_korean_only.txt'
merged_file_path = 'free_chat_elderly_merged.txt'

# Read the contents of the first file
with open(file1_path, 'r') as file1:
    lines1 = file1.readlines()

# Read the contents of the second file
with open(file2_path, 'r') as file2:
    lines2 = file2.readlines()

# Merge the contents
merged_lines = lines1 + lines2

# Write the merged content to a new file
with open(merged_file_path, 'w') as merged_file:
    merged_file.writelines(merged_lines)

# Print the total number of lines
print(f'Total number of lines: {len(merged_lines)}')
