import math

values = {
    "Object": ["attr1","attr2","attr3","attr4","attr5","attr6"],
    "1":    [1, 2, 0, 0, 0, 0],
    "2":    [1, 0, 1, 1, 1, 0],
    "3":    [3, 0, 0, 0, 0, 3],
    "4":    [2, 4, 0, 0, 0, 0],
}


attr_matrix = {
    "attr1": [1, 1, 3, 2],
    "attr2": [2, 0, 0, 4],
    "attr3": [0, 1, 0, 0],
    "attr4": [0, 1, 0, 0],
    "attr5": [0, 1, 0, 0],
    "attr6": [0, 0, 3, 0]
}
NUM_DOCS = 4

voc = list(attr_matrix.keys())
voc.sort()

print(values)

def cosine(dv, qv):
    sumdq, sumd, sumq = 0, 0, 0
    # Iterate two lists parallel
    for wtd, wtq in zip(dv, qv):
        sumdq += wtd * wtq
        sumd += wtd**2
        sumq += wtq**2
    return sumdq / math.sqrt(sumd * sumq)

scores = {}

for d in range(NUM_DOCS):
    dtv = []
    for t in voc:
        dtv.append(tdm_tfidf[t][d])
    score = round(cosine(dtv, tqv_tfidf), 3)  # round to 3 digits
    scores[d] = score
    print("scoring D" + str(d), dtv, "vs. ", tqv_tfidf, score)


for d, score in sorted(scores.items(), key=operator.itemgetter(1), reverse=True):
    print("D" + str(d+1) + ": " + str(score))