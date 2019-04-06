# BFS路线搜索
import networkx as nx
import matplotlib.pyplot as plt


BEIJING, CHANGCHUN, WULUMUQI, WUHAN, GUNAGHZOU, SHENZHEN, BANGKOK, SHANGHAI, NEWYORK = """
BEIJING CHANGCHUN WULUMUQI WUHAN GUANGZHOU SHENZHEN BANGKOK SHANGHAI NEWYORK
""".split()

connection = {
    CHANGCHUN: [BEIJING],
    WULUMUQI: [BEIJING],  # 应该是乌鲁木齐
    BEIJING: [WULUMUQI, CHANGCHUN, WUHAN, SHENZHEN, NEWYORK],
    NEWYORK: [BEIJING, SHANGHAI],
    SHANGHAI: [NEWYORK, WUHAN],
    WUHAN: [SHANGHAI, BEIJING, GUNAGHZOU, SHENZHEN],  # 漏了深圳
    GUNAGHZOU: [WUHAN, BANGKOK],
    SHENZHEN: [BEIJING,WUHAN, BANGKOK],  # 漏了北京
    BANGKOK: [SHENZHEN, GUNAGHZOU]
}

graph = connection
g = nx.Graph(graph)
#nx.draw(g)
#plt.show()


def navigator_bfs(start, destination, connection_graph):  # 应该是navigator
    paths = [[start]]  # 应该是paths
    seen = set()
    while paths:
        path = paths.pop(0)
        frontier = path[-1]   # 应该是frontier
        if frontier in seen:
            continue
        successors = connection_graph[frontier]
        for s in successors:
            if s == destination:
                path.append(s)
                return path
            elif s not in seen:  # 修改了下
                paths.append(path + [s])
        paths = sorted(paths, key=len)
        seen.add(frontier)

print(navigator_bfs(CHANGCHUN, BANGKOK, connection))




# 文本自动生成
import random

grammar_rules = """
sentence => noun_phrase verb_phrase
noun_phrase => Article Adj* noun
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>   蓝色的 |  好看的 | 小小的
"""


def parse_grammar(grammar_str, sep='=>'):
    grammar = {}
    for line in grammar_str.split('\n'):
        line = line.strip()
        if not line:
            continue
        target, rules = line.split(sep)
        grammar[target.strip()] = [r.split() for r in rules.split('|')]
    return grammar

g = parse_grammar(grammar_rules)


def gene(grammar_parsed, target='sentence'):
    if target not in grammar_parsed:
        return target
    rule = random.choice(grammar_parsed[target])
    return ''.join(gene(grammar_parsed, target=r) for r in rule if r != 'null')

print(gene(g))
