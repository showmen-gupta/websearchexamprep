import math

from collections import Counter

def accuracy(cp, tp):
    """
    :param cp: number of correct prediction, true positive + true negative
    :param tp: total prediction, tp + tn + fp + fn
    :return: cp / tp
    """
    return cp / tp

def error_rate(fp, tp):
    """
    :param fp: number of false prediction
    :param tp: number of total prediction
    :return: fp / tp
    """
    return fp / tp

def coverage(tp, tr):
    """
    :param tp: total number of prediction
    :param tr: total number of records
    :return: tp / tr
    """
    return tp / tr


def log2(n):
    try:
        return math.log2(n)
    except:
        return 0

def entrophy(p, n):
    """

    :param p: number of positive target class
    :param n: number of negative target class
    :return: information gain
    """
    t = p + n

    return -p/t * log2(p/t) - n/t * log2(n/t)

def info_gain(ep, splits= {}):
    """
    :param ep: entrophy of parent
    :param splits: a dict of splits: name of split as key and [p, n] as value
    :return: info gain of an attribute
    """
    t = sum([i + j for i, j in splits.values()])
    return ep - sum([(p+n)/t * entrophy(p, n) for p, n in splits.values()])

def gini(p, n):
    """

    :param p: number of positive target class
    :param n: number of negative target class
    :return: gini
    """
    t = p + n
    return 1 - pow(p/t, 2) - pow(n/t, 2)

def gini_index(splits={}):
    """

    :param gp: parent gini
    :param splits: a dict of splits: name of split as key and [p, n] as value
    :return: gini index of a node
    """
    t = sum([i + j for i, j in splits.values()])
    return sum([(p+n)/t * gini(p, n) for p, n in splits.values()])


def gini_index_gain(gp, splits={}):
    """
    :param gp: overall gini
    :param splits: all splits
    :return:
    """
    t = sum([i + j for i, j in splits.values()])
    return gp - sum([(p + n) / t * gini(p, n) for p, n in splits.values()])

def classification_error(p, n):
    """

    :param p: number of positive target class
    :param n: number of negative target class
    :return: classification error
    """
    t = p + n
    return 1 - max(p/t, n/t)


if __name__ == "__main__":
    Ep = entrophy(4, 6)
    a_gain = info_gain(Ep, splits={"S,M":[1, 3], "L,XL": [3,3]})

    Ep2= entrophy(1,3)
    info_gender = info_gain(Ep2, splits={"m":[0,1], "f":[1,2]})
    info_color = info_gain(Ep2, splits={"r":[1,1],"b":[0,1], "gr":[0,1]})
    print(info_gender)
    print(info_color)

    Ep3 = entrophy(3,3)
    info_gender1 = info_gain(Ep3, splits={"m": [3, 1], "f": [0, 2]})
    info_color1 = info_gain(Ep3, splits={"r": [0, 2], "b": [2, 0], "gr": [1, 1]})
    print(info_gender1)
    print(info_color1)


    # print(Ep)
    #
    # M0 = entrophy(1,3)
    #
    # b_gain = info_gain(Ep, splits={"R, G, B":[1, 3]})
    #
    # c_gain = info_gain(Ep, splits={"R, G, B": [3, 3]})
    # print("a gain = ", a_gain)
    # print("b gain = ", b_gain)
    # print("c gain =", c_gain)
    #
    # gp = gini(4, 6)
    # print("Gp = ", gp)
    # a_index = gini_index(splits={"t":[4, 3], "f": [0, 3]})
    # b_index = gini_index(splits={"t":[3, 1], "f": [1, 5]})
    # print("a index = ", a_index)
    # print("b index = ", b_index)
    # gini_gain_a = gini_index_gain(gp, splits={"t":[4, 3], "f": [0, 3]})
    # gini_gain_b = gini_index_gain(gp, splits={"t":[3, 1], "f": [1, 5]})
    # print("gini gain a = ", gini_gain_a)
    # print("gini gain b = ", gini_gain_b)

    # Ep = entrophy(9, 5)
    # gain_outlook = info_gain(Ep, splits={"s": [2, 3], "o":[4, 0], "r":[3, 2]})
    # print("Gain outlook = ", gain_outlook)
    # Ep_sunny = entrophy(2, 3)
    # gain_humid_sunny = info_gain(Ep_sunny, splits={"h": [0, 3], "n":[2, 0]})
    # print("Gain humidity | sunny =", gain_humid_sunny)
    # #Accuracy problem trail exam
    # accuracy_val= accuracy(3,5)
    # #coverage
    # coverage_val= coverage(5,10)

    # EpExam = entrophy(4,6)
    # node_1_infogain= info_gain(EpExam,splits={"S": [2, 3], "M":[4, 0] })


    # R1 = accuracy(4,1)
    # R2 = accuracy(30, 10)
    # R3 = accuracy(100, 90)
    #
    # print("R1:", R1)
    # print("R2:", R2)
    # print("R3:", R3)

