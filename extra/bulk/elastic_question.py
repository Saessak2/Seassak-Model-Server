import requests, json
from elasticsearch import Elasticsearch

INDEX_NAME = "mysql_question"

res = requests.get('http://localhost:9200')
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
                            "filter": ["lowercase", "my_synonym"]
                        }
                    },
                    "filter": {
                        "my_synonym": {
                            "type": "synonym",
                            "synonyms_path": "analysis/synonym.txt"
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
                "question_id": {
                    "type": "long"
                },
                "user_id": {
                    "type": "long"
                },
                 "user_name": {
                    "type": "keyword"
                },
                "category": {
                    "type": "keyword",
                },
                "content": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                },
                "create_date": {
                    "type": "date",
                    "format": "YY/M/D HH:mm"
                },
                "answer_count": {
                    "type": "byte"
                }
            }   
        }
    }
)