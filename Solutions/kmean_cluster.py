import math
import sys
import random
from statistics import mean


def ecludian_distance(p1, p2):
    n = len(p1)
    assert n == len(p2)
    return math.sqrt(sum([pow(p1[i] - p2[i], 2) for i in range(n)]))


def dot_product(p1, p2):
    return sum([a*b for a, b in zip(p1, p2)])


def clustering(points, centroids, sim_measure="ecludian"):
    clusters = []  # each index in clusters will hold the index of centroids
    for p in points:
        min_d = sys.maxsize
        min_c = 0

        max_d = -1 * sys.maxsize
        for i in range(len(centroids)):
            if sim_measure == "ecludian":
                d = ecludian_distance(p, centroids[i])
                print("distance between point {} and centroid {} = {}".format(p, centroids[i], d))
                if d < min_d:
                    min_d = d
                    min_c = i
            else:
                d = dot_product(p, centroids[i])
                print("similarity between point {} and centroid {} = {}".format(p, centroids[i], d))
                if d > max_d:
                    max_d = d
                    min_c = i
        clusters.append(min_c)
    return clusters


def update_centroids(k, points, clusters):
    # First collect the list of points belonging to each cluster
    cpoints = [[] for i in range(k)]  # init list of lists
    for i in range(len(points)):
        c = clusters[i]  # cluster index
        cpoints[c].append(points[i])

    centroids = []
    for c in cpoints:
        avg = map(mean, zip(*c))
        centroids.append(list(avg))
    return centroids

def display_cluster(k, points, clusters):
    cpoints = [[] for i in range(k)]  # init list of lists
    for i in range(len(points)):
        c = clusters[i]  # cluster index
        cpoints[c].append(points[i])
    for i in range(k):
        print("cluster {} = {}".format(i, cpoints[i]))


def k_mean(points, k=2, centriods_init=None, sim_measure="ecludian", num_iter=None):
    centroids = []
    if centriods_init is None:
        for i in range(k):
            j = random.randint(0, len(points))
            centroids.append(points[j])
    else:
        centroids = centriods_init

    print("Initial centroids = ", centroids)
    clusters = [0] * len(points)  # assign all points to one cluster
    iteration = 0
    changed = len(points)

    # Repeat until the cluster assignments change for less than 1% of the data points
    while changed > len(points) * 0.01:
        iteration += 1
        clusters_old = list(clusters)
        clusters = clustering(points, centroids, sim_measure=sim_measure)

        centroids = update_centroids(k, points, clusters)
        print("Iteration = ", iteration)
        print("new centroid = ", centroids)
        display_cluster(k, points, clusters)
        # Count how many points have changed clusters
        changed = 0
        for i in range(len(clusters)):
            if clusters[i] != clusters_old[i]:
                changed += 1

        if num_iter is not None and iteration >= num_iter:
            break


if __name__ == "__main__":
    # points = [[1, 1], [1.5, 2], [3, 4], [5, 7], [3.5, 5], [4.5, 5], [3.5, 4.5]]
    # k = 2
    # centirods_init= [[1, 1], [5, 7]]
    # k_mean(points, k, centriods_init=centirods_init)
    points = [[3, 1, 0, 4], [2, 0, 1.5, 1], [1, 3, 4.5, 5], [2.5, 2.5, 5, 3.5], [6, 3, 2, 0]]
    k = 3
    centroids_init = [[3, 5, 4, 4.5], [1.5, 2.5, 1, 2],[2, 3.5, 1, 0]]
    k_mean(points, k, centroids_init, sim_measure="dotproduct")