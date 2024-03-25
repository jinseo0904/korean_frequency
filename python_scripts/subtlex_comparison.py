import pandas as pd
from scipy import stats

kor = pd.read_csv("/Users/jinseokim/LDC_Analysis/LREC2024/final_word_frequency/all_speakers_frequency_counts_final.csv")
sub = pd.read_excel("/Users/jinseokim/LDC_Analysis/LREC2024/subtl.xlsx")
sub["Word"] = sub["Word"].str.lower()

# Load CSV file into a DataFrame
csv_file_path = "/Users/jinseokim/LDC_Analysis/LREC2024/concrete_words.csv"  # Replace with the actual file path
df = pd.read_csv(csv_file_path)

# Filter rows where "Korean" column value is not empty
words_to_compare = df[df['Korean'].notna()]

# initialize
words_kor_wf = []
words_eng_wf = []

# log10 data
words_kor_log = []
words_eng_log = []


for index, row in words_to_compare.iterrows():
    #print("Processing... ", row["Word"])
    matching_eng = sub[(sub["Word"] == row["Word"])]
    matching_kor = kor[(kor["WORD"] == row["Korean"]) & (kor["POS_TAG"].isin(["NNG", "NNP", "VV"]))]
    
    # if there is no matching Korean term, skip
    if (matching_kor.shape[0] == 0):
        print("Word {} is not registered in the Korean corpus. Skipping...".format(row["Word"]))
        continue

    words_kor_wf.append(matching_kor["COUNT_ADJUST"].values[0])
    words_eng_wf.append(matching_eng["FREQcount"].values[0])

    words_kor_log.append(matching_kor["LOG10"].values[0])
    words_eng_log.append(matching_eng["LG10WF"].values[0])


assert len(words_eng_wf) == len(words_kor_wf)
print(len(words_eng_wf))

wf = {
    "kor" : words_kor_wf,
    "eng" : words_eng_wf
}

log = {
     "kor" : words_kor_log,
    "eng" : words_eng_log
}

# initialize dataframes and print correlation data
wf_mil = pd.DataFrame(wf)
wf_log = pd.DataFrame(log)

res = stats.spearmanr(words_kor_wf, words_eng_wf)
print(res)


# print output
print("Using n = {} words for comparison.".format(len(words_eng_log)))
print("\n\n FREQ Count correlations:")
print(wf_mil.corr())
print(stats.pearsonr(words_kor_wf, words_eng_wf).pvalue)
print("\n\n WF log10 correlations:")
print(wf_log.corr())
print(stats.pearsonr(words_kor_log, words_eng_log))