import math


def nominal_similarity(p, q):
    return 1 if p == q else 0


def nominal_dissimilarity(p, q):
    return 0 if p == q else 1


def oridinal_similarity(n, p, q):
    return 1 - (abs(p - q) / (n - 1))


def ordinal_dissimilarity(n, p, q):
    """
    :param n: total number of values
    :param p: first value to compare with
    :param q: second value to compare with
    :return: dissimilarity for ordinal data type
    """
    return abs(p - q) / (n - 1)


def ecludian_distance(p, q):
    n = len(p)
    assert n == len(q)
    return math.sqrt(sum([pow(p[i] - q[i], 2) for i in range(n)]))

# in minkowski distance,
# if r = 1 => manhattan distance
# if r = 2 => Ecludian distance
# if r = infinity => Supremum distance
def minkowski_distance(p, q, r):
    n = len(p)
    assert n == len(q)
    return pow(sum([pow(abs(p[i] - q[i]), r) for i in range(n)]), 1/r)

# similarity between Binary vector
# simple matching coffecient, SMC
def smc(p, q):
    match = 0
    total = 0
    for a, b in zip(p, q):
        total += 1
        if a == b:
            match += 1

    return match / total


# Jaccard similarity ignore 0-0 match
def jaccard_similarity(p, q):
    match, total = 0, 0
    for a, b in zip(p, q):
        if a == 0 and b == 0:
            continue
        total += 1
        if a > 0 and b > 0:
            match += 1
    try:
        return match / total
    except:
        return 0

def cosine_similarity(p, q):
    """
    :param p: document vector, eg = [1,2, 1, 0.6]
    :param q: query vector, eg = [0.4, 1, 0]
    :return:
    """
    n = len(p)
    assert n == len(q)
    dot = sum([a*b for a, b in zip(p, q)])
    x = math.sqrt(sum([pow(i, 2) for i in p]))
    y = math.sqrt(sum([pow(i, 2) for i in q]))
    return dot / (x*y)

def normalization(p):
    """
    :param p: list of values
    :return: return min-max normalization
    """
    r = []
    min_v = min(p)
    max_v = max(p)
    for i in p:
        r.append((i-min_v)/(max_v - min_v))
    return r

if __name__ == "__main__":
    # # poor = 0, fair = 1, ok = 2, good = 3, wonderful = 4
    # a = [0, 1, 2, 3, 4]
    # # similarity between good and wonderful
    # s = oridinal_similarity(len(a), 3, 4)
    # print("similarity of good and wonderful = ", s)
    # p1 = (3, 1)
    # p2 = (5, 1)
    # d = ecludian_distance(p1, p2)
    # print("Ecludian distance = ", round(d, 2))
    #
    # md = minkowski_distance(p1, p2, 1)
    # print("Minkowski distance = ", round(md, 2))
    #
    # a = [1, 1, 0, 1, 0, 0, 1, 0]
    # b = [1, 0, 0, 1, 0, 0, 1, 1]
    # print("Jaccard similarity  = ", jaccard_similarity(a, b))
    # print("cosine similarity = ", round(cosine_similarity(a, b), 3))
    # a = [2*i for i in a]
    # b = [i/2 for i in b]
    # print("cosine similarity = ", round(cosine_similarity(a, b), 3))
    #
    # #### Lecture 4 exercise
    # o1 = [1, 2, 0, 0, 0, 0]
    # o2 = [1, 0, 1, 1, 1, 0]
    # o3 = [3, 0, 0, 0, 0, 3]
    # o4 = [2, 4, 0, 0, 0, 0]
    # print("Jaccard o1 vs o2 = ", round(jaccard_similarity(o1, o2), 2))
    # print("Jaccard o1 vs o3 = ", round(jaccard_similarity(o1, o3), 2))
    # print("Jaccard o1 vs o4 = ", round(jaccard_similarity(o1, o4), 2))
    # #
    # print("Cosine o1 vs o2 = ", round(cosine_similarity(o1, o2), 2))
    # print("Cosine o1 vs o3 = ", round(cosine_similarity(o1, o3), 2))
    # print("Cosine o1 vs o4 = ", round(cosine_similarity(o1, o4), 2))

    # value =[2,12,7]
    # result = normalization(value)
    # print(result)
    #
    # sim_val = [0, 1, 2, 3, 4, 5, 6]
    # s = ordinal_dissimilarity(len(sim_val),1,4)
    # print(s)

    o1 = [1, 0, 0, 1, 1, 0, 1, 1, 0, 1]
    o2 = [1, 1, 0, 1, 0, 0, 1, 0, 1, 1]

    print("Jacard Similarity:", round(jaccard_similarity(o1,o2),2))
    print("Cosine Similarity:", round(cosine_similarity(o1, o2), 2))