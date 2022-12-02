from bs4 import BeautifulSoup
import requests
import re

class Crawler():
    def __init__(self):
        rank = ['하수','평민',"시민",'초수',"중수","고수",'영웅','지존','초인','식물신','바람신','물신','달신','별신','테양신','은하신','우주신','수호신','절대신']

    def get_answer(self, link):
        ######## 댓글 개수 크롤링 ########
        try:
            soup = BeautifulSoup(requests.get(link).text, 'html.parser')
            answer_num = int(soup.find("em", {"class": "_answerCount"}).find(text=True))
        except:
            answer_num = 0
        print("answer_num => ", answer_num)
        if answer_num == 0:
            return None

        ######## 댓글 크롤링 #########
        answers = []

        ranks = []
        for i in range(1, answer_num+1):
            print('{}번째 -------------'.format(i))
                
            adoptCheck = soup.select('div.answer-content__list div.adoptCheck') # 채택 
            if len(adoptCheck) > 0:
                try:
                    answer = answer.select('#answer_'+str(i)+' div.se-main-container div.se-text p')
                except Exception:
                    answer = soup.select_one('#answer_'+str(i)+" > div._endContents").find("div",{"class": "_endContentsText"}).find_all(text=True)
                return answer

            else:
                try:
                    ranks.append({'str(i)' : self.rank.index(answer.select('div.badge'))})
                except:
                    continue
        
                    
        ranks = sorted(ranks, key=lambda x: x[''])

        #     ans_item = ''
        #     for text in answer:
        #         text = re.sub(r"\s+", " ", text.text)
        #         if text != '\u200b' and 'http' not in text:
        #             ans_item += (text + ' ')
                
        #     answers.append(ans_item.strip())
            
        #     answer = ''
        #     for x in answers :
        #         if x == '':
        #             continue
        #         else:
        #             answer += x
        #             break

        # return answer

crawler = Crawler()
crawler.get_answer('https://kin.naver.com/qna/detail.naver?d1id=8&dirId=80604&docId=431969367&qb=7Iud66y8&enc=utf8&section=kin&rank=1&search_sort=0&spq=0')