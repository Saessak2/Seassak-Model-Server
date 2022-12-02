import pickle
import json
import pandas as pd
from hanspell import spell_checker
import re
from konlpy.tag import Komoran

class FileHandler():

    def save_file(filepath, data):
        with open(filepath, 'wb') as lf:
            pickle.dump(data, lf)

    def load_file(filepath):
        with open(filepath, 'rb') as lf:
            data = pickle.load(lf)
            print('데이터 개수 :', len(data))
        return data

    def save_json(filepath, data):
        with open(filepath, 'w', encoding='UTF-8') as jf:
            json.dump(data, jf, indent=2, ensure_ascii=False)

        
    def load_json_to_df(filepath):
        data = open(filepath, encoding='utf-8')
        data = pd.DataFrame(json.load(data))
        return data

    def load_json_to_list(filepath):
        data = open(filepath, encoding='utf-8')
        data = list(json.load(data))
        print('데이터 개수 :', len(data))
        return data


class Preprocessor():
    
    # 불용어 제거 - 1
    def remove_stopword(texts):
        results = []
        for text in texts:
            text = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z.\s]",' ', text) # 한글음절, 영어, 숫자, 띄어쓰기 뺴고 다 제거
            text = re.sub('[.]{2,}', '.', text) # 온점 2개 이상 1개로 대체
            text = re.sub('[ ]{2,}', ' ', text) # 공백 2개 이상 1개로 대체
            text = re.sub("[\t]",' ', text) 

            results.append(text)

        return results
    
    def check_spell(texts) :
        results = [] 
        cnt = 0

        for x in texts:

            try :
                cnt+=1
                spell_dict = spell_checker.check(x).as_dict()
                results.append(spell_dict['checked'])

            except:
                print('except no : ', cnt)
                results.append(x) 

        return results
    
    def komoran_analyzer(texts):
        komoran = Komoran(userdic='./data/plantnames.txt')
        results = []
        for text in texts:
            analyzed = komoran.morphs(text)
            result_str = ''
            for x in analyzed:
                result_str += (x + ' ')
            results.append(result_str.strip())

        return results

