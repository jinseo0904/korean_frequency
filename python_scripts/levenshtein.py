from Levenshtein import distance

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
    'MMA' : 'o', # 성상 관형사
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


list1 = ['VA', 'EC', 'VX', 'ETM', 'NNB', 'JX', 'VV', 'EF']
list2 = ['VA', 'EC', 'VX', 'ETM', 'NNB', 'VCP', 'EF', 'VV', 'EF']

list1_mapped = [bareun_tokendict[item] for item in list1]
list2_mapped = [bareun_tokendict[item] for item in list2]

print(list1_mapped)
print(list2_mapped)

levenshtein_distance = distance("".join(list1_mapped), "".join(list2_mapped))
print("Levenshtein distance:", levenshtein_distance)

