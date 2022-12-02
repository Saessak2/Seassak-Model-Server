import requests, json
from elasticsearch import Elasticsearch, helpers
from sentence_transformers import SentenceTransformer, models
from ko_sentence_transformers.models import KoBertTransformer
import re

INDEX_NAME = "kinnaver"

# res = requests.get('http://localhost:9200')
es = Elasticsearch([{'host':'localhost','port':'9200'}])

es.indices.delete(index=INDEX_NAME, ignore=[404])

es.indices.create(
    index= INDEX_NAME,
    body={
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1,
            "index": {
                "analysis": {
                    "analyzer": {
                        "my_analyzer": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer",
                            "filter": ["lowercase", "stop"]
                        }
                    }
                }
            }
        },
         # Elasticsearch의 인덱스에 들어가는 데이터의 타입을 정의 
        "mappings": {
            "_source": {
                "enabled": "true"
            },
            "properties": {
                "knid": {
                    "type": "long"
                },
                "link": {
                    "type": "keyword"
                },
                "title": {
                    "type": "keyword"
                },
                "content": {
                    "type": "keyword"
                },
                # "answer": {
                #     "type": "text"
                # },
                "sentence": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                },
                "sentence_vector": {
                    "type": "dense_vector",
                    "dims": 768,
                    # "index": True,
                    # "similarity": "cosine"
                },
            }   
        }
    }
)

# 여러 개의 데이터를 한 번에 bulk하기 위해서 데이터를 Elasticsearch 형식에 맞게 정제
fileapath = '/Users/eunbin/Desktop/Projects/saessack-server/extra/data/kinnaver/'
with open(fileapath+'dataset.json', encoding='utf-8') as json_file:
    json_data = json.loads(json_file.read())
# json_data = json_data[:20]

##### EMBEDDING MODEL #####
# word_embedding_model = KoBertTransformer("monologg/kobert", max_seq_length=512)
word_embedding_model = KoBertTransformer("monologg/kobert")
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(), pooling_mode='mean')
embedder = SentenceTransformer(modules=[word_embedding_model, pooling_model])


docs = []
count = -1
for data in json_data:
    count += 1
    answer = ''
    for ans in data['answers']:
        answer += ans + '. '
    sentence = data['title'] + '. ' + data['content'] + '. ' + answer

    # 불용어 제거
    sentence = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z.\s]",' ', sentence) # 한글음절, 영어, 숫자, 띄어쓰기 뺴고 다 제거
    sentence = re.sub('[.]{2,}', '.', sentence) # 온점 2개 이상 1개로 대체
    sentence = re.sub('[ ]{2,}', ' ', sentence) # 공백 2개 이상 1개로 대체
    sentence = re.sub("[\t]",' ', sentence) 
    embeddings = embedder.encode(sentence, convert_to_tensor=False)
    
    # 카테고리 추가
    docs.append({
        "_index": INDEX_NAME,
        "_id": count,
        '_source': {
            "knid": count,
            "link": data['link'],
            "title": data['title'],
            "content": data['content'],
            # "answer" : answer,
            "sentence" : sentence,
            "sentence_vector" : embeddings
        }
    })

helpers.bulk(es, docs)