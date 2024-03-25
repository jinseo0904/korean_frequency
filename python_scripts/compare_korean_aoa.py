import pandas as pd 

import scipy
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

freq = pd.read_csv("/Users/jinseokim/LDC_Analysis/LREC2024/korean_corpus_postprocessing/korean_frequencies_permil_added.csv")
aoa = pd.read_csv("/Users/jinseokim/LDC_Analysis/LREC2024/control_AOA.csv")

total_wordcount = freq["COUNT"].sum()
freq["WF_MIL"] = freq["COUNT"] / total_wordcount

wf = []
aoas = []
log = []

for index, row in aoa.iterrows():
	#print(row["Word"] + " " + row["POS"] + " " + str(row["AOA"]))

	# Find the row where WORD and POS_TAG match the specified values
	matching_row = freq[(freq["WORD"] == row["Word"]) & (freq["POS_TAG"] == row["POS"])]


	if not matching_row.empty:
	    count = matching_row["COUNT"].values[0]
	    key_word = row["Word"]
	    key_pos = row["POS"]
	    #print(f"Count for '{key_word}' with POS '{key_pos}': {count}\n\n")

	    # add to the list
	    aoas.append(row["AOA"])
	    wf.append(matching_row["WF_MIL"].values[0])
	    log.append(matching_row["WF_LOG"].values[0])
	else:

		import pandas as pd

assert len(aoas) == len(wf)
assert len(aoas) > 0

data = {
	"aoa" : aoas,
	"wf_mil" : wf,
	"log" : log
}

df = pd.DataFrame(data)
print("WF per million:")
print(stats.pearsonr(aoas, wf))

print("\n\nWF log10")
print(stats.pearsonr(aoas, log))




# Compare with WF from SUBTLEX

# Select rows where "POS_TAG" is equal to "NNG"
nng = freq[(freq["POS_TAG"] == "NNG") & (freq["COUNT"] > 3000)]

# Randomly sample 50 rows from the filtered DataFrame
#nng50 = nng.sample(n=50, random_state=42)  # Use a specific random state for reproducibility

#print(nng50)
#nng50.to_csv("sampled_nouns2.csv")

# plot correlation
#sns.lmplot(x="wf_mil", y="aoa", data=df)
#plt.show()
