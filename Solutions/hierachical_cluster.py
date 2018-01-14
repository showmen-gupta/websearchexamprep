import sys
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
import numpy as np

def closest(prox):
    min_dist = sys.maxsize
    best_c1 = 0
    best_c2 = 0
    for i in range(len(prox)):
        for j in range(len(prox)):
            if 0 < prox[i][j] < min_dist:
                min_dist = prox[i][j]
                best_c1 = i
                best_c2 = j
    return best_c1, best_c2, min_dist


def cdist(dist, c1, c2, linkage):
    """

    :param dist: distance matric
    :param c1: list of data points in cluster 1
    :param c2: list of data points in cluster 2
    :param linkage: min, max or avg
    :return:
    """
    d = 0
    if len(c1) > 0 and len(c2) > 0:  # only if both clusters are non-empty
        if linkage == "min":
            d = sys.maxsize
            for i1 in c1:
                for i2 in c2:
                    if dist[i1][i2] < d:
                        d = dist[i1][i2]
        if linkage == "max":
            d = 0
            for i1 in c1:
                for i2 in c2:
                    if dist[i1][i2] > d:
                        d = dist[i1][i2]
        if linkage == "avg":
            sum = 0
            num = 0
            for i1 in c1:
                for i2 in c2:
                    if dist[i1][i2] > d:
                        sum += dist[i1][i2]
                        num += 1
            d = sum / num if num > 0 else 0
    return d


def hac(nodes, dist, linkage):
    # Clusters are represented as a list of data points belonging to that cluster
    clusters = []
    # Each data point is a singleton cluster initially
    for i in range(len(dist)):
        clusters.append([i])

    # Compute initial promiximity matrix
    prox = []
    for c1 in clusters:
        c1dist = []  # the row in the proximity matrix corresponding to cluster 1
        for c2 in clusters:
            c1dist.append(cdist(dist, c1, c2, linkage))
        prox.append(c1dist)

    linkages = []

    # Repeat until only one cluster remains
    num = len(clusters)
    while num > 1:
        # Find the closest two clusters
        c1, c2, min_dist = closest(prox)
        print("merged {} and {}".format( nodes[c1], nodes[c2]))
        nodes.append(nodes[c1]+","+nodes[c2])
        # Merge the closest two clusters
        clusters.append(clusters[c1] + clusters[c2])
        # "empty" the clusters that are being merged
        clusters[c1] = []
        clusters[c2] = []

        # Update the proximity matrix
        # Zero out the rows and columns corresponding to the old clusters (that are being merged)
        for i in range(len(prox)):
            prox[i][c1] = 0
            prox[i][c2] = 0
            prox[c1][i] = 0
            prox[c2][i] = 0

        # Add new column and row corresponding to the new cluster
        cnew = len(clusters) - 1  # index of the new matrix
        cnewdist = []  # the row in the proximity matrix corresponding to the new cluster
        for i in range(cnew):
            d = cdist(dist, clusters[i], clusters[cnew], linkage)
            prox[i].append(d)  # append column to row i
            cnewdist.append(d)
            # append new row to proximity matrix
        prox.append(cnewdist + [0])  # distance from itself is 0 by definition

        linkages.append([c1, c2, min_dist, len(clusters[cnew])])
        num -= 1

        # Return the linkages for visualization
    return linkages


if __name__ == "__main__":
    cities = ["BOS", "NY", "DC", "MIA", "CHI", "SEA", "SF", "LA", "DEN"]
    dist = [[0, 206, 429, 1504, 963, 2976, 3095, 2979, 1949], [206, 0, 233, 1308, 802, 2815, 2934, 2786, 1771],
            [429, 233, 0, 1075, 671, 2684, 2799, 2631, 1616], [1504, 1308, 1075, 0, 1329, 3273, 3053, 2687, 2037],
            [963, 802, 671, 1329, 0, 2013, 2142, 2054, 996], [2976, 2815, 2684, 3273, 2013, 0, 808, 1131, 1307],
            [3095, 2934, 2799, 3053, 2142, 808, 0, 379, 1235], [2979, 2786, 2631, 2687, 2054, 1131, 379, 0, 1059],
            [1949, 1771, 1616, 2037, 996, 1307, 1235, 1059, 0]]
    hac(cities, dist, "min")

    linkages_min = hac(cities, dist, "min")

    linkage_matrix = np.array(linkages_min)
    plt.clf()
    plt.title("Single link (min)")
    dendrogram(linkage_matrix.astype(float),
               color_threshold=1,
               labels=cities,
               show_leaf_counts=True)
    plt.show()
