import re


def read_txt(filename):
    sentences = []
    with open(filename, "r") as f:
        for line in f:
            sentences.append(line.strip())
    return sentences


def split_sentence(sentences):
    res = []
    for sentence in sentences:
        temp = re.split("[,，。.、;；\'\"\(\)“（）【】\[\]\?？:：!！\s+]", sentence)
        res.extend(temp)
    res = list(set(res))
    return res


def is_same_set(s1, s2):
    return len(s1 & s2) == len(s1) == len(s2)


def merge_dicts_sum(dict1, dict2):
    for key in dict2:
        if key in dict1:
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]


# def intersection(set1, set2):
#     res = set()
#     for elem in set1:
#         if elem in set2:
#             res.add(elem)
#     return res
#
#
# def union(set1, set2):
#     res = set(set1)
#     for elem in set2:
#         if elem not in res:
#             res.add(elem)
#     return res