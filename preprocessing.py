import pandas as pd
from tqdm import tqdm
import re
from sklearn.model_selection import train_test_split



old_csv = pd.read_csv("from_minwoo.csv")


# print(old_csv.columns)

# print(len(old_csv)) # 44480
# 결측값 제거
old_csv = old_csv.dropna(subset=['Opinion'])
old_csv = old_csv.dropna(how='all', subset=['Procedural Posture', 'Overview', 'Outcome'])
# print(len(old_csv)) # 2150
old_csv = old_csv.reset_index(drop=True)


# 새로운 df로 만들기
rows_list = []
for i in tqdm(range(len(old_csv))):
    dict1 = {}
    dict1['input'] = old_csv.loc[i, 'Opinion']
    dict1['output'] = str(old_csv.loc[i, 'Procedural Posture']) \
                    + str(old_csv.loc[i, 'Overview']) \
                    + str(old_csv.loc[i, 'Outcome'])
    rows_list.append(dict1)

new_csv = pd.DataFrame(rows_list, columns=['input', 'output'])




p1 = r'\([^)]*\)' # () 괄호와 괄호 안의 내용
p2 = r'\[[^]]*\]' # [] 괄호와 괄호 안의 내용
p3 = r'\<[^>]*\>' # <> 괄호와 괄호 안의 내용
p4 = r'[-=+,#/\?:^$@*\"※~œ§&\n\tš™%ㆍ;!』\(\)\[\]\<\>\\‘|`\'…》]'
for i in tqdm(range(len(new_csv))):
    df_in = new_csv.loc[i, 'input']
    df_out = new_csv.loc[i, 'output']

    # 괄호 제거
    df_in = re.sub(pattern=p1, repl='', string=df_in)
    df_in = re.sub(pattern=p2, repl='', string=df_in)
    df_in = re.sub(pattern=p3, repl='', string=df_in)
    df_out = re.sub(pattern=p1, repl='', string=df_out)
    df_out = re.sub(pattern=p2, repl='', string=df_out)
    df_out = re.sub(pattern=p3, repl='', string=df_out)
    
    # 대문자 소문자로 변환
    df_in = df_in.lower()
    df_out = df_out.lower()

    # 특수문자 제거
    df_in = re.sub(pattern=p4, repl=' ', string=df_in)
    df_out = re.sub(pattern=p4, repl=' ', string=df_out)
    df_in = re.sub(' +', ' ', df_in)
    df_out = re.sub(' +', ' ', df_out)

    new_csv.loc[i, 'input'] = df_in
    new_csv.loc[i, 'output'] = df_out
    
# print(new_csv)
# new_csv.to_csv("preprocessed.csv", encoding='utf-8-sig')


x_train, x_test, y_train, y_test = train_test_split(new_csv['input'], new_csv['output'], test_size=0.1, shuffle=True, random_state=1)
train = pd.DataFrame({'input':x_train, 'output':y_train}, columns=['input', 'output'])
test = pd.DataFrame({'input':x_test, 'output':y_test}, columns=['input', 'output'])
train = train.reset_index(drop=True)
test = test.reset_index(drop=True)


# train.to_csv("train.csv", encoding='utf-8-sig')
# test.to_csv("test.csv", encoding='utf-8-sig')