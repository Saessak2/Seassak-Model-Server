from rank_bm25 import BM25Okapi
import pickle
import preprocessor


with open('/Users/eunbin/Desktop/Projects/saessack-server/extra/data/kinnaver/dataset.txt', 'rb') as lf:
    docs = pickle.load(lf)

docs = docs[:100]

print('데이터 개수   :', len(docs))

indexs = [i for i in range(len(docs))] # 문서가 아닌 인덱스를 가져오기 위해 인덱스 배열 저장

# 불용어 제거
removed = preprocessor.remove_stopwords(docs)
# 형태소 분석
analyzed = preprocessor.komoran_analyzer(removed)
# bm25
bm25 = BM25Okapi(analyzed)
print("=========================> bm25 module created")


def getTopN(tokenized_query, n=1):
    return bm25.get_top_n(tokenized_query, indexs, n)

def get_scores(query):
    return bm25.get_scores(query)


