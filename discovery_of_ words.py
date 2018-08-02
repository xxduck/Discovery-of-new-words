# -*- coding=utf-8 -*-
import math
import re


CON = {}


# 断句
def break_sentence(strings):
    splited = re.split(r'[\n\r \r\n   ,，\s。 }{]', strings, flags=re.M)
    return splited


# 断词
def break_word(string):
    lens = len(string)
    # 默认取长度为2及以上的为词
    if lens >= 2:
        for i in range(lens):
            for j in range(i, lens):
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
    

def main(string, minwords=2, maxwords=5):
    sentences = break_sentence(string)
    for sentence in sentences:
        if sentence:
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

    # 过滤结果输出
    for k, v in CON.items():
        if v[0] > 1 and len(k) >= minwords:
            print(k, v[0], v[-2], v[-1])
        

if __name__ == '__main__':
    main("""电影院的电影影院的电影""")
