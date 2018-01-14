import numpy as np
import re
import pprint
import math


def is_number(s):
    try:
        complex(s)  # for int, long, float and complex
    except ValueError:
        return False

    return True


def numericalize_table(records):
    records = records.copy()
    str_to_num = {}
    number = 0
    for i in range(len(records[0])):
        for ele in set(records[:, i]):
            if not is_number(ele):
                str_to_num[ele] = number
                number += 1

    for i, row in enumerate(records):
        for j, col in enumerate(row):
            if not is_number(col):
                records[i][j] = int(str_to_num[col])
    records = records.astype(float)

    return records, str_to_num


def select_row(col_idx, col_val, operator, records):
    selected_records = None
    if operator == "==":
        selected_records = records[records[:, col_idx] == col_val]
    elif operator == "<=":
        selected_records = records[records[:, col_idx] <= col_val]
    elif operator == "<":
        selected_records = records[records[:, col_idx] < col_val]
    elif operator == ">":
        selected_records = records[records[:, col_idx] > col_val]
    elif operator == ">=":
        selected_records = records[records[:, col_idx] >= col_val]
    return selected_records


def print_format_division(a, b, laplaceC=0):
    if laplaceC:
        return str(len(a) + 1) + "/" + str(len(b) + laplaceC) + "=" + str(round((len(a) + 1) / (len(b) + laplaceC), 3))
    else:
        return str(len(a)) + "/" + str(len(b)) + "=" + str(round(len(a) / len(b), 3))


def gaussian_pdf(mu, var, x):
    return (1 / math.sqrt(2 * math.pi * var)) * math.exp((-math.pow(x - mu, 2)) / (2 * var))


def naive_bayes_classifier(cols, records, instance, isGaussian=False, isLaplace=False):
    records = records.copy()
    classes = set(records[:, -1])
    str_to_num = {}
    records, str_to_num = numericalize_table(records)

    table = {}
    for i, cls in enumerate(classes):
        cls_key = cls
        cls = int(str_to_num[cls])
        class_records = select_row(len(cols) - 1, cls, "==", records)
        table[cls_key] = {cls_key: print_format_division(class_records, records)}
        prob = 1
        prob *= len(class_records) / len(records)
        for key, val in instance.items():
            if type(val) == list:
                if not isGaussian:
                    s_records = select_row(cols.index(key), val[1], val[0], class_records)
                    p = len(s_records) / len(class_records)
                    prob *= p
                    table[cls_key][str(key) + val[0] + str(val)] = print_format_division(s_records, class_records)
                else:
                    p = gaussian_pdf(np.mean(class_records[:, cols.index(key)]),
                                     np.var(class_records[:, cols.index(key)], ddof=1), val)
                    prob *= p
                    table[cls_key]["(G)" + str(key) + "==" + str(val)] = str(p)
            else:
                if not isLaplace:
                    s_records = select_row(cols.index(key), str_to_num[val], "==", class_records)
                    p = len(s_records) / len(class_records)
                    prob *= p
                    table[cls_key][str(key) + "=" + str(val)] = print_format_division(s_records, class_records)
                else:
                    s_records = select_row(cols.index(key), str_to_num[val], "==", class_records)
                    p = (len(s_records)) + 1 / (len(class_records) + len(classes))
                    prob *= p
                    table[cls_key][str(key) + "=" + str(val)] = print_format_division(s_records, class_records,
                                                                                      len(classes))

        print("P(" + cls_key + "|X)=" + str(round(prob, 10)))
    pprint.pprint(table)

# Cols = ["Outlook","Temp","Humidity","Windy", "Play"]
# Records = np.array([
#     ["sunny",85,85,"false","No"],
#     ["sunny",80,90,"true","No"],
#     ["overcast",83,78,"false","Yes"],
#     ["rain",70,96,"false","Yes"],
#     ["rain",68,80,"false","Yes"],
#     ["rain",65,70,"true","No"],
#     ["overcast",64,65,"true","Yes"],
#     ["sunny",72,95,"false","No"],
#     ["sunny",69,70,"false","Yes"],
#     ["rain",75,80,"false","Yes"],
#     ["sunny",75,70,"true","Yes"],
#     ["overcast",72,90,"true","Yes"],
#     ["overcast",81,75,"false","Yes"],
#     ["rain",71,80,"true","No"],
# ])
#
# #if there is comparison, put data as list.
# # first value will be comparator, second value will be value
# X = {"Outlook":"sunny", "Temp":["<=",75],"Humidity":["<=",75],"Windy":"true"}
# naive_bayes_classifier(Cols,Records,X)
#
#
#
#
# #for using Gaussian distribution, just put value
# X = {"Outlook":"rain", "Temp":[87],"Humidity":[90],"Windy":"false"}
# naive_bayes_classifier(Cols,Records,X,isGaussian=True)
#
#
# #for using Gaussian distribution, just put value
# X = {"Outlook":"rain", "Temp":[87],"Humidity":[90],"Windy":"false"}
# naive_bayes_classifier(Cols,Records,X,isGaussian=True,isLaplace=True)
#
#
#
#
# Cols = ["Refund","MartialStatus","TaxableIncome","Class"]
# Records = np.array([
#     ["Yes","Single",125,"No"],
#     ["No","Married",100,"No"],
#     ["No","Single",70,"No"],
#     ["Yes","Married",120,"No"],
#     ["No","Divorced",95,"Yes"],
#     ["No","Married",60,"No"],
#     ["Yes","Divorced",220,"No"],
#     ["No","Single",85,"Yes"],
#     ["No","Married",75,"No"],
#     ["No","Single",90,"Yes"],
# ])
#
# X = {"Refund":"No", "MartialStatus":"Married","TaxableIncome":[120]}
# naive_bayes_classifier(Cols,Records,X,isGaussian=True)
#
# #with laplace smoothing
# X = {"Refund":"No", "MartialStatus":"Married","TaxableIncome":[120]}
# naive_bayes_classifier(Cols,Records,X,isGaussian=True,isLaplace=True)


Cols_exam = ["t1","t2","t3","t4","t5", "class"]
Records_exam = np.array([
    [1, 0, 2, 2, 0, "C1"],
    [3, 0, 0, 2, 3, "C3"],
    [0, 4, 2, 0, 0, "C2"],
    [1, 0, 0, 1, 1, "C1"],
    [0, 0, 0, 2, 1, "C3"],
    [0, 1, 1, 4, 3, "C3"],
    [0, 2, 1, 0, 0, "C2"],
    [1, 0, 1, 2, 3, "C3"],
])

X_val = {"class":"C2"}
naive_bayes_classifier(Cols_exam,Records_exam,X_val,isLaplace=True)