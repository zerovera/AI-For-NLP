import pandas as pd
import re
import jieba
import requests
from collections import Counter
from functools import reduce


# 预处理
database = 'F:/python/workspace/nlp/homework/sqlResult_1558435.csv'
data_frame = pd.read_csv(database, encoding='gb18030')
all_articles = data_frame['content'].tolist()


def token(string):
    return ' '.join(re.findall('[\w|\d]+', string))


def cut(string):
    return list(jieba.cut(string))

all_articles = [token(str(a)) for a in all_articles]
text = ''
for a in all_articles:
    text += a
TEXT = text
ALL_TOKENS = cut(TEXT)
valida_tokens = [t for t in ALL_TOKENS if t.strip() and t != 'n']


# 插入一段正则和爬虫
url = 'https://movie.douban.com/'
response = requests.get(url)
html_content = response.text
image_pattern = re.compile('https://img3.doubanio.com/view/photo/s_ratio_poster/public/\w\d+.\w+')
print(image_pattern.findall(html_content))


# one-Gram
words_count = Counter(valida_tokens)
frequency_all = [f for w, f in words_count.most_common()]
frequency_sum = sum(frequency_all)


def get_prob(word):
    esp = 1 / frequency_sum
    if word in words_count:
        return words_count[word] / frequency_sum
    else:
        return esp


def product(numbers):
    return reduce(lambda n1, n2: n1 * n2, numbers)


def language_model_one_gram(string):
    words = cut(string)
    return product([get_prob(w) for w in words])


sentences = """
这是一个比较正常的句子
这个一个比较罕见的句子
小明毕业于清华大学
小明毕业于秦华大学
""".split()

for s in sentences:
    print(s, language_model_one_gram(s))

need_compared = [
    "今天晚上请你吃大餐，我们一起吃日料 明天晚上请你吃大餐，我们一起吃苹果",
    "真事一只好看的小猫 真是一只好看的小猫",
    "我去吃火锅，今晚 今晚我去吃火锅"
]

for s in need_compared:
    s1, s2 = s.split()
    p1, p2 = language_model_one_gram(s1), language_model_one_gram(s2)
    better = s1 if p1 > p2 else s2
    print('{} is more possible'.format(better))
    print('-' * 4 + ' {} with probability {}'.format(s1, p1))    # probability拼写错误
    print('-' * 4 + ' {} with probability {}'.format(s2, p2))


# two-Gram
valid_tokens = [str(t) for t in valida_tokens]
all_2_grams_words = [''.join(valid_tokens[i:i+2]) for i in range(len(valid_tokens[:-2]))]
_2_gram_sum = len(all_2_grams_words)
_2_gram_counter = Counter(all_2_grams_words)


def get_combination_prob(w1, w2):
    if w1 + w2 in _2_gram_counter:
        return _2_gram_counter[w1+w2] / _2_gram_sum
    else:
        return 1 / _2_gram_sum


def get_prob_2_gram(w1, w2):
    return get_combination_prob(w1, w2) / get_prob(w1)


def language_model_of_2_gram(sentence):   # language拼写错误
    sentence_probability = 1
    words = cut(sentence)
    for i, word in enumerate(words):
        if i == 0:
            prob = get_prob(word)
        else:
            previous = words[i - 1]
            prob = get_prob_2_gram(previous, word)
        sentence_probability *= prob
    return sentence_probability

need_compared = [
    "今天晚上请你吃大餐，我们一起吃日料 明天晚上请你吃大餐，我们一起吃苹果",
    "真事一只好看的小猫 真是一只好看的小猫",
    "今晚我去吃火锅 今晚火锅去吃我",
    "洋葱奶昔来一杯 养乐多绿来一杯"
]

for s in need_compared:
    s1, s2 = s.split()
    p1, p2 = language_model_of_2_gram(s1), language_model_of_2_gram(s2)
    better = s1 if p1 > p2 else s2
    print('{} is more possible'.format(better))
    print('-' * 4 + ' {} with probability {}'.format(s1, p1))
    print('-' * 4 + ' {} with probability {}'.format(s2, p2))
