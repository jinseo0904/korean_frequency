import pandas as pd

# Read the CSV files
file1 = pd.read_csv('/Users/jinseokim/LDC_Analysis/NHN_full_corpus/complete_free_chat_corpus_frequencies.csv')
file2 = pd.read_csv('elderly_frequency_counts.csv')
file3 = pd.read_csv('merged_children_word_frequency_counts.csv')

# Function to update the count in file1
def update_count(row):
    global file1
    word = row['WORD']
    pos_tag = row['POS_TAG']
    count = row['COUNT']
    
    # Get the index of the matching (WORD, POS_TAG) pair in file1
    index = file1[(file1['WORD'] == word) & (file1['POS_TAG'] == pos_tag)].index
    
    # If the (WORD, POS_TAG) pair exists in file1
    if not index.empty:
        idx = index[0]
        
        # Subtract the count
        file1.at[idx, 'COUNT'] -= count
        
        # If the count becomes less than 1, remove the row
        if file1.at[idx, 'COUNT'] < 1:
            file1 = file1.drop(idx)

# Iterate through each row of file2 and file3 and update the count in file1
print("Processing elderly frequencies...")
file2.apply(update_count, axis=1)
print("Processing child frequencies...")
file3.apply(update_count, axis=1)

# Write the updated file1 DataFrame to a new CSV file
file1.to_csv('adult_frequency_counts_final.csv', index=False)
