import os

def count_words_and_letters(input_string):
    # Count the number of words
    words = input_string.split()
    num_words = len(words)

    # Count the number of letters
    letters = ''.join(words)
    num_letters = len(letters)

    return num_words, num_letters

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

input_dir = '/Users/jinseokim/LDC_Analysis/NHN_full_corpus'

# 전체 어절 수 단어 수 저장할 변수생성
words = 0
letters = 0

for txt in os.listdir(input_dir):
    if txt.endswith('.txt'):
        # text 파일만 처리
        print("Processing file... {}".format(txt))

        # Read the content of the text file
        file_content = read_text_file(txt)

        # Call the function to count the number of words and letters
        num_words, num_letters = count_words_and_letters(file_content)

        print("Number of words:", num_words)
        print("Number of letters:", num_letters)

        words += num_words
        letters += num_letters


print("Total words: ", words)
print("Total letters: ", letters)