import math


rankings = {
    "q1": [10, 7, 9, 8, 2, 1, 3, 4, 5, 6],
    "q2": [3, 2, 1, 4, 5, 7, 8, 10, 9, 6],

}

gtruth = {
    "q1": {10:0,7: 3, 9:0, 8:0, 2: 2, 1: 3, 3:1, 4:0, 5:0, 6:0},
    "q2": {3:1, 2:2, 1:3, 4:0, 5:0, 7:3, 8:0, 10:0, 9:0, 6:0},
}

def dcg(rel, p):
    dcg = rel[0]
    for i in range(1, min(p, len(rel))):
        dcg += rel[i] / math.log(i + 1, 2)  # rank position is indexed from 1..
    return dcg


sum_ndcg5 = 0
sum_ndcg10 = 0

for qid, ranking in sorted(rankings.items()):
    gt = gtruth[qid]
    print("Query", qid)

    gains = []  # holds corresponding relevance levels for the ranked docs
    for doc_id in ranking:
        gain = gt.get(doc_id, 0)
        gains.append(gain)
    print("\tGains:", gains)

    # relevance levels of the idealized ranking
    gain_ideal = sorted([v for _, v in gt.items()], reverse=True)
    print("\tIdeal gains:", gain_ideal)
    print(dcg(gain_ideal, 5))
    print(dcg(gain_ideal, 10))
    ndcg5 = dcg(gains, 5) / dcg(gain_ideal, 5)
    ndcg10 = dcg(gains, 10) / dcg(gain_ideal, 10)
    sum_ndcg5 += ndcg5
    sum_ndcg10 += ndcg10

    print("\tNDCG@5:", round(ndcg5, 3), "\n\tNDCG@10:", round(ndcg10, 3))
    print("\tDCG@5:", round(dcg(gain_ideal, 5), 3), "\n\tDCG@10:", round(dcg(gain_ideal, 10), 3))

print("Average")
print("\tNDCG@5:", round(sum_ndcg5 / len(rankings), 3), "\n\tNDCG@10:", round(sum_ndcg10 / len(rankings), 3))
