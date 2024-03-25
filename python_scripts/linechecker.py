# import konlpy
import string
from tqdm import tqdm

# Using readlines()
file1 = open(r'/Users/jinseokim/LDC_Analysis/nhn_corpus_training_total_clean.txt', 'r')
Lines = file1.readlines()

print("File 1 has {} lines in total".format(len(Lines)))

# Using readlines()
file2 = open(r'/Users/jinseokim/LDC_Analysis/nhn_corpus_validation_total_clean.txt', 'r')
Lines = file2.readlines()

print("File 12has {} lines in total".format(len(Lines)))



