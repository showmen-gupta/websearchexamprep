import math


def pagarank(T, edges, q=0.15, max_iter=3):
    """
    :param T: total number of pages
    :param edges: out going edges
    :param q: random pic probability
    :param max_iter: maximum number of iteration to perform
    :return:
    """
    out_edge = {}
    pr = {}
    in_edge = {}
    for i in range(1, T + 1):
        out_edge[i] = 0
        pr[i] = 1/T
        in_edge[i] = []
    for (n1, n2) in edges:
        out_edge[n1] += 1
        in_edge[n2].append(n1)

    # Dealing with "rank sink" nodes
    for k, x in out_edge.items():
        if x == 0:
            out_edge[k] = T
            for y in in_edge:
                in_edge[y].append(k)

    print("Iteration 0:  ", end="")

    for k in range(1, T + 1):
        print("{:d}: {:05.3f}   ".format(k, pr[k]), end="")
    print("")  # new line

    for i in range(max_iter):
        temp = {}
        for j in range(1, T + 1):
            temp[j] = q/T + (1 - q)*sum(pr[x]/out_edge[x] for x in in_edge[j])
        pr = dict(temp)

        print("Iteration {}:  ".format(i + 1), end="")

        for k in range(1, T + 1):
            print("{:d}: {:05.3f}   ".format(k, pr[k]), end="")
        print("")  # new line

def tf(m):
    """
    :param m: term document matrix
    :return: term frequency matrix

    tf = tf/|d|
    """
    if type(m[0]) is list:
        # for term document
        tf_m = [[0 for i in m[0]] for j in m]

        d = [sum(i) for i in zip(*m)]

        for ri, r in enumerate(m):
            for ci, c in enumerate(r):
                tf_m[ri][ci] = c / d[ci]

        return tf_m
    else:
        # for term query
        tf_m = [0 for i in m]
        d = sum(m)
        for idx, i in enumerate(m):
            tf_m[idx] = i / d
        return tf_m

def idf(m):
    """
    :param m: term document matrix
    :return: inverted document frequency
    """
    d = len(m[0])
    idf_m = [0 for i in m]
    for idx, i in enumerate(m):
        try:
            idf_m[idx] = math.log(d / sum(i), 10)
        except:
            continue

    return idf_m

def tf_idf(m, idf_doc=None):
    """
    :param m: term document matrix
    :param idf_doc: idf for documents (must be given to calculate tf_idf for query)
    :return: TF-IDF
    """
    tf_m = tf(m)
    idf_m = idf(m) if idf_doc is None else idf_doc
    if idf_doc is None:
        tfidf = [[0 for i in m[0]] for j in m]
        for ri, r in enumerate(tf_m):
            for ci, c in enumerate(r):
                tfidf[ri][ci] = c * idf_m[ri]
        return tfidf
    else:
        tfidf = [0 for i in m]
        for i in range(len(tf_m)):
            tfidf[i] = tf_m[i] * idf_m[i]
        return tfidf


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

def document_score(td_m, tq_m):
    """
    :param td_m: term document matrix
    :param tq_m: term query matrix
    :return: score matrix
    """
    tfidf_doc = tf_idf(td_m)

    idf_doc = idf(td_m)
    tfidf_query = tf_idf(tq_m, idf_doc=idf_doc)

    scores = []
    d_tfidf = [list(i) for i in zip(*tfidf_doc)]
    for i in d_tfidf:
        scores.append(cosine_similarity(i, tfidf_query))
    return scores

if __name__ == "__main__":
    NODES = 6
    # EDGES = [[1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6],
    #          [3, 1], [3, 2], [3, 5], [4, 6], [4, 5], [5, 6], [5, 4], [6, 4]]
    # pagarank(NODES, EDGES, q=0.15, max_iter=3)

    EDGES_TWO = [[1, 6], [2, 1], [2, 3],[2, 5], [4, 4], [5, 5],[6, 2],[3,1],[3,2],[3,3],[3,4],[3,5],[3,6]]
    pagarank(NODES, EDGES_TWO, q=0.2, max_iter=2)


    # td_matrix = [[0, 1, 0, 0, 1],
    #              [0, 1, 0, 0, 1],
    #              [3, 2, 2, 0, 1],
    #              [0, 0, 1, 1, 0],
    #              [0, 0, 1, 1, 1],
    #              [0, 0, 0, 0, 0]]
    #
    # print("TF = ", tf(td_matrix))
    # print("IDF = ", idf(td_matrix))
    # print("TFIDF = ", tf_idf(td_matrix))
    #
    # tq_matrix = [1, 0, 1, 0, 1, 0]  # term query matrix
    # print("TF Query =", tf(tq_matrix))
    # print("document score = ", document_score(td_matrix, tq_matrix))
