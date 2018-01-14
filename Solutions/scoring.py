import math


def score_bm25(collection, doc, qterms, total_doc, doc_len, avg_doc_len, k1=1.2, b=0.75, base=2):

    s = 0  # holds the retrieval score
    for t in qterms:
        df_t = collection.get(t, 0)
        f_td = doc.get(t, 0)

        w_tq = 1
        idf_t = math.log(total_doc / df_t, base)
        B = 1 - b + b * doc_len / avg_doc_len
        w_td = (f_td * (k1 + 1)) / (f_td + k1 * B) * idf_t
        s += w_tq * w_td
    return s


if __name__ == "__main__":
    total_doc = 1000
    avg_doc_len = 50

    doc1 = {"t1": 3, "t2": 0, "t3": 2, "t4": 1, "t5": 10, "t6": 5}
    doc2 = {"t1": 4, "t2": 3, "t3": 3, "t4": 2, "t5": 1, "t6": 7}

    doc1_len = 21
    doc2_len = 20

    collection = {"t1": 100, "t2": 50, "t3": 80, "t4": 93, "t5": 100, "t6": 25}

    qterms = ["t2", "t2", "t5"]
    bm25_d1 = score_bm25(collection, doc1, qterms, total_doc, doc1_len, avg_doc_len, k1=1.25, b=0.8, base=10)
    bm25_d2 = score_bm25(collection, doc2, qterms, total_doc, doc2_len, avg_doc_len, k1=1.25, b=0.8, base=10)
    print("BM25 for doc1 = ", bm25_d1)
    print("BM25 for doc2 = ", bm25_d2)
