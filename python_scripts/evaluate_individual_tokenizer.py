import csv
import pandas as pd
import statistics
import sys
from Levenshtein import distance
import math
from jiwer import wer

def eval_each_sentence(gt, pred, line_number):
	true_pos = gt[gt["Line_No"] == line_number]
	pred_pos = pred[pred["Line_No"] == line_number]

	# POS tag 보정용
	tokenizer_output = []
	gt_tagging = []
	line_no = []

	print("\n\n\nEvaluating line {}...".format(line_number))
	#print(true_pos.shape[0])
	#print(pred_pos.shape[0])
	gttoken = true_pos["Token"].tolist()

	# Remove white spaces from each string in the list
	gttoken = [s.replace(" ", "") for s in gttoken]
	ptoken = pred_pos["Token"].tolist()

	gpos = true_pos["POS_Tag"].tolist()
	gpos = [s.replace(" ", "") for s in gpos]
	ppos = pred_pos["POS_Tag"].tolist()

	ppos = ['NA' if pd.isna(value) else value for value in ppos]


	attempt = [(t, p) for t, p in zip(ptoken, ppos)]
	answer = [(t, p) for t, p in zip(gttoken, gpos)]

	for tuple1 in attempt:
		for tuple2 in answer:
			if tuple1[0] == tuple2[0] and tuple1[1] != tuple2[1]:
				print(f"Tuple from tokenizer: {tuple1}, Ground Truth: {tuple2}")
				tokenizer_output.append(tuple1[1])
				gt_tagging.append(tuple2[1])
				line_no.append(line_number)

	
	print(gttoken)
	print(ptoken)
	print(gpos)
	print(ppos)

	# print tokenization accuracy
	correct = 0

	for tok in gttoken:
		if tok in ptoken:
			correct += 1

	correct_pos = 0
	for pos in gpos:
		if pos in ppos:
			correct_pos += 1

	tok_accuracy = correct / len(gttoken)

	# compute levenshtein distance for POS tagging
	mapped_ground_truth = [bareun_tokendict[item] for item in gpos]

	# prediction 전용 dict 사용
	if sys.argv[1] == 'bareun':
		pred_tokendict = bareun_tokendict
		print('using bareun')
	elif sys.argv[1] == 'kkma':
		pred_tokendict = kkma_tokendict
		print('using kkma')
	else:
		pred_tokendict = komoran_tokendict
		print('using komoran')

	mapped_prediction = [pred_tokendict[item] for item in ppos]
	#lev_dist = distance("".join(mapped_ground_truth), "".join(mapped_prediction))
	lev_dist = wer(" ".join(gpos), " ".join(ppos))

	print("Tokenization Accuracy : {acc:.3f}".format(acc=tok_accuracy))
	print("POS Levenshtein distance: {}".format(lev_dist))

	

	if gttoken == ptoken and true_pos["POS_Tag"].tolist() == pred_pos["POS_Tag"].tolist():
		print("Sentence {} is 100 percent correct".format(line_number))

	return tok_accuracy, lev_dist, len(gpos), correct_pos, tokenizer_output, gt_tagging, line_no, len(gttoken), correct, " ".join(gpos), " ".join(ppos)

# main method 
def main():
	# initialize csv type
	tokenizer_type = sys.argv[1]
	tokenizer_csv_path = "/Users/jinseokim/LDC_Analysis/bareun_tokenizer/" + tokenizer_type + "_output.csv"

	gt = pd.read_csv(r"/Users/jinseokim/LDC_Analysis/bareun_tokenizer/test_lines.csv")
	tokenizer = pd.read_csv(tokenizer_csv_path)

	i = 1
	lastline = max(tokenizer["Line_No"].tolist())

	toks = []
	postags = []
	postotal = []
	poscorr = []

	manual_pos_check_pred = []
	manual_pos_check_gt = []
	linenums = []
	tokens_total = []
	tokens_correct = []

	# String to compute total POS tagging levenshtein distance
	levenshtein_gt = ""
	levenshtein_pred = ""

	while i <= lastline:
		tok, pos, total, cor, poscheck_pred, poscheck_gt, linen, tk_total, tk_correct, lev_gt, lev_pred = eval_each_sentence(gt, tokenizer, i)
		toks.append(tok)
		postags.append(pos)
		postotal.append(total)
		poscorr.append(cor)

		tokens_total.append(tk_total)
		tokens_correct.append(tk_correct)

		# Bareun 외 다른 tokenizer 수정용으로만 사용
		manual_pos_check_pred += poscheck_pred
		manual_pos_check_gt += poscheck_gt
		linenums += linen
		i += 1

		# String concatenation for LD calculation
		levenshtein_gt += (" " + lev_gt)
		levenshtein_pred += (" " + lev_pred)


	# print statistics

	t_mean = statistics.mean(toks)
	t_std_dev = statistics.stdev(toks)
	p_mean = statistics.mean(postags)
	p_std_dev = statistics.stdev(postags)

	print("\n\n\nTokenization Mean: {acc:.3f}".format(acc=t_mean))
	print("Tokenization Standard Deviation: {acc:.3f}".format(acc=t_std_dev))

	print("WER Mean:{acc:.3f}".format(acc=p_mean))
	print("WER Standard Deviation:{acc:.3f}".format(acc=p_std_dev))

	# Path to the output CSV file
	csv_file_path = tokenizer_type + '_accuracy_results.csv'

	# Write data to CSV file
	with open(csv_file_path, 'w', newline='') as csv_file:
		csv_writer = csv.writer(csv_file)
		
		# Write header
		csv_writer.writerow(['Tokenization Accuracy', 'POS LevDist', 'No_POS', 'Correct_Pos', 'Total Tokens', 'Correct Tokens'])
		
		# Write data from both lists
		for token_accuracy, pos_accuracy, t, c, tkt, tkc in zip(toks, postags, postotal, poscorr, tokens_total, tokens_correct):
			csv_writer.writerow([round(token_accuracy,3), round(pos_accuracy,3), t, c, tkt, tkc])

	print("CSV file saved:", csv_file_path)

	# print LD for entire dataset
	print("\n\nTotal WER: ", wer(levenshtein_gt, levenshtein_pred))
	print("Total tokenization accuracy for 50 sentences: ", round(sum(tokens_correct) / sum(tokens_total),3))




	# ================= 타 tokenizer 전용 ========

	# 보정용 csv file path
	if 2 == 2:
		manual_correction_path = tokenizer_type + '_manual_pos_correction.csv'

		with open(manual_correction_path, 'w', newline = '') as csvfile:
			csv_writer = csv.writer(csvfile)
			csv_writer.writerow(['Sentence_No', 'Predicted POS', 'Ground Truth', 'Mark_as_correct'])

			# Write data from both lists
			for l, pr, gt in zip(linenums, manual_pos_check_pred, manual_pos_check_gt):
				csv_writer.writerow([l, pr, gt, 0])

		print("CSV file saved:", manual_correction_path)

# dictionaries
bareun_tokendict = {
	'UNK' : 'a',
	'NNG' : 'b', # 일반 명사
	'NNP' : 'c', # 고유 명사
	'NNB' : 'd', # 의존 명사
	'NP' : 'e', # 대명사
	'NR' : 'f', # 수사
	'NF' : 'g', # 명사 추정 범주
	'NA' : 'h', # 분석불능범주
	'NV' : 'i', # 용언 추정 범주
	'VV' : 'j', # 동사
	'VA' : 'k', # 형용사
	'VX' : 'l', # 보조 용언
	'VCP' : 'm', # 긍정 지정사
	'VCN' : 'n', # 부정 지정사
	'MMA' : 'p', # 성상 관형사
	'MMD' : 'p', # 지시 관형사
	'MMN' : 'q', # 수 관형사
	'MAG' : 'r', # 일반 부사
	'MAJ' : 's', # 접속 부사
	'IC' : 't', # 감탄사
	'JKS' : 'u', # 주격 조사
	'JKC' : 'v', # 보격 조사
	'JKG' : 'w', # 관형격 조사
	'JKO' : 'x', # 목적격 조사
	'JKB' : 'y', # 부사격 조사
	'JKV' : 'z', # 호격 조사
	'JKQ' : 'A', # 인용격 조사
	'JX' : 'B', # 보조사
	'JC' : 'C', # 접속 조사
	'EP' : 'D', # 선어말 어미
	'EF' : 'E', # 종결 어미
	'EC' : 'F', # 연결 어미
	'ETN' : 'G', # 명사형 전성 어미
	'ETM' : 'H', # 관형형 전성 어미
	'XPN' : 'I', # 체언 접두사
	'XSN' : 'J', # 명사 파생 접미사
	'XSV' : 'K', # 동사 파생 접미사
	'XSA' : 'L', # 형용사 파생 접미사
	'XR' : 'M', # 어근
	'SF' : 'N', # 마침표,물음표,느낌표
	'SP' : 'O', # 쉼표,가운뎃점,콜론,빗금
	'SS' : 'P', # 따옴표,괄호표,줄표
	'SE' : 'Q', # 줄임표
	'SO' : 'R', # 붙임표(물결,숨김,빠짐)
	'SW' : 'S', # 기타기호 (논리수학기호,화폐기호)
	'SL' : 'T', # 외국어
	'SH' : 'U', # 한자
	'SN' : 'V' # 숫자
}

kkma_tokendict = {
	'UNK' : 'a',
	'NNG' : 'b', # 일반 명사
	'NNP' : 'c', # 고유 명사
	'NNB' : 'd', # 의존 명사
	'NNM' : 'd',
	'NP' : 'e', # 대명사
	'NR' : 'f', # 수사
	'UN' : 'g', # 명사 추정 범주
	'NA' : 'h', # 분석불능범주
	'NV' : 'i', # 용언 추정 범주
	'VV' : 'j', # 동사
	'VA' : 'k', # 형용사
	'VXV' : 'l',
	'VXA' : 'l',
	'VX' : 'l', # 보조 용언
	'VCP' : 'm', # 긍정 지정사
	'VCN' : 'n', # 부정 지정사
	'MDT' : 'q', # 지시 관형사
	'MDN' : 'q', # 수 관형사
	'MAG' : 'r', # 일반 부사
	'MAC' : 's', # 접속 부사
	'IC' : 't', # 감탄사
	'JKS' : 'u', # 주격 조사
	'JKC' : 'v', # 보격 조사
	'JKG' : 'w', # 관형격 조사
	'JKO' : 'x', # 목적격 조사
	'JKM' : 'y', # 부사격 조사
	'JKI' : 'z', # 호격 조사
	'JKQ' : 'A', # 인용격 조사
	'JX' : 'B', # 보조사
	'JC' : 'C', # 접속 조사
	'EPH' : 'D',
	'EPT' : 'D',
	'EPP' : 'D', # 선어말 어미
	'EFN' : 'E',
	'EFQ' : 'E',
	'EFO' : 'E',
	'EFA' : 'E',
	'EFI' : 'E',
	'EFR' : 'E',
	'EF' : 'E', # 종결 어미
	'ECE' : 'F', # 연결 어미
	'ECS' : 'F', # 연결 어미
	'ECD' : 'F', # 연결 어미
	'EC' : 'F', # 연결 어미
	'ETN' : 'G', # 명사형 전성 어미
	'ETD' : 'H', # 관형형 전성 어미
	'XPN' : 'I', # 체언 접두사
	'XPV' : 'I', # 체언 접두사
	'XSN' : 'J', # 명사 파생 접미사
	'XSV' : 'K', # 동사 파생 접미사
	'XSA' : 'L', # 형용사 파생 접미사
	'XR' : 'M', # 어근
	'SF' : 'N', # 마침표,물음표,느낌표
	'SP' : 'O', # 쉼표,가운뎃점,콜론,빗금
	'SS' : 'P', # 따옴표,괄호표,줄표
	'SE' : 'Q', # 줄임표
	'SO' : 'R', # 붙임표(물결,숨김,빠짐)
	'SW' : 'S', # 기타기호 (논리수학기호,화폐기호)
	'OL' : 'T', # 외국어
	'OH' : 'U', # 한자
	'ON' : 'V' # 숫자
}

komoran_tokendict = {
	'NA' : 'a',
	'NNG' : 'b', # 일반 명사
	'NNP' : 'c', # 고유 명사
	'NNB' : 'd', # 의존 명사
	'NNM' : 'd',
	'NP' : 'e', # 대명사
	'NR' : 'f', # 수사
	'NF' : 'g', # 명사 추정 범주
	'NA' : 'h', # 분석불능범주
	'NV' : 'i', # 용언 추정 범주
	'VV' : 'j', # 동사
	'VA' : 'k', # 형용사
	'VXV' : 'l',
	'VXA' : 'l',
	'VX' : 'l', # 보조 용언
	'VCP' : 'm', # 긍정 지정사
	'VCN' : 'n', # 부정 지정사
	'MDT' : 'p', # 지시 관형사
	'MM' : 'q', # 수 관형사
	'MAG' : 'r', # 일반 부사
	'MAJ' : 's', # 접속 부사
	'IC' : 't', # 감탄사
	'JKS' : 'u', # 주격 조사
	'JKC' : 'v', # 보격 조사
	'JKG' : 'w', # 관형격 조사
	'JKO' : 'x', # 목적격 조사
	'JKB' : 'y', # 부사격 조사
	'JKV' : 'z', # 호격 조사
	'JKQ' : 'A', # 인용격 조사
	'JX' : 'B', # 보조사
	'JC' : 'C', # 접속 조사
	'EPH' : 'D',
	'EPT' : 'D',
	'EP' : 'D', # 선어말 어미
	'EFN' : 'E',
	'EFQ' : 'E',
	'EFO' : 'E',
	'EFA' : 'E',
	'EFI' : 'E',
	'EFR' : 'E',
	'EF' : 'E', # 종결 어미
	'ECE' : 'F', # 연결 어미
	'ECS' : 'F', # 연결 어미
	'ECD' : 'F', # 연결 어미
	'EC' : 'F', # 연결 어미
	'ETN' : 'G', # 명사형 전성 어미
	'ETM' : 'H', # 관형형 전성 어미
	'XPN' : 'I', # 체언 접두사
	'XPV' : 'I', # 체언 접두사
	'XSN' : 'J', # 명사 파생 접미사
	'XSV' : 'K', # 동사 파생 접미사
	'XSA' : 'L', # 형용사 파생 접미사
	'XR' : 'M', # 어근
	'SF' : 'N', # 마침표,물음표,느낌표
	'SP' : 'O', # 쉼표,가운뎃점,콜론,빗금
	'SS' : 'P', # 따옴표,괄호표,줄표
	'SE' : 'Q', # 줄임표
	'SO' : 'R', # 붙임표(물결,숨김,빠짐)
	'SW' : 'S', # 기타기호 (논리수학기호,화폐기호)
	'OL' : 'T', # 외국어
	'OH' : 'U', # 한자
	'ON' : 'V' # 숫자
}


if __name__ == "__main__":
	main()


