import re
from konlpy.tag import Komoran


komoran = Komoran(userdic='/Users/eunbin/Desktop/Projects/saessack-server/extra/data/userdic2.txt')
print("=====================> komoran module created")

def komoran_analyzer(texts):
    results = []
    for text in texts:
        tagging = komoran.pos(text)
        temp = []
        for item in tagging:
            if item[1]=='NNG' or item[1]=='NNP'or item[1]=='VV' or item[1]=='VA'or item[1]=='MM' or item[1]=='XR':
                temp.append(item[0])
        results.append(temp)

    return results

def remove_stopwords(texts):
    result = []
    for text in texts:
        text = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z.\s]",' ', text) # 한글음절, 영어, 숫자, 띄어쓰기 뺴고 다 제거
        text = re.sub('[.]{2,}', '.', text) # 온점 2개 이상 1개로 대체
        text = re.sub('[ ]{2,}', ' ', text) # 공백 2개 이상 1개로 대체
        text = re.sub("[\t]",' ', text) 
        result.append(text)
    return result