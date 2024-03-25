# import konlpy
from collections import Counter
from bareunpy import Tagger
from tqdm import tqdm
import os

# 바른 tokenizer 초기화
API_KEY="koba-ON6NEQI-6ZPUS6I-UJEI2SA-EUIRDSA"
tagger = Tagger(API_KEY, 'localhost')

# Using readlines()
text_dir = "/Users/jinseokim/LDC_Analysis/NHN_full_corpus/"
txt_file = "free_chat_elderly_merged.txt"
txtpath = os.path.join(text_dir, txt_file)

print("Reading file ... {}".format(txt_file))
file1 = open(txtpath, 'r')
Lines = file1.readlines()


token_list = []

# threshold and start values
start = 0
threshold = 1990000


count = 0

for line in tqdm(Lines):
	if count < start:
		count += 1
		continue


	try:
		# 바른 사용해 pos 태깅
		res = tagger.tags([line])
		toks = res.pos()

		for word, pos in toks:
			combined = word + '_' + pos
			token_list.append(combined)
	except:
		print("Error processing the following line: {}".format(line))
		continue
	finally:
		count += 1

		# finish if count = threshold
		if count == threshold:
			print("INFO: finished processing {} lines.".format(count))
			break

'''
# Using readlines()
text_filename = '/Users/jinseokim/LDC_Analysis/NHN_full_corpus/free_chat_elderly_validation.txt'
file2 = open(r'/Users/jinseokim/LDC_Analysis/nhn_corpus_validation_total_clean.txt', 'r')
Lines = file2.readlines()

for line in tqdm(Lines):

	try:
		toks = komoran.pos(line)
		for word, pos in toks:
			combined = word + '_' + pos
			token_list.append(combined)
	except:
		print("Error processing the following line: {}".format(line))
		continue
'''

# counter 생성 및 frequency 기준으로 내림차순 정렬
print("Done tokenizing. Now counting frequencies...")
word_frequency = Counter(token_list)
sorted_frequencies = word_frequency.most_common()

dirname = '/Users/jinseokim/LDC_Analysis/NHN_full_corpus/'
filename = 'elderly_corpus_from_{}_to_{}.csv'.format(start, count)

print("Done sorting counts. Saving to : ", filename)

# csv 파일에 정렬해서 저장
with open(os.path.join(dirname, filename), 'w') as file:
	file.writelines("WORD" + "," + "POS_TAG" + "," + "COUNT" + '\n')
	for key, value in sorted_frequencies:
		#split the string
		try:
			word, pos = key.split("_")
			file.writelines(word + "," + pos + "," + str(value) + '\n')
		except:
			print("ERROR processing the token: {}".format(key))
			continue




