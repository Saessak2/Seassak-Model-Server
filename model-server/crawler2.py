from bs4 import BeautifulSoup
import requests
import re

class Crawler():

    def get_answer(link):
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
        result = ''
        for i in range(1, answer_num+1):

            try:
                selector = '#answer_'+str(i)+' div.se-main-container div.se-text p'
                find_all = soup.select(selector)
            except Exception:
                try:
                    find_all = soup.select_one('#answer_'+str(i)+" > div._endContents").find("div",{"class": "_endContentsText"}).find_all(text=True)
                except:
                    continue

            answer = ''
            for x in find_all:
                x = re.sub(r"\s+", " ", x.text)
                if x != '\u200b' and 'http' not in x:
                    answer += (x + ' ')

            answer = answer.strip()
            result += (answer+ '. ')

        return result

        
                    

# answer = Crawler.get_answer('https://kin.naver.com/qna/detail.naver?d1id=8&dirId=80604&docId=431969367&qb=7Iud66y8&enc=utf8&section=kin&rank=1&search_sort=0&spq=0')
# print(answer)