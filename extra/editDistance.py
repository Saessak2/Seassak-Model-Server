# 여기서 편집거리 코드 전까진 언니가 저장해놔야 할거 (검색할때마다 실행되면 안되고 앱 실행할떄 한번만 실행되도록 해야함)
phoneme = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ',
         'ㄲ', 'ㄸ', 'ㅃ', 'ㅆ', 'ㅉ',
        'ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ', 
        'ㄳ', 'ㄵ', 'ㄶ', 'ㄺ', 'ㄻ', 'ㄼ,' 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅄ'
        ]

ja = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㄲ', 'ㄸ', 'ㅃ', 'ㅆ', 'ㅉ']
mo = ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ']
bat = ['ㄳ', 'ㄵ', 'ㄶ', 'ㄺ', 'ㄻ', 'ㄼ,' 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅄ'] # 겹받침

print(len(phoneme))

cost_matrix = []
for i in range(len(phoneme)):
    row = []
    for j in range(len(phoneme)):
        row.append(1) 
    cost_matrix.append(row)

# 같은 글자
for i in range(len(phoneme)):
    cost_matrix[i][i] = -1
# print(cost_matrix)


# 비슷한 글자는 cost를 조금 뺌
a = -0.2
b = -0.4

# ㄱ,ㄲ,ㅋ
cost_matrix[phoneme.index('ㄱ')][phoneme.index('ㅋ')] = a
cost_matrix[phoneme.index('ㅋ')][phoneme.index('ㄱ')] = a
cost_matrix[phoneme.index('ㄱ')][phoneme.index('ㄲ')] = a
cost_matrix[phoneme.index('ㄲ')][phoneme.index('ㄱ')] = a
cost_matrix[phoneme.index('ㄲ')][phoneme.index('ㅋ')] = a
cost_matrix[phoneme.index('ㅋ')][phoneme.index('ㄲ')] = a


# ㅂ, ㅍ, ㅃ
cost_matrix[phoneme.index('ㅂ')][phoneme.index('ㅍ')] = a
cost_matrix[phoneme.index('ㅍ')][phoneme.index('ㅂ')] = a
cost_matrix[phoneme.index('ㅂ')][phoneme.index('ㅃ')] = a
cost_matrix[phoneme.index('ㅃ')][phoneme.index('ㅂ')] = a
cost_matrix[phoneme.index('ㅍ')][phoneme.index('ㅃ')] = a
cost_matrix[phoneme.index('ㅃ')][phoneme.index('ㅍ')] = a

# ㅅ, ㅆ
cost_matrix[phoneme.index('ㅅ')][phoneme.index('ㅆ')] = a
cost_matrix[phoneme.index('ㅆ')][phoneme.index('ㅅ')] = a

# ㅈ,ㅉ,ㅊ
cost_matrix[phoneme.index('ㅈ')][phoneme.index('ㅉ')] = a
cost_matrix[phoneme.index('ㅉ')][phoneme.index('ㅈ')] = a
cost_matrix[phoneme.index('ㅈ')][phoneme.index('ㅊ')] = a
cost_matrix[phoneme.index('ㅊ')][phoneme.index('ㅈ')] = a
cost_matrix[phoneme.index('ㅉ')][phoneme.index('ㅊ')] = a
cost_matrix[phoneme.index('ㅊ')][phoneme.index('ㅉ')] = a

# ㄷ,ㄸ,ㅌ
cost_matrix[phoneme.index('ㄷ')][phoneme.index('ㄸ')] = a
cost_matrix[phoneme.index('ㄸ')][phoneme.index('ㄷ')] = a
cost_matrix[phoneme.index('ㄷ')][phoneme.index('ㅌ')] = a
cost_matrix[phoneme.index('ㅌ')][phoneme.index('ㄷ')] = a
cost_matrix[phoneme.index('ㄸ')][phoneme.index('ㅌ')] = a
cost_matrix[phoneme.index('ㅌ')][phoneme.index('ㄸ')] = a

# ㅏ, ㅐ 
cost_matrix[phoneme.index('ㅏ')][phoneme.index('ㅐ')] = b
cost_matrix[phoneme.index('ㅐ')][phoneme.index('ㅏ')] = b

# ㅏ, ㅓ
cost_matrix[phoneme.index('ㅏ')][phoneme.index('ㅓ')] = b
cost_matrix[phoneme.index('ㅓ')][phoneme.index('ㅏ')] = b

# ㅗ, ㅜ
cost_matrix[phoneme.index('ㅏ')][phoneme.index('ㅐ')] = b
cost_matrix[phoneme.index('ㅐ')][phoneme.index('ㅏ')] = b

# ㅓ, ㅗ
cost_matrix[phoneme.index('ㅓ')][phoneme.index('ㅗ')] = b
cost_matrix[phoneme.index('ㅗ')][phoneme.index('ㅓ')] = b

# ㅔ, ㅐ
cost_matrix[phoneme.index('ㅔ')][phoneme.index('ㅐ')] = b
cost_matrix[phoneme.index('ㅐ')][phoneme.index('ㅔ')] = b

# ㅖ, ㅒ
cost_matrix[phoneme.index('ㅖ')][phoneme.index('ㅒ')] = b
cost_matrix[phoneme.index('ㅒ')][phoneme.index('ㅖ')] = b


for i in range(len(phoneme)):
    for j in range(len(phoneme)):
        if (phoneme[i] in ja and phoneme[j] in mo) or (phoneme[i] in mo and phoneme[j] in ja): # 모음, 자음 
            cost_matrix[i][j] = 1.2
        elif (phoneme[i] in ja and phoneme[j] in bat) or (phoneme[i] in bat and phoneme[j] in ja): # 겹받침, 자음
            cost_matrix[i][j] = 1.1
        elif (phoneme[i] in mo and phoneme[j] in bat) or (phoneme[i] in bat and phoneme[j] in mo): # 모음 , 겹받침
            cost_matrix[i][j] = 1.3

# 겹받침끼리의 비용
for i in bat:
    for j in bat:
        if i != j:  # 같은 겹받침은 이미 초기화했기 때문에 다른 경우에만 비용 다시 초기화 해야함.
            cost_matrix[phoneme.index(i)][phoneme.index(j)] = 0.9  # 겹받침끼리

# print(cost_matrix[phoneme.index('ㄱ')])
# print(cost_matrix[phoneme.index('ㄲ')])
# print(cost_matrix[phoneme.index('ㅋ')])
# print(cost_matrix[phoneme.index('ㅔ')])
# print(cost_matrix[phoneme.index('ㅐ')])
# print(cost_matrix[phoneme.index('ㄱ')])
# print(cost_matrix[phoneme.index('ㄳ')])
# print(cost_matrix[phoneme.index('ㅄ')])



############################################### 편집거리 ################################################
def edit_dist(str1, str2):

    # print(str1)
    # print(str2)
    dp = [[0] * (len(str2)+1) for _ in range(len(str1) + 1)]
    for i in range(1, len(str1)+1):
        dp[i][0] = i
    for j in range(1, len(str2)+1):
        dp[0][j] = j


    for i in range(1, len(str1)+1):
        for j in range(1, len(str2)+1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + cost_matrix[phoneme.index(str1[i-1])][phoneme.index(str2[j-1])]  # 같은글자 -1

            else:
                left = dp[i][j-1] 
                up = dp[i-1][j] 
                left_up = dp[i-1][j-1] 

                min_val = min(left, up)
                if min_val < left_up: 
                    dp[i][j] = min_val + 0.45  # 삭제/삽입 비용을 낮춤 0.45

                else:
                    cost = cost_matrix[phoneme.index(str1[i-1])][phoneme.index(str2[j-1])] 
                    dp[i][j] = left_up + 1 + cost  # 대체 비용은 디폴트 1.2


    return dp[-1][-1]


######################################### 테스트코드 ##################################################

# 한글제외한 문자는 모두 제거해야함!! 안하면 에러남


from jamo import h2j, j2hcj
import pandas as pd

plant_csv = pd.read_csv('/Users/eunbin/Desktop/Projects/saessack-server/extra/data/tag/PLANT.csv', encoding='utf-8')
tags = list(plant_csv['PLT'])
tags.sort(key=len)
plants = []
for tag in tags:
    if tag not in plants:
        plants.append(tag)


text = input()
jamo_str = j2hcj(h2j(text))

# plants = ['베고니아', '배고니아', '배고니어', '바구니야', '수', '짜장면', '장미', '감']
# plants = ['베고니아', '배고니아']

result = []
cnt = -1
for plant in plants:
    cnt +=1
    
    # print(plant)
    anaylzed = j2hcj(h2j(plant))
    distance = edit_dist(jamo_str, anaylzed)
    item ={
            'name' : plant, 
            'distance' : distance
    }
    result.append(item)

result = sorted(result, key=lambda x: x['distance'],reverse=False)
print(result[:10])
