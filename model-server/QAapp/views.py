from rest_framework import viewsets, status
from rest_framework.views import APIView  
from rest_framework.response import Response
from rest_framework.decorators import api_view
from elasticsearch import Elasticsearch , helpers
import re
import time
from embedder import Embedder
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from hanspell import spell_checker
from konlpy.tag import Komoran
from crawler2 import Crawler
import logging

es = Elasticsearch([{'host':'localhost','port':'9200'}])


# 검색 field에 (^) notation을 추가하면 해당 field 검색이 boost(relevance score 계산시 우대를 받게 됨)를 얻게 됩니다. notation이 있을 때와 없을 때 score를 비교해보면 바로 알수 있을것입니다

# 자동 답변 
# qa/comment/auto
class AutoCommentAPI(APIView):
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s || %(name)s || %(levelname)s || %(message)s')
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    INDEX_NAME = 'kinnaver'

    before_request = ''

    def post(self, request):
        print("#################################### connnected #######################################")  
        
        # client_ip = get_client_ip(request)

        self.logger.info(get_client_ip(request))

        request_data = request.data
        question = request_data['question']
        category = request_data['category']
        print("query => " + question +", category => "+category)

        # TODO  개체명 인식 -> 태그 꺼내기 {'PLT': [], 'CTG': [], 'BUG' : [], 'DIS' : []}

        es = Elasticsearch([{'host':'localhost','port':'9200'}])

        ####################### 질문 임베딩 #########################
        user_matrix = np.array([embedding(remove_stopword(question))])

        search_start = time.time()

        # TODO : 모든 vector랑 조회하지 말고 그 전에 거르기 <- 모든 vector 조회하니까 시간 너무 오래걸림
        # TODO : 위에 태그 꺼낸걸로 elastic 검색해서 스코어 높은거 size 100개? 정도 꺼내기
        ################ 모든 sentence_vector 조회 XxXXX ################
        # try :
        response = es.search(
            index = self.INDEX_NAME,
            body= {
                "track_total_hits": True,
                "_source": [
                    "sentence_vector", "knid"
                ],
                "query": {"match_all": {}},
                "size": 10000,
                "sort": [{
                    "knid": {"order": "asc"}
                }]
            }
        )

        search_time = "총 시간 => " + str(time.time() - search_start)

        cnt = str(response['hits']['total']['value'])
        print("search 개수 -> " + cnt)

        sources = []
        matrix = []
        for data in response['hits']['hits']:
            source = {}
            source['knid'] = data.get('_source')['knid']
            source['sentence_vector'] = data.get('_source')['sentence_vector']
            matrix.append(source['sentence_vector'])
            sources.append(source)
        matrix = np.array(matrix)
        
        ################## cosine similarity ###################

        sim_list = get_similar_list(matrix, user_matrix)  # -> id 오름차순 
        sim_list = sorted(sim_list, key=lambda x: x['score'], reverse=True) # 유사도 순 정렬
        # sim_list = sim_list[:10]
        # print(sim_list)

        ################ 유사한거 뽑은 id로 조회 ##################
        for item in sim_list:
            print("start crawling >> id -> " + str(item['id'])) 
            search_response = search_auto_comment(str(item['id']))  # knid, title, link 받아옴

            ################### 댓글 크롤링 ######################
            answer = Crawler.get_answer(search_response['link'])
            if answer != None:
                result = {
                    # 'id': item['id'],
                    'similarity': str(round(item['score'] * 100)) + "%",
                    # 'knid': search_response['knid'],
                    'title': search_response['title'],
                    'link': search_response['link'],
                    'answer': answer
                    # 'sentence': search_response['sentence']
                }
                break # 댓글 있는거 찾으면 바로 완료
                
            
        print(search_time)

        return Response([result], status=status.HTTP_200_OK)

def search_auto_comment(id):
    response = es.search(
                index = 'kinnaver',
                body={
                    "query": {
                        "term": {
                            "_id": id
                        }
                    },
                    "_source": [
                        "link", "title", "knid", "sentence"
                    ]
                }
            )

    hit = response['hits']['hits'][0]
    response = {
        'knid': hit.get('_source')['knid'],
        'title': hit.get('_source')['title'],
        'link': hit.get('_source')['link'],
        'sentence': hit.get('_source')['sentence']

    }
    return response

def get_similar_list(matrix, user_matrix):
    cosine_sim = cosine_similarity(matrix, user_matrix)
    print('코사인 유사도 연산 결과 :',cosine_sim.shape)
    

    sim_list = [] 
    cnt = -1
    for x in cosine_sim:
        cnt += 1 
        item = {}
        item['id'] = cnt
        item['score'] = x[0]
        sim_list.append(item)

    return sim_list         



def remove_stopword(text):
    # 불용어 제거
    text = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z.\s]",' ', text) # 한글음절, 영어, 숫자, 띄어쓰기 뺴고 다 제거
    text = re.sub('[.]{2,}', '.', text) # 온점 2개 이상 1개로 대체
    text = re.sub('[ ]{2,}', ' ', text) # 공백 2개 이상 1개로 대체
    text = re.sub("[\t]",' ', text) 
    return text


def embedding(text):
    # 임베딩
    embedding_start = time.time()
    text_vector = Embedder.embedder.encode(text, convert_to_tensor=False).tolist()
    embedding_time = time.time() - embedding_start
    print("embedding time: {:.2f} ms".format(embedding_time * 1000))
    return text_vector




















# 질문 검색
# qa/question/search/
class QuestionSearch(APIView):
    INDEX_NAME = 'mysql_question'
    
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s || %(name)s || %(levelname)s || %(message)s')
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


    def post(self, request):
        print("#################### connnected #####################")    
        self.logger.info(get_client_ip(request))
    
        category = request.data['category']
        search_query = request.data['content']
        
        es = Elasticsearch([{'host':'localhost','port':'9200'}])
        
        if len(search_query) > 0 : # 검색어 있는 경우
            response = es.search(
                index = self.INDEX_NAME,
                body ={
                    "query": {
                        "bool": {
                            "filter": [{
                                "term": {
                                    "category": category
                                }
                            }],
                        "must": [
                            {
                            "match": {
                                "content": {
                                "analyzer": "my_analyzer",
                                "query": search_query
                                }
                            }
                            }
                        ]
                        }
                    },
                    "_source": ["question_id", "user_name", "category", "content", "create_date", "answer_count", "user_id"],
                    "sort": [{
                        "_score": {"order": "desc"}
                    }]
                }
            )
        else: # 검색어 없는 경우
            response = es.search(
                index = self.INDEX_NAME,
                body ={
                    "query": {
                        "bool": {
                            "filter": [{
                                "term": {
                                    "category": category
                                }
                            }]
                        }
                    },
                    "_source": ["question_id", "user_name", "category", "content", "create_date", "answer_count", "user_id"],
                     "sort": [{
                        "_score": {"order": "desc"}
                    }]
                }
            )

        result = []
        for res in response['hits']['hits']:
            source = res.get('_source')
            res_item = {}
            res_item['id'] = source['question_id']
            res_item['user_id'] = source['user_id']
            res_item['userName'] = source['user_name']
            res_item['category'] = source['category']
            res_item['content'] = source['content']
            res_item['commentCnt'] = source['answer_count']
            res_item['dateTime'] = source['create_date']
            res_item['img'] = 0
            # res_item['_score'] = res.get('_score')
            result.append(res_item)

        # result = sorted(result, key=lambda data: (data['_score'], data['dateTime'], data['commentCnt']), reverse=True) 
        
        return Response(result, status=status.HTTP_200_OK)





# 지식인 데이터 전체 조회
# qa/kinnaver/all/
@api_view(['GET'])
def kinnaver_all(request):
    INDEX_NAME = 'kinnaver'

    if request.method == 'GET':
        es = Elasticsearch([{'host':'localhost','port':'9200'}])
        query = {
            "query": {"match_all": {}}
        }
        response = es.search(
            index = INDEX_NAME,
            body ={
                "track_total_hits": True,
                "query": {
                    "match_all": {}
                }
            }
        )
        return Response(response, status=status.HTTP_200_OK)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip