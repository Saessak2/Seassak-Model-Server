import json
from elasticsearch import Elasticsearch, helpers
import re

INDEX_NAME = "kinnaver"

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
                }
            }   
        }
    }
)

# 여러 개의 데이터를 한 번에 bulk하기 위해서 데이터를 Elasticsearch 형식에 맞게 정제
fileapath = '/Users/eunbin/Desktop/Projects/saessack-server/extra/data/kinnaver/'
with open(fileapath+'dataset.json', encoding='utf-8') as json_file:
    json_data = json.loads(json_file.read())


docs = []
count = -1
for data in json_data:
    count += 1

    title = data['title']

    # 제목만 불용어 제거
    title = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z.\s]",' ', title) # 한글음절, 영어, 숫자, 띄어쓰기 뺴고 다 제거
    title = re.sub('[.]{2,}', '.', title) # 온점 2개 이상 1개로 대체
    title = re.sub('[ ]{2,}', ' ', title) # 공백 2개 이상 1개로 대체
    title = re.sub("[\t]",' ', title) 
    
    # 카테고리 추가
    docs.append({
        "_index": INDEX_NAME,
        "_id": count,
        '_source': {
            "knid": count,
            "link": data['link'],
            "title": title,
            "content": data['content']
        }
    })

helpers.bulk(es, docs)