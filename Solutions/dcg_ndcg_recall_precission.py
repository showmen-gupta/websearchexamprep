#!/usr/bin/python3
import math

"""
This script compute Recall, Precision and F-measures.

Let say there are 12 dogs and some cat. And an identifier classified
8 dogs. Out of 8 classified dogs, 5 are actually dog and 3 cats.
So, Precision = 5/8.
    Recall = 5/12
    F-Measure = 2*R*P / (R+P)

A = set of relevent document
B = set of retreived docuemnt
R = len(intersect(A,B)) / len(A)
P = len(intersect(A,B)) / len(B)
F = 2*R*P/(R+P)
"""

# returns number of correct identification
def intersect(a, b):
    c = 0
    for i in b:
        if i in a:
            c += 1
    return c

# returns how many are correctly identified from the retrieved set. (true positive)
def precision(gt, b, at=None):
    if at is None:
        return intersect(gt, b) / len(b)
    else:
        return intersect(gt, b[:at]) / len(b[:at])

# return  how many are correctly identified from whole dataset.
def recall(gt, b, at=None):
    """
    :param gt: ground truth or relevant documents
    :param b: retrieved documents
    :param at: calculate recall up to at
    :return:
    """
    if at is None:
        return intersect(gt, b) / len(gt)
    else:
        return intersect(gt, b[:at]) / len(gt)


# returns f-measure
def fmeasure(gt, b, at=None):
    """
    :param gt: ground truth
    :param b: retrieved documents
    :param at:
    :return:
    """
    return 2 * recall(gt, b, at) * precision(gt, b, at) / (recall(gt, b, at) + precision(gt, b, at))

# return average precision
# if i'th doc in retreived set  is relavent, then calculate P@i
# return the average
def avg_precision(gt, b):
    p = []
    for idx, i in enumerate(b):
        if i in gt:
            p.append(precision(gt, b, idx+1))
    return sum(p) / len(gt)

def mean_ap(queries):
    """
    :param queries: [[gt1, q1], [gt2, q2]]
    :return:
    """
    map = []
    for gt, b in queries:
        map.append(avg_precision(gt, b))
    return sum(map) / len(map)

# 1 divided by the position of first relavent doc retreived
def reciprocal_rank(gt, b):
    for idx, i in enumerate(b):
        if i in gt:
            return 1 / (idx+1)


def mean_reciprocal(queries):
    """
    :param queries: [[gt1, q1], [gt2, q2]]
    :return:
    """
    mrr = []
    for gt, b in queries:
        mrr.append(reciprocal_rank(gt, b))
    return sum(mrr) / len(mrr)


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
        return [round(sum(gain[:i]), 2) for i in range(1, len(gain) + 1)]
    else:
        gain = discounted_gain(rel[:at])
    return [round(sum(gain[:i]), 2) for i in range(1, len(gain) + 1)]


# normalize DCG or NDCG
def ndcg(rel, at=None):
    l = len(rel)
    _dcg = dcg(rel, at)
    _ideal_dcg = dcg(sorted(rel, reverse=True), at)

    if at is not None:
        l = at
    _ndcg = [round(_dcg[i] / _ideal_dcg[i], 2) for i in range(l)]

    if at is not None:
        return _ndcg[at-1]
    return _ndcg

    return _ndcg

if __name__ == "__main__":
    # for query 1
    # A1 = [1, 1, 1, 1, 1, 1]  # a list of relevant documents or ground truth or actual label
    # B1 = [1, 0, 1, 1, 1, 1, 0, 0, 0, 1]  # a list of retrieved documents or predicted label
    # B12 = [0, 1, 0, 0, 1, 1, 1, 0, 1, 1]  # a list of retrieved documents or predicted label
    #
    # # for query 2
    # A2 = [1, 1, 1, 1, 1]
    # B2 = [1, 0, 1, 0, 0, 1, 0, 0, 1, 1]
    #
    # # for query 3
    # A3 = [1, 1, 1]
    # B3 = [0, 1, 0, 0, 1, 0, 1, 0, 0, 0]
    #
    # print("Recall = ", recall(A1, B1, at=10))
    # print("Precision = ", precision(A1, B1, at=10))
    # print("F-measure = ", fmeasure(A1, B1, at=5))
    # print("Avg Precision = ", avg_precision(A1, B1))
    #
    # # mean AP or MAP
    # # calculate avg AP for different queries and return average
    # print("MAP = ", mean_ap([[A1, B1], [A2, B2], [A3, B3]]))
    #
    # # reciprocal rank
    # print("Reciprocal = ", reciprocal_rank(A1, B1))
    # # mean reciprocal
    # #print("Mean reciprocal rank MRR = ", mean_reciprocal( [A2 , [B1, B12]]))
    #
    # print("Mean reciprocal rank MRR = ", mean_reciprocal([[A2, B12], [B1, B12]]))
    #
    # # discounted gain, document judged on 0-3 relevance scale
    # drel = [3, 2, 3, 0, 0, 1, 2, 2, 3, 0]
    # print("discounted gain= ", discounted_gain(drel))
    #
    # print("DCG = ", dcg(drel))
    # print("DCG@5 = ", dcg(drel, at=5))
    #
    # # NDCG
    # print("NDCG = ", ndcg(drel))
    #
    # #### Lecture 3 Exercise
    # q1_a = [1, 2, 6, 5, 9, 10, 7, 4, 8, 3]
    # q1_b = [10, 9, 8, 7, 5, 4, 6, 2, 1, 3]
    # gt1 = [1, 4, 5]
    #
    # q2_a = [1, 2, 4, 5, 7, 10, 8, 3, 9, 6]
    # q2_b = [1, 3, 2, 4, 5, 6, 8, 7, 10, 9]
    # gt2 = [3, 6]
    #
    # q3_a = [1, 7, 4, 5, 3, 6, 9, 8, 10, 2]
    # q3_b = [2, 4, 3, 7, 5, 6, 1, 8, 9, 10]
    # gt3 = [7]
    #
    # # effective matrix for system A
    # p5_q1 = precision(gt1, q1_a, at=5)
    # p5_q2 = precision(gt1, q2_a, at=5)
    # print("p@5 for A on Q1", p5_q1)
    # print("AP for A on Q1", avg_precision(gt1, q1_a))
    # print("RR for B on Q2", reciprocal_rank(gt2, q2_b))
    # print("MRR for B", mean_reciprocal([[gt1, q1_b], [gt2, q2_b]]))
    # print("MAP for A", mean_ap([[gt1, q1_a], [gt2, q2_a]]))
    # print("MAP for B", mean_ap([[gt1, q1_b], [gt2, q2_b]]))

    # p10_q1 = precision(gt1, q1_a, at=10)
    # _ap_q1 = avg_precision(gt1, q1_a)
    # rr_q1 = reciprocal_rank(gt1, q1_a)
    #
    # p5_q2 = precision(gt2, q2_a, at=5)
    # p10_q2 = precision(gt2, q2_a, at=10)
    # _ap_q2 = avg_precision(gt2, q2_a)
    # rr_q2 = reciprocal_rank(gt2, q2_a)
    #
    # p5_q3 = precision(gt3, q3_a, at=5)
    # p10_q3 = precision(gt3, q3_a, at=10)
    # _ap_q3 = avg_precision(gt3, q3_a)
    # rr_q3 = reciprocal_rank(gt3, q3_a)
    #
    # avgP5 = (p5_q1 + p5_q2 + p5_q3) / 3
    # avgP10 = (p10_q1 + p10_q2 + p10_q3) / 3
    # MAP = (_ap_q1 + _ap_q2 + _ap_q3) / 3
    # MRR = (rr_q1 + rr_q2 + rr_q3) / 3
    #
    # print("Query \t P@5 \t p@10 \t (M)AP \t (M)RR")
    # print("{} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f}".format("Q1", p5_q1, p10_q1, _ap_q1, rr_q1))
    # print("{} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f}".format("Q2", p5_q2, p10_q2, _ap_q2, rr_q2))
    # print("{} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f}".format("Q3", p5_q3, p10_q3, _ap_q3, rr_q3))
    # print("{} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f}".format("Avg", avgP5, avgP10, MAP, MRR))
    #
    # # effective matric for system A
    # p5_q1 = precision(gt1, q1_b, at=5)
    # p10_q1 = precision(gt1, q1_b, at=10)
    # _ap_q1 = avg_precision(gt1, q1_b)
    # rr_q1 = reciprocal_rank(gt1, q1_b)
    #
    # p5_q2 = precision(gt2, q2_b, at=5)
    # p10_q2 = precision(gt2, q2_b, at=10)
    # _ap_q2 = avg_precision(gt2, q2_b)
    # rr_q2 = reciprocal_rank(gt2, q2_b)
    #
    # p5_q3 = precision(gt3, q3_b, at=5)
    # p10_q3 = precision(gt3, q3_b, at=10)
    # _ap_q3 = avg_precision(gt3, q3_b)
    # rr_q3 = reciprocal_rank(gt3, q3_b)
    #
    # avgP5 = (p5_q1 + p5_q2 + p5_q3) / 3
    # avgP10 = (p10_q1 + p10_q2 + p10_q3) / 3
    # MAP = (_ap_q1 + _ap_q2 + _ap_q3) / 3
    # MRR = (rr_q1 + rr_q2 + rr_q3) / 3
    #
    # print("Query \t P@5 \t p@10 \t (M)AP \t (M)RR")
    # print("{} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f}".format("Q1", p5_q1, p10_q1, _ap_q1, rr_q1))
    # print("{} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f}".format("Q2", p5_q2, p10_q2, _ap_q2, rr_q2))
    # print("{} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f}".format("Q3", p5_q3, p10_q3, _ap_q3, rr_q3))
    # print("{} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f}".format("Avg", avgP5, avgP10, MAP, MRR))
    #
    # ### task 2
    # q1 = [2, 1, 3, 4, 5, 6, 10, 7, 9, 8]
    # q2 = [1, 2, 9, 4, 5, 6, 7, 8, 3, 10]
    # q3 = [1, 7, 4, 5, 3, 6, 9, 8, 10, 2]
    # rel1 = [1, 2, 0, 3, 0, 0, 0, 0, 0, 0]
    # rel2 = [2, 1, 0, 3, 0, 0, 0, 1, 3, 0]
    # rel3 = [3, 2, 3, 2, 0, 0, 0, 0, 0, 0]
    #
    # ndcg5_q1 = ndcg(rel1, at=5)
    # ndcg5_q2 = ndcg(rel2, at=5)
    # ndcg5_q3 = ndcg(rel3, at=5)
    # avgNDCG5 = (ndcg5_q1 + ndcg5_q2 + ndcg5_q3) / 3
    #
    # ndcg10_q1 = ndcg(rel1, at=10)
    # ndcg10_q2 = ndcg(rel2, at=10)
    # ndcg10_q3 = ndcg(rel3, at=10)
    # avgNDCG10 = (ndcg10_q1 + ndcg10_q2 + ndcg10_q3) / 3
    #
    # print("Query \t NDC@5 \t NDCG@10")
    # print("{} \t {:.3f} \t {:.3f}".format("Q1", ndcg5_q1, ndcg10_q1))
    # print("{} \t {:.3f} \t {:.3f}".format("Q2", ndcg5_q2, ndcg10_q2))
    # print("{} \t {:.3f} \t {:.3f}".format("Q3", ndcg5_q3, ndcg10_q3))
    # print("{} \t {:.3f} \t {:.3f}".format("Avg", avgNDCG5, avgNDCG10))

    # value1=[0, 1, 1, 0, 0, 0, 1, 1, 0, 0]
    # value2=[1, 1, 1, 1, 0, 0, 1, 0, 0, 1]
    #
    # print("Recall = ", recall(value1, value2, at=10))
    # print("Precision = ", precision(value1, value2, at=10))
    # print("F-measure = ", fmeasure(value1, value2, at=10))


    q1_a = [1, 2, 4, 3, 6, 8, 10, 5, 9, 7]
    q1_b = [2, 7, 5, 8, 4, 9, 1, 6, 10, 3]
    gt1 = [2, 3, 4, 8, 10, 12]

    p5_q1 = precision(gt1, q1_b, at=5)
    _ap_q1 = avg_precision(gt1, q1_a)
    print(_ap_q1)
    # rr_q1 = reciprocal_rank(gt1, q1_a)

    # p5_q2 = precision(gt2, q2_a, at=5)
    # p10_q2 = precision(gt2, q2_a, at=10)
    # _ap_q2 = avg_precision(gt2, q2_a)
    # rr_q2 = reciprocal_rank(gt2, q2_a)
