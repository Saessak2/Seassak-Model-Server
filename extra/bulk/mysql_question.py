# mysql question db에 지식인 데이터 넣기 - create_time 넣어서 돌려야 함

import pymysql.cursors
import json

# 접속
# 비밀번호가 포함되어 있기 때문에 보통 config파일에서 key값으로 부른다.
conn = pymysql.connect(
    host = "34.64.194.141", 	 #ex) '127.0.0.1'
    port=3306,
    user = "saessacki", 		 #ex) root
    password = "1234",
    database = "saessac",
	charset = 'utf8'
)


# Cursor Object 가져오기
curs = conn.cursor()

try:
    with open('/Users/eunbin/Desktop/Projects/saessack-server/extra/data/crawling_data/mysql_question.json', encoding='utf-8') as jf:
        json_list = list(json.load(jf))

    for data in json_list:
        user_id = data['user_id']
        user_name = '윤겸지'
        category = data['category']
        content = data['content']
        answer_count = data['answer_count']
        create_time = '22/12/02 07:21'

        sql = 'INSERT INTO question(content, answer_count, category, user_id, create_date, user_name) VALUES (%s, %s, %s, %s, %s, %s)'
        val = (content, answer_count, category, user_id, create_time, user_name)

        curs.execute(sql, val)
        conn.commit()

finally:
    conn.close()

print(curs.rowcount, "record inserted")

