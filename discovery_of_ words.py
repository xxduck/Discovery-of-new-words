# -*- coding=utf-8 -*-
import math
import re

CON = {}

# 使用这串字符串的目的是，这个字符串包含所有比较重要的字，字对我重要，词才对我重要，字不重要就可以筛去了
# 当然你可以在下面的断句函数中取消在这个字符串中的循环
pre = """骏＝-宝=，菱柳宏！的了7五。删车聚友有一是》不我…家这30个会？们上到1来就好没在看5琥·珀么下州人说奖多豪天都俊震光里哥图.去6大还音小开点*用莞谊发神要吗年队以怎你时牌动也出过华子能地证棍面什买片山那样滴群为―之后活手、知拍吧2提可滋跑款钱前想道机主给月兄噪问加位已中自回改次现心谢四漠48和起装今马喷咯接做响行市啊得少才打准美路方弟炮果线通感鲨祝照题保三七高声各村分吃把～除很等完公边号轮最第几游/真水长量丁灯己广两场又成品快走区贴候定油航他百于十如景胎本着望≈名换农气首意话减东门拉刚呢桂头生求新然搞相後挡只合白比荣乡早县_工老城速盘认亮迎对办再解花觉转适始正试导块带谁销~全驾希【@经型古烤S待厂】包见所朋亲－论效表关晚千旗太更远?店儿交直事种间哪礼底记拆秭情文让西请甲伙同些女电别汽哈明师录向体送实满作右板乐影标因二媒注坑"""


# 断句
def break_sentence(strings):
    splited = re.split(
        r'[\n\r \r\n   ,，\s。 }{）、（：=》《”? ― ()|！“‘’”？！；~/…:】!#%\*\.\[\]【★]', strings, flags=re.M)
    tmp = []
    for s in splited:
        for p in pre:
            if p in s:
                tmp.append(s)
                break
    # print(f"完成低频词过滤，当前字典长度{len(CON)}")    
    return splited


# 断词
def break_word(string, maxword_length):
    # print(f"开始断词，当前字典长度{len(CON)}")

    lens = len(string)
    # 默认取长度为2及以上的为词
    if lens >= 2:
        for i in range(lens):
            # 筛掉超过设置长度的词，节约字典使用
            for j in range(i + 1, i + maxword_length + 1):
                word = string[i:j]
                count(word, string[i - 1:i], string[j:j + 1])


# 统计词频，为计算自由度，凝合程度
def count(word, left, right):
    # 参数： 词，左邻字，右邻字
    if word in CON:
        CON[word][0] += 1

        
        # 如果左邻字在
        for i in CON[word][1]:
            if left in i:
                i[left] += 1
                break
        else:
            CON[word][1].append({left: 1})
        # 如果右邻字在
        for i in CON[word][2]:
            if right in i:
                i[right] += 1
                break
        else:
            CON[word][2].append({right: 1})

    else:
        CON[word] = [1, [], []]


# 凝合度计算
def coagulability():
    # print(f"开始计算凝结度，当前字典长度{len(CON)}")
    all_words = 0
    for k in CON:
        all_words += CON[k][0]

    print(CON)
    
    for k in CON:
        min_value = 99999
        i = 1
        word_lens = len(k)
        while i < word_lens:
            left = k[:i]
            right = k[i:]
            if left in CON and right in CON:
                result = (CON[k][0] / all_words) / ((CON[left][0] / all_words) * (CON[right][0] / all_words))
                min_value = result if result < min_value else min_value
            i += 1
        CON[k].append(min_value)

    # for k in CON:
    #     if len(k) > 0:
    #         if k[0] in CON and k[1:] in CON and k[-1] in CON and k[:-1] in CON:
    #             left = (CON[k][0] / all_words) / (
    #                 CON.get(k[0])[0] * CON.get(k[1:])[0])
    #             right = (CON[k][0] / all_words) / (
    #                 CON.get(k[-1])[0] * CON.get(k[:-1])[0])
    #             CON[k].append(left if left < right else right)
    #         else:
    #             CON[k].append(0)
    #     else:
    #         CON[k].append(0)


# 自由度计算
def free(l):
    # print(f"开始计算自由度，当前字典长度{len(CON)}")
    lens = 0
    for i in l:
        lens += list(i.values())[0]
    result = 0

    if l and lens:
        for i in l:
            per = list(i.values())[0] / lens
            result -= per * math.log(per)
        return result
    else:
        return result


def main(string, minwords=2, maxwords=5):
    sentences = break_sentence(string)
    for sentence in sentences:
        if sentence:
            break_word(sentence, maxwords)

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
    # print(f"开始输出结果，当前字典长度{len(CON)}")
    #  频率、自由度、 凝结度
    i = 1
    for k, v in CON.items():
        # 过滤输出
        if v[0] > 0 and len(k) >= minwords and v[-2] and v[-1]:
            print(f"{i}, {k.upper()}, {v[0]}, {v[-2]}, {v[-1]}")
            i += 1


if __name__ == '__main__':
    main("""电影院的电影影院的电影""")
