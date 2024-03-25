import sys
from bareunpy import Tagger
from konlpy.tag import Hannanum, Kkma, Komoran, Mecab
import csv
import pandas as pd

def main():
    # tokenizer type 확인
    tokenizer_type = sys.argv[1]


    API_KEY="koba-ON6NEQI-6ZPUS6I-UJEI2SA-EUIRDSA"
    kkma = Kkma()
    komoran = Komoran()
    hannanum = Hannanum()

    # 방금 설치한 자신의 호스트에 접속합니다.
    tagger = Tagger(API_KEY, 'localhost')

    bareun = []
    tokens = []

    filename = "/Users/jinseokim/LDC_Analysis/bareun_tokenizer/50_sentences.csv"
    
    df = pd.read_csv(filename)

    for index, row in df.iterrows():
        print("Line number {0}: {1}".format(index, row["Sentences"]))
        # comment this line if you're not using Bareun
        res = tagger.tags([row["Sentences"]])
        result = res.pos()

        #result = komoran.pos(row["Sentences"])

        bareun += result
        tokens += [index + 1 for x in range(len(result))]

    #word = ["똑같이 사실만 얘기할 것입니다"]
    #res = tagger.tags(word)
    #print('Original: {}'.format(word))
    #print("Bareun: " + str(res.pos()))
    #print("Kkma: " + str(kkma.pos(word[0])))
    #print("Komoran: " + str(komoran.pos(word[0])))
    #print("Hannanum: " + str(hannanum.pos(word[0])))
    #print("")

    # Path to the output CSV file
    csv_file_path = tokenizer_type + '_output.csv'

    # Write data to CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write header
        csv_writer.writerow(['Token', 'POS_Tag', 'Line_No'])
        
        # Write data from each tuple and corresponding integer
        for item_tuple, item_integer in zip(bareun, tokens):
            csv_writer.writerow(item_tuple + (item_integer,))

    print("CSV file saved:", csv_file_path)

if __name__ == "__main__":
    main()
