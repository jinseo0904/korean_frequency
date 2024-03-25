import pandas as pd 
import sys

subtlex = pd.read_excel("subtlex_pos.xlsx")
concrete = pd.read_excel("/Users/jinseokim/LDC_Analysis/LREC2024/concreteness.xlsx")

# load already saved dataset
current = pd.read_csv("/Users/jinseokim/LDC_Analysis/LREC2024/concrete_words.csv")

sorted_df = concrete.sort_values(by="Conc.M", ascending=False)

# choose Nouns only
noun = subtlex[subtlex["All_PoS_SUBTLEX"] == "Adjective"]

# initialize lists
bigram, concr, sub = [], [], []

# fetch concrete data
for index, row in noun.iterrows():
	word = row["Word"]

	matching_row = concrete[concrete["Word"] == row["Word"]]
	# if there is no matching Korean term, skip
	if (matching_row.shape[0] == 0):
		print("Word {} is not registered in the corpus. Skipping...".format(row["Word"]))
		bigram.append(-1)
		concr.append(-1)
		sub.append(-1)
		continue

	else:
		bigram.append(matching_row["Bigram"].values[0])
		concr.append(matching_row["Conc.M"].values[0])
		sub.append(matching_row["SUBTLEX"].values[0])


noun["Bigram"] = bigram
noun["Conc"] = concr
noun["SUBTLEX"] = sub


# filter single words only
words = noun[(noun["Bigram"] == 0) & (noun["Conc"] > 3.0) & (noun["SUBTLEX"] > 100)]
#print(words.head())

# sample rows
num = sys.argv[1]
print(words.shape[0])
sample = words.sample(n=int(num), random_state=42)


sample["Korean"] = None
#concatenated_df = pd.concat([current, sample], ignore_index=True)
concatenated_df = sample
clean = concatenated_df.drop_duplicates(subset=["Word"], keep="first")

# drop dummy columns
columns_to_drop = [col for col in clean.columns if col.startswith("Unnamed")]
df_dropped = clean.drop(columns=columns_to_drop)

# Select and keep only specific columns
selected_columns = ["Word", "SUBTLEX", "Korean"]
df = df_dropped.loc[:, selected_columns]
df.to_csv("concrete_adj.csv")

