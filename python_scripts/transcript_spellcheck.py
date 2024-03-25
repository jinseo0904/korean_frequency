import pandas as pd
import os
import sys
from hanspell import spell_checker


# 주어진 df 객체에 대해 맞춤법 검사 실행
def spellcheck_tsv(df, save_path, filename):
	correct = []

	for index, row in df.iterrows():
		if row.Section != '조음교대운동':
			result = spell_checker.check(row.Text)
			answer = result.as_dict()['checked']

            # 수정됐을 경우 해당 결과물 출력
			if (row.Text != answer):
				print('다음 text를 수정 완료: {0}  =======>  {1}'.format	(row.Text, answer))
		else:
			answer = row.Text
        
		correct.append(answer)
    
	df['Text'] = correct
	df.to_csv(save_path + filename[:-4] + '.tsv', encoding='utf-8', sep='\t')


# 주어진 directory 내부의 모든 tsv 파일들에 맞춤법 검사기를 돌려 파일을 새로 저장합니다.
if __name__ == '__main__':

    # 메인 프로그램으로서 실행 ...
    print("Input Directory:  {}".format(sys.argv[1]))
    input_dir = sys.argv[1]
    output_dir = input_dir + "/맞춤법_검사완료/"

    #디렉토리 없을 경우 생성
    if not(os.path.exists(output_dir)):
    	os.makedirs(output_dir)


    # Spellchecker 정상작동 확인용 더미코드
    result = spell_checker.check(u'안녕 하세요.')
    assert result.as_dict()['checked'] == '안녕하세요.'
    #print(result.as_dict()['checked'])

    for tsv in os.listdir(input_dir):

    	# tsv 파일에 한해 코드 실행
    	if (tsv[-4:] == '.tsv'): 
    		print("파일명 {}  처리중........".format(tsv))
    		filepath = input_dir + "/" + tsv

    		df = pd.read_csv(filepath, sep='\t')
    		spellcheck_tsv(df, output_dir, tsv)


