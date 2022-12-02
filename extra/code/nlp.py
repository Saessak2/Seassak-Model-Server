import pickle
import numpy as pd
import pandas as pd
import json
from hanspell import spell_checker
from konlpy.tag import Komoran
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Prepocessing():
    def preprocess(texts):
        texts = Prepocessing.remove_stopword(texts)
        print(texts)
        texts = Prepocessing.check_spell(texts)
        print(texts)
        texts = Prepocessing.komoran_analyzer(texts)
        print(texts)
        return texts

    def remove_stopword(texts):
        results = []
        for text in texts:
            text = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]",' ', text) # 한글음절, 영어, 숫자, 띄어쓰기 뺴고 다 제거
            # text = re.sub('[.]{2,}', '.', text) # 온점 2개 이상 1개로 대체
            text = re.sub('[ ]{2,}', ' ', text) # 공백 2개 이상 1개로 대체
            text = re.sub("[\t]",' ', text) 
            
            if text[-1] == ' ': 
                text = text[:-1]
                
            results.append(text)
            
        return results

    def check_spell(text) :
        
        try :
            cnt+=1
            spell_dict = spell_checker.check(text).as_dict()
            return spell_dict(['checked'])
        except :
            print('except no : ', cnt)


    def komoran_analyzer(texts):
        komoran = Komoran()
        results = []
        for text in texts:
            analyzed = komoran.morphs(text)
            result_str = ''
            for x in analyzed:
                result_str += (x + ' ')
            results.append(result_str.strip())
            
        return results

class Embedding():
    def vectorize(document):
        tfidfv = TfidfVectorizer().fit(document)
        tfidf_matrix = tfidfv.transform(document)
        print('TF-IDF 행렬의 크기(shape) :',tfidf_matrix.shape)
        tfidf_matrix = tfidf_matrix.todense()

        return tfidfv, tfidf_matrix

class CosineSimilarity():

    def get_similar_questions(user_question, tfidf_matrix, tfidfv, questions):
        user_question = Prepocessing.preprocess(user_question)
        userv = tfidfv.transform(user_question).todense()

        cosine_sim = cosine_similarity(tfidf_matrix, userv)
        print('코사인 유사도 연산 결과 :',cosine_sim.shape)
        
        sim_scores = list(enumerate(cosine_sim))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                        
        sim_scores = sim_scores[0:2]

        results = []
        for x in sim_scores:
            dic = {}
            dic['text'] = questions[x[0]]
            dic['similarity'] = x[1][0]
            results.append(dic)
                
        return results

