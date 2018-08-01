# -*- coding=utf-8 -*-
import math, re

s = """电影院的电影"""

CON = {}


# 断句
def break_sentence(strings):
    splited = re.split(r'[\n\r \r\n   ,，\s。 ]', strings, flags=re.M)
    return splited

# 断词
def break_word(string, min_str=4, max_str=10):
    lens = len(string)
    if lens > min_str:
        for i in range(lens):
            if len(string[i:]) > min_str:
                for j in range(i, i+max_str):
                    word = string[i:j]
                    count(word, string[i-1: i], string[i: i+1])


# 统计词频，计算自由度，凝合程度
def count(word, left, right):
    # 参数： 词，左邻字，右邻字


    if word in CON:
        CON[word][0] += 1

        # 如果左邻字在
        CON[word][1].append(left)
        # 如果右邻字在
        CON[word][2].append(right)

    else:
        CON[word] = [1, [], []]


# 凝合度计算
def coagulability():

    all_words = 0
    for k in CON:
        all_words += CON[k][0]

    for k in CON:
        if len(k) > 0:
            if k[0] in CON and k[1:] in CON and k[-1] in CON and k[:-1] in CON:
                left = (CON[k][0] / all_words) / (CON.get(k[0])[0] * CON.get(k[1:])[0])
                right = (CON[k][0] / all_words) / (CON.get(k[-1])[0] * CON.get(k[:-1])[0])
                CON[k].append(left if left < right else right)
            else:
                CON[k].append(0)
        else:
            CON[k].append(0)

# 自由度计算
def free(l):
    lens = len(l)
    result = 0

    if l and lens:

        for i in l:
            per = float(l.count(i)) / lens
            result -= per * math.log(per) 
        return result
    else:
        return result
    

def main():
    sentences = break_sentence(s)
    for sentence in sentences:
        break_word(sentence)

    # 计算自由度
    for k, v in CON.items():
        # 邻字
        # print(k,v)
        lf = free(v[1])
        rf = free(v[2])
        CON[k].append(lf if lf > rf else rf)
    
    # 计算凝结度
    coagulability()
    
    # 打印结果
    for k, v in CON.items():
        print(k, v)
        

if __name__ == '__main__':
    main()
