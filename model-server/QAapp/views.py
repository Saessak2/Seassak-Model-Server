from rest_framework import viewsets, status
from rest_framework.views import APIView  
from rest_framework.response import Response
from rest_framework.decorators import api_view
from elasticsearch import Elasticsearch
import time
from crawler2 import Crawler
import logging
import bm25
import preprocessor
import datetime


es = Elasticsearch([{'host':'localhost','port':'9200'}])
dt_now = datetime.datetime.now()

# 검색 field에 (^) notation을 추가하면 해당 field 검색이 boost(relevance score 계산시 우대를 받게 됨)를 얻게 됩니다. notation이 있을 때와 없을 때 score를 비교해보면 바로 알수 있을것입니다


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
                        "link", "title", "knid"
                    ]
                }
            )

    hit = response['hits']['hits'][0]
    response = {
        'knid': hit.get('_source')['knid'],
        'title': hit.get('_source')['title'],
        'link': hit.get('_source')['link']
    }
    return response


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
    
    flag = 0
    print('flag => ', flag)

    def post(self, request):
        
        if self.flag == 1:
            print("한번만 해라...")
            return Response() 

        self.flag = 1
        print("#################################### connnected #######################################")  

        self.logger.info(get_client_ip(request))

        # now = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        # if self.request_time == now:
        #     return Response(status=status.HTTP_200_OK)
        # self.request_time = now

        # print(now)

        search_start = time.time()

        request_data = request.data
        question = request_data['question']
        category = request_data['category']
        print("question => " + question +", category => "+category)

        # TODO  개체명 인식 -> 태그 꺼내기 {'PLT': [], 'CTG': [], 'BUG' : [], 'DIS' : []}

        ####################### 질문 전처리 및 임베딩 #########################

        # 불용어 제거 & 형태소 분석
        removed = preprocessor.remove_stopwords([question])
        analyzed = preprocessor.komoran_analyzer(removed)
        
        # doc_scores = bm25.get_scores(analyzed[0])
        # print(doc_scores)

        top_indexs = bm25.getTopN(analyzed[0], n=10)
        print(top_indexs)

        ################ index로 문서 조회  ################

        for index in top_indexs:
            search_response = search_auto_comment(index)  # knid, title, link 받아옴

            ################### 댓글 크롤링 ######################
            answer = Crawler.get_answer(search_response['link'])
            if answer != None:
                result = {
                    # 'knid': search_response['knid'],
                    'title': search_response['title'],
                    'link': search_response['link'],
                    'answer': answer
                }
                break # 댓글 있는거 찾으면 바로 완료
                
        search_time = "총 시간 => " + str(time.time() - search_start)
        print(search_time)

        self.flag = 0
        return Response([result], status=status.HTTP_200_OK)

























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