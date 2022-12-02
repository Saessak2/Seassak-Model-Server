from jamo import h2j, j2hcj


def edit_dist(str1, str2):
    dp = [[0] * (len(str2)+1) for _ in range(len(str1) + 1)]
    for i in range(1, len(str1)+1):
        dp[i][0] = i
    for j in range(1, len(str2)+1):
        dp[0][j] = j

    for i in range(1, len(str1)+1):
        for j in range(1, len(str2)+1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]

            else:
                dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1]) + 1

    return dp[-1][-1]

def adjust(str1, str2, distance):
    score = 1
    str1 = [x for x in str1] # ['ㄱ', 'ㅏ', 'ㄴ'] 이런식으로 배열에 담기
    str2 = [x for x in str2]
    
    if len(str2) < len(str1): # str2 길이가 str1 보다 짧으면 교환,
        temp = str2
        str1 = str2
        str2 = temp

    for i in range(len(str1)): # str1 개수만큼 반복
        if str1[i] == str2[i]: 
            distance *= 0.2
    
    # flag = False
    # is_removed = False
    # for i in str1:
    #     for j in str2:
    #         if i == j:
    #             flag = True
    #             distance *= 0.8
    # if flag == False:
    #     is_removed = True

    distance = round(distance, 4) # 소수점 넷째자리까지 반올림
    return distance


import pandas as pd
plant_csv = pd.read_csv('/Users/eunbin/Desktop/Projects/saessack-server/extra/data/tag/PLANT.csv', encoding='utf-8')
tags = list(plant_csv['PLT'])
tags.sort(key=len)
plants = []
for tag in tags:
    if tag not in plants:
        plants.append(tag)
print(len(plants))


input = input("검색어 >")
input = j2hcj(h2j(input)) # 자모 분리

result = []
for plant_name in plants:
    plant = j2hcj(h2j(plant_name)) # 자모 분리
    distance = edit_dist(input, plant)
    print(plant_name,':', distance)


    adjusted_distance = adjust(input, plant, distance)
    # if is_removed == True:
    #     continue
    
    dic = {
        'plant': plant_name,
        'distance': adjusted_distance
    }

    result.append(dic)

result = sorted(result, key=lambda data: data['distance'], reverse=False) # 거리순 정렬 - 오름차순
result = result[:10]
print(result)

