# -*- coding: utf-8 -*-
import ch
import jieba
import jieba.analyse
import jieba.posseg as pseg

# 範例

# text1 = '我最近和我朋友都在看籃球'

# print('\n- 斷字:\n\n', '|'.join(jieba.cut(text1, cut_all=False, HMM=True))+'\n')

# words = pseg.cut(text1)
# for word, flag in words:
#     print(word, flag)


def partition(text):

    # jump = 0
    keyword = []

    # 冗詞

    ignore = ['照片', '貼圖', '晚安', '早安', '感覺', '時候', '結果', '嘴巴',
              '電話', '話', '樓', '意思', '原本', '大家', '時間', '眼', '人', '小夜']

    # 把通話及照片的相關字句刪掉

    for Line in text:
        if '☎' in Line:
            # jump = 1
            return None

    # 自定義部分詞彙

    jieba.load_userdict('./data/userDict.txt')

    # 斷字結果

    # if jump == 0:
    #     result = jieba.cut(text, cut_all=False, HMM=True)
    #     print('|'.join(result))

    # 關鍵字抽取

    tags = jieba.analyse.extract_tags(text, topK=8)

    # 找出合適關鍵字

    str = ''
    temp = str.join(tags)

    words = pseg.cut(temp)
    for word, flag in words:
        ignore_set = set(ignore)
        if not word in ignore_set:
            if flag == ('n' or 'nr' or 'ns' or 'nt' or 'nz'):
                keyword.append(word)

    return keyword
