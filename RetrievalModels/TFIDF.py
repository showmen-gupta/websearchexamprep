import math
import operator


td_matrix = {
    "beijing": [0, 1, 0, 0, 1],
    "dish": [0, 1, 0, 0, 1],
    "duck": [3, 2, 2, 0, 1],
    "rabbit": [0, 0, 1, 1, 0],
    "recipe": [0, 0, 1, 1, 1],
    "roast": [0, 0, 0, 0, 0]
}

voc = list(td_matrix.keys())
voc.sort()

NUM_DOCS = 5

query = ["beijing", "duck", "recipe"]

#TFIDF term weighting
idf = []  # idf[i] holds the IDF weight for term voc[i]
for t in voc:
    nt = sum([1 for x in td_matrix[t] if x >0]) # number of documents that contain t
    idf.append(math.log(NUM_DOCS / nt, 10) if nt > 0 else 0)

print(idf)

#Term weighting for documents
def tfidf_docs(tdm):
    tdm_tfidf = {}

    dlen = []  # dlen[i] stores the length of the i-th document
    for d in range(NUM_DOCS):
        l = 0
        for t in voc:
            l += td_matrix[t][d]
        # sum([x for t in voc for x in td_matrix[t][d]])
        dlen.append(l)

    # iterate through terms
    for i, t in enumerate(voc):
        td = tdm[t]  # vector of docs for the given term
        tdm_tfidf[t] = []
        for d, f in enumerate(td):
            # f is the frequency of term t for doc d
            # Compute TFIDF score for term t in doc d
            tf = f / dlen[d]
            print("Values for Each Doc:"+ str(d))
            print(tf)
            tfidf = tf * idf[i]
            tdm_tfidf[t].append(round(tfidf, 3))  # round to 3 digits

    return tdm_tfidf

tdm_tfidf = tfidf_docs(td_matrix)

print(tdm_tfidf)

#TFIDF term weighting for query
def tfidf_q(tqv):
    tqv_tfidf = []
    for i, t in enumerate(voc):
        # tqv[i] holds the raw frequency for term t
        tf = tqv[i] / len(query)
        print("TF Value:")
        print(tf)
        print("IDF Value:")
        print(idf[i])

        tfidf = tf * idf[i]
        tqv_tfidf.append(round(tfidf, 3))  # round to 3 digits
    return tqv_tfidf

tqv = []
for t in voc:
    tqv.append(query.count(t) if t in query else 0)


tqv_tfidf = tfidf_q(tqv)
print(tqv, "=>", tqv_tfidf)

#Cosine similarity between a document and query vector
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