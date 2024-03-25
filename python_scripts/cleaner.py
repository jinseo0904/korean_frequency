# import konlpy
import string
from tqdm import tqdm

# Using readlines()
file1 = open(r'/Users/jinseokim/LDC_Analysis/nhn_corpus_training_total.txt', 'r')
Lines = file1.readlines()

no_punct = []
count = 0
for line in tqdm(Lines):

	# Translation table for removing punctuation
	translator = str.maketrans("", "", string.punctuation)

	# Remove punctuation from text
	text_without_punct = line.translate(translator)

	if line != text_without_punct:
		#print("Cleaned the line: {0} ====> {1}".format(line, text_without_punct))
		count += 1

	no_punct.append(text_without_punct)

print(len(no_punct))

print("Cleaned {} lines in total".format(count))

with open(r'/Users/jinseokim/LDC_Analysis/nhn_corpus_training_total_clean.txt', 'w') as file:
	for line in no_punct:
		file.writelines(line)

# Using readlines()
file2 = open(r'/Users/jinseokim/LDC_Analysis/nhn_corpus_validation_total.txt', 'r')
Lines = file2.readlines()

no_punct = []
count = 0
for line in tqdm(Lines):

	# Translation table for removing punctuation
	translator = str.maketrans("", "", string.punctuation)

	# Remove punctuation from text
	text_without_punct = line.translate(translator)

	if line != text_without_punct:
		#print("Cleaned the line: {0} ====> {1}".format(line, text_without_punct))
		count += 1

	no_punct.append(text_without_punct)

print(len(no_punct))

print("Cleaned {} lines in total".format(count))

with open(r'/Users/jinseokim/LDC_Analysis/nhn_corpus_validation_total_clean.txt', 'w') as file:
	for line in no_punct:
		file.writelines(line)



