from django.core.management.base import BaseCommand

import json
import re
from hanspell import spell_checker
from konlpy.tag import Komoran
import pandas as pd
import pickle

import tensorflow.compat.v1 as tf
import tensorflow_hub as hub

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class Command(BaseCommand):

    def handle(self, *args, **options):
        KinNaver.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Started database population process...'))

        file_path = '/Users/eunbin/Desktop/Projects/saessack/data/docs/dataset.json'
        dataset = open(file_path, encoding='utf-8')
        dataset = list(json.load(dataset))

        for data in dataset:
            title = data['title'],
            content = data['content'],
            answers = ''
            for x in data['answers']:
                answers += (x + '. ')

            docs = title + '. ' + content + '. ' + answers
            docs = docs.strip()


            kinplant = KinNaver.objects.create(
                link = data['link'],
                title = data['title'],
                content = data['content'], 
                answer = answers,
                vector = sent_vector,
            )
            kinplant.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database.'))

    def sentence_to_vector(self, sentence):
        sentence = self.preprocessing(sentence)



    def preprocessing(self, sentence):
        # 불용어 제거
        sentence = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z.\s]",' ', sentence) # 한글음절, 영어, 숫자, 띄어쓰기 뺴고 다 제거
        sentence = re.sub('[.]{2,}', '.', sentence) # 온점 2개 이상 1개로 대체
        sentence = re.sub('[ ]{2,}', ' ', sentence) # 공백 2개 이상 1개로 대체
        sentence = re.sub("[\t]",' ', sentence) 

        # 맞춤법 수정
        spelled_dict = spell_checker.check(sentence).as_dict()
        sentence = spelled_dict['checked']

        # 태그 리스트 가져오기
        tag_path = '/Users/eunbin/Desktop/Projects/saessack/data/tag/'
        plt_tags = pd.read_csv(tag_path+'PLANT.csv', encoding='utf-8')
        plt_tags = list(set(plt_tags['PLT']))
        bug_tags = pd.read_csv(tag_path+'BUG.csv', encoding='utf-8')
        bug_tags = list(set(plt_tags['BUG']))
        dis_tags = pd.read_csv(tag_path+'DISEASE.csv', encoding='utf-8')
        dis_tags = list(set(plt_tags['DIS']))
        ctg_tags = pd.read_csv(tag_path+'CATEGORY.csv', encoding='utf-8')
        ctg_tags = list(set(plt_tags['CTG']))
        tags = plt_tags + bug_tags + dis_tags + dis_tags
        
        with open('.../static/tags.txt', 'wb') as lf:
            pickle.dump(tags, lf)

        # 형태소 분석
        komoran = Komoran(userdic='.../static/tags.txt')
        analyzed = komoran.morphs(sentence)

        return analyzed


    def embedding(self, sentence):
