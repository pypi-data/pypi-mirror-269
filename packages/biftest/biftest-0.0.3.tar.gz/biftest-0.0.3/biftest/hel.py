import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import json


def joinplot(jsonData, xStr, yStr):
    insertData = json.dumps(jsonData)
    df = pd.read_json(insertData, encoding='utf-8')
    
    plt.rcParams['font.family'] = 'Malgun Gothic'
    mpl.rcParams['axes.unicode_minus']=False

    sns.jointplot(x=xStr, y=yStr, data=df, kind='reg')

    plt.show()


def helloBix5():
    print('helloBix5')

# 예시로 xStr, yStr를 지정
#xStr = '유입량'
#yStr = '방류량'

# 예시로 JSON 파일 경로를 지정
#file_path = 'sewerData.json'

#with open(file_path, 'r', encoding='utf-8') as file:
#    json_data = json.load(file)

# joinplot 함수 호출
#joinplot(json_data, xStr, yStr)

