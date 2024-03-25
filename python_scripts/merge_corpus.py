import pandas as pd
import glob

# List to hold dataframes
dfs = []

# Specify your path where csv files are located
path = '/Users/jinseokim/LDC_Analysis/NHN_full_corpus/child_corpus/*.csv' 

# Read each csv file and append it to the list
for filename in glob.glob(path):
    df = pd.read_csv(filename, index_col=None, header=0)
    dfs.append(df)

# Concatenate all data into one DataFrame
all_data = pd.concat(dfs, ignore_index=True)

# Group by 'word' and 'pos_tag', then sum 'count'
result = all_data.groupby(['WORD', 'POS_TAG'])['COUNT'].sum().reset_index()

# Sort by 'count' in descending order
result = result.sort_values(by='COUNT', ascending=False)

# Write the sorted combined data to a new CSV file
result.to_csv('merged_children_word_frequency_counts.csv', index=False)
