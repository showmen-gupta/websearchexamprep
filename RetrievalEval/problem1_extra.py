rankings_A = {
    "q1": [1, 2, 6, 5, 9, 10, 7, 4, 8, 3],
    "q2": [1, 2, 4, 5, 7, 10, 8, 3, 9, 6]
}

rankings_B = {
    "q1": [10, 9 , 8, 7, 5, 4, 6, 2, 1, 3],
    "q2": [1, 3, 2, 4, 5, 6, 8, 7, 10, 9]
}

gtruth = {
    "q1": [1, 4, 5],
    "q2": [3, 6]
}

sum_p5, sum_p10, sum_ap, sum_rr = 0, 0, 0, 0
sum_p5B, sum_p10B, sum_apB, sum_rrB = 0, 0, 0, 0

for qid, ranking in sorted(rankings_A.items()):
    gt = gtruth[qid]
    print("Query", qid, "\n\tranking:", ranking, "\n\tground truth:", gt)

    p5, p10, ap, rr, num_rel = 0, 0, 0, 0, 0

    for i, doc_id in enumerate(ranking):
        if doc_id in gt:  # doc is relevant
            num_rel += 1
            pi = num_rel / (i + 1)  # P@i
            ap += pi  # AP

            if i < 5:  # P@5
                p5 += 1
            if i < 10:  # P@10
                p10 += 1
            if rr == 0:  # Reciprocal rank
                rr = 1 / (i + 1)

    p5 /= 5
    p10 /= 10
    ap /= len(gt)  # divide by the number of relevant documents
    print("\tSystem A P@5:", round(p5, 3), "\n\t System A P@10:", round(p10, 3), "\n\tSystem A AP:", round(ap, 3), "\n\tSystem A RR:", round(rr, 3))

    sum_p5 += p5
    sum_p10 += p10
    sum_ap += ap
    sum_rr += rr

print("Average")
print("\tSystem A P@5:", round(sum_p5 / len(rankings_A), 3), "\n\tSystem A P@10:", round(sum_p10 / len(rankings_A), 3),
      "\n\tSystem A MAP:", round(sum_ap / len(rankings_A), 3), "\n\tSystem A MRR:", round(sum_rr / len(rankings_A), 3))


for qid, ranking in sorted(rankings_B.items()):
    gt = gtruth[qid]
    print("Query", qid, "\n\tranking:", ranking, "\n\tground truth:", gt)

    p5, p10, ap, rr, num_rel = 0, 0, 0, 0, 0

    for i, doc_id in enumerate(ranking):
        if doc_id in gt:  # doc is relevant
            num_rel += 1
            pi = num_rel / (i + 1)  # P@i
            ap += pi  # AP

            if i < 5:  # P@5
                p5 += 1
            if i < 10:  # P@10
                p10 += 1
            if rr == 0:  # Reciprocal rank
                rr = 1 / (i + 1)

    p5 /= 5
    p10 /= 10
    ap /= len(gt)  # divide by the number of relevant documents
    print("\tSystem B P@5:", round(p5, 3), "\n\t System B P@10:", round(p10, 3), "\n\tSystem B AP:", round(ap, 3), "\n\tSystem B RR:", round(rr, 3))

    sum_p5B += p5
    sum_p10B += p10
    sum_apB += ap
    sum_rrB += rr

print("Average")
print("\tSystem B P@5:", round(sum_p5B / len(rankings_B), 3), "\n\tSystem B P@10:", round(sum_p10B / len(rankings_B), 3),
      "\n\tSystem B MAP:", round(sum_apB / len(rankings_B), 3), "\n\tSystem B MRR:", round(sum_rrB / len(rankings_B), 3))