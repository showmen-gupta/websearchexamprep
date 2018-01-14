import math


def binarization(x):
    b = [[0 for i in x] for j in x]
    for idx, i in enumerate(x):
        b[idx][idx] = 1
    return b


# returns number of correct identification
def intersect(a, b):
    """
    :param a: relevant documents
    :param retrieved documents
    :return: count of relevant documents in retrieved document set
    """
    c = 0
    for i in b:
        if i in a:
            c += 1
    return c


# returns how many are correctly identified from the retrieved set. (true positive)
def precision(gt, b, at=None):
    """
    :param gt: relevant document list
    :param b: retrieved document list
    :param at: precision at
    :return: precition
    """
    if at is None:
        return intersect(gt, b) / len(b)
    else:
        return intersect(gt, b[:at]) / len(b[:at])


# return  how many are correctly identified from whole dataset.
def recall(gt, b, at=None):
    """
    :param gt: relevant document list
    :param b: retrieved document list
    :param at: recall at
    :return: recall
    """
    if at is None:
        return intersect(gt, b) / len(gt)
    else:
        return intersect(gt, b[:at]) / len(gt)


# returns f-measure
def fmeasure(gt, b, at=None):
    """
    :param gt: relevant document list
    :param b: retrieved document list
    :param at: f-measure at
    :return: f-measure
    """
    return 2 * recall(gt, b, at) * precision(gt, b, at) / (recall(gt, b, at) + precision(gt, b, at))


# return average precision
# if i'th doc in retreived set  is relavent, then calculate P@i
# return the average
def avg_precision(gt, b):
    """
    :param gt: relevant document list
    :param b: retrieved document list
    :return: AP
    """
    p = []
    for idx, i in enumerate(b):
        if i in gt:
            p.append(precision(gt, b, idx + 1))
    return sum(p) / len(gt)


AP = avg_precision


def mean_ap(queries):
    """
    :param queries: [[gt, b], [gt, b]]
    :return: MAP
    """
    map = []
    for gt, b in queries:
        map.append(avg_precision(gt, b))
    return sum(map) / len(map)


MAP = mean_ap


# 1 divided by the position of first relavent doc retreived
def reciprocal_rank(gt, b):
    """
    :param gt: relavant document list
    :param b: retrived document list
    :return:  RR
    """
    for idx, i in enumerate(b):
        if i in gt:
            return 1 / (idx + 1)


RR = reciprocal_rank


def mean_reciprocal(gt, bs):
    """
    :param gt: relevant document list
    :param bs: list of retrieved document list: [[1, 2], [1, 4]]
    :return:
    """
    mrr = []
    for b in bs:
        mrr.append(reciprocal_rank(gt, b))
    return sum(mrr) / len(mrr)


MRR = mean_reciprocal


def discounted_gain(rel):
    gain = [rel[0]]
    for idx, i in enumerate(rel[1:]):
        try:
            gain.append(round(i / math.log2(idx + 2), 2))
        except:
            gain.append(0)
    return gain


# discounted gain
# DGCp = rel1 + sum(RELi / log2(i)) where 2 <= i <= len(REL) - 1
def dcg(rel, at=None):
    if at is None:
        gain = discounted_gain(rel)
        return [sum(gain[:i]) for i in range(1, len(gain) + 1)]
    else:
        gain = discounted_gain(rel[:at])
    return [sum(gain[:i]) for i in range(1, len(gain) + 1)]


# normalize DCG or NDCG
def ndcg(rel, at=None):
    l = len(rel)
    _dcg = dcg(rel, at)
    _ideal_dcg = dcg(sorted(rel, reverse=True), at)

    if at is not None:
        l = at
    _ndcg = [_dcg[i] / _ideal_dcg[i] for i in range(l)]

    if at is not None:
        return _ndcg[at - 1]
    return _ndcg

    return _ndcg


if __name__ == "__main__":
    s = [0, 1, 2, 3, 4]
    print("binarization = ", binarization(s))

    q1a = [1, 2, 4, 5, 3, 6, 9, 8, 10, 7]
    q1b = [2, 4, 3, 10, 5, 6, 7, 8, 9, 1]
    gt1 = [1, 3]

    p5a = precision(gt1, q1a, at=5)
    p10a = precision(gt1, q1a, at=10)
    apa = avg_precision(gt1, q1a)
    rra = reciprocal_rank(gt1, q1a)

    p5b = precision(gt1, q1b, at=5)
    p10b = precision(gt1, q1b, at=10)
    apb = avg_precision(gt1, q1b)
    rrb = reciprocal_rank(gt1, q1b)

    q2a = [1, 2, 4, 5, 3, 9, 8, 6, 10, 7]
    q2b = [5, 6, 4, 1, 7, 8, 9, 10, 2]
    gt2 = [2, 4, 5, 6]

    p5a2 = precision(gt2, q2a, at=5)
    p10a2 = precision(gt2, q2a, at=10)
    apa2 = avg_precision(gt2, q2a)
    rra2 = reciprocal_rank(gt2, q2a)

    p5b2 = precision(gt2, q2b, at=5)
    p10b2 = precision(gt2, q2b, at=10)
    apb2 = avg_precision(gt2, q2b)
    rrb2 = reciprocal_rank(gt2, q2b)

    q3a = [1, 7, 4, 5, 3, 6, 9, 8, 10, 2]
    q3b = [2, 4, 3, 7, 5, 6, 1, 8, 9, 10]
    gt3 = [7]

    p5a3 = precision(gt3, q3a, at=5)
    p10a3 = precision(gt3, q3a, at=10)
    apa3 = avg_precision(gt3, q3a)
    rra3 = reciprocal_rank(gt3, q3a)

    p5b3 = precision(gt3, q3b, at=5)
    p10b3 = precision(gt3, q3b, at=10)
    apb3 = avg_precision(gt3, q3b)
    rrb3 = reciprocal_rank(gt3, q3b)

    avgp5 = (p5a + p5a2 + p5a3) / 3
    avgp10 = (p10a + p10a2 + p10a3) / 3
    MAPa = (apa + apa2 + apa3) / 3
    MRRa = (rra + rra2 + rra3) / 3

    avgp5b = (p5b + p5b2 + p5b3) / 3
    avgp10b = (p10b + p10b2 + p10b3) / 3
    MAPb = (apb + apb2 + apb3) / 3
    MRRb = (rrb + rrb2 + rrb3) / 3
    print("Query \t p@5 \t p@10 \t MAP \t MRR \t")
    print("{} \t {} \t {} \t {} \t {} \t".format("Q1", p5a, p10a, apa, rra))
    print("{} \t {} \t {} \t {} \t {} \t".format("Q2", p5a2, p10a2, apa2, rra2))
    print("{} \t {} \t {} \t {} \t {} \t".format("Q3", p5a3, p10a3, apa3, rra3))
    print("{} \t {} \t {} \t {} \t {} \t".format("Avg", avgp5, avgp10, MAPa, MRRa))

    print("for system b")
    print("Query \t p@5 \t p@10 \t MAP \t MRR \t")
    print("{} \t {} \t {} \t {} \t {} \t".format("Q1", p5b, p10b, apb, rrb))
    print("{} \t {} \t {} \t {} \t {} \t".format("Q2", p5b2, p10b2, apb2, rrb2))
    print("{} \t {} \t {} \t {} \t {} \t".format("Q3", p5b3, p10b3, apb3, rrb3))
    print("{} \t {} \t {} \t {} \t {} \t".format("Avg", avgp5b, avgp10b, MAPb, MRRb))

    ####### evluation task-2

    q1 = [2, 1, 3, 4, 5, 6, 10, 7, 9, 8]
    gt1 = [1, 2, 0, 3, 0, 0, 0, 0, 0, 0]

    q2 = [1, 2, 9, 4, 5, 6, 7, 8, 3, 10]
    gt2 = [2, 1, 0, 3, 0, 0, 0, 0, 3, 0]

    q3 = [1, 7, 4, 5, 3, 6, 9, 8, 10, 2]
    gt3 = [3, 2, 3, 2, 0, 1, 0, 1, 0, 0]

    dcg1 = dcg(gt1)
    dcg2 = dcg(gt2)
    dcg3 = dcg(gt3)

    ndcg51 = ndcg(gt1, at=5)
    ndcg52 = ndcg(gt2, at=5)
    ndcg53 = ndcg(gt3, at=5)

    ndcg101 = ndcg(gt1, at=10)
    ndcg102 = ndcg(gt2, at=10)
    ndcg103 = ndcg(gt3, at=10)

    print("DCG", dcg1)
    print("NDCG@5", ndcg51, ndcg52, ndcg53)
    print("AVG NDCG@5", (ndcg51 + ndcg52 + ndcg53) / 3)

    print("NDCG@10", ndcg101, ndcg102, ndcg103)
    print("AVG NDCG@10", (ndcg101 + ndcg102 + ndcg103) / 3)
