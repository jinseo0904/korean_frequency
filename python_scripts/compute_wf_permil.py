import numpy as np
import pandas as pd

kor = pd.read_csv("/Users/jinseokim/LDC_Analysis/LREC2024/korean_frequencies.csv")

# number of hits / corpus size in millions of tokens = frequency per million
corpus_size = kor["COUNT"].sum()
size_in_mil = corpus_size / 1000000
print(size_in_mil)

kor["WF_MIL"] = kor["COUNT"] / size_in_mil
kor["WF_LOG"] = np.log10(kor["WF_MIL"])

kor.to_csv("korean_frequencies_permil_added.csv")