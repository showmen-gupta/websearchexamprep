import math


def percentile(x, k):
    sorted_x = sorted(x)
    n = len(x) * k/100
    n = round(n+0.5)
    n = int(n)
    return sorted_x[n]


def mean(x):
    return sum(x) / len(x)


def median(x):
    sorted_x = sorted(x)
    l = len(x)
    m = l // 2
    if l%2 == 0:
        return (sorted_x[m-1] + sorted_x[m]) / 2
    else:
        return sorted_x[m]


def range_of(x):
    return max(x) - min(x)


def variance(x):
    m = mean(x)
    return sum([pow(i - m, 2) for i in x]) / (len(x))


def standard_deviation(x):
    v = variance(x)
    return math.sqrt(v)


def aad(x):
    m = mean(x)
    return sum([abs(i-m) for i in x]) / len(x)


AAD = aad


def mad(x):
    m = mean(x)
    return median([abs(i - m) for i in x])


MAD = mad


def iqr(x):
    x25 = percentile(x, 25)
    x75 = percentile(x, 75)
    return x75 - x25


IQR = iqr
interquartile_range = iqr


def gaussian_distri(d, c):
    """
    :param d: list of continuous data
    :return:
    """
    m = mean(d)
    v = variance(d)
    sd = standard_deviation(d)
    return (1/math.sqrt(2*math.pi*v)) * math.exp(-(pow(c - m, 2))/(2 * v))

if __name__ == "__main__":

    # Temp_y = [83, 70, 68, 64, 69, 75, 75, 72, 81]
    # Temp_n = [85, 80, 65, 72, 71]
    # print("Mean Yes = ", mean(Temp_y))
    # print("Variance Yes = ", variance(Temp_y))
    # print("Mean No = ", mean(Temp_n))
    # print("Variance NO = ", variance(Temp_n))
    #
    # Humi_y = [78, 96, 80, 65, 70, 80, 70, 90, 75]
    # Humi_n = [85, 90, 70, 95, 80]
    # print("Mean Yes = ", mean(Humi_y))
    # print("Variance Yes = ", variance(Humi_y))
    # print("Mean No = ", mean(Humi_n))
    # print("Variance NO = ", variance(Humi_n))
    #
    # print("Temp = 87 | yes = ", gaussian_distri(Temp_y, 87))
    # print("Humi = 90 | yes = ", gaussian_distri(Humi_y, 90))

    # t11 = [1, 1]
    # t12 = [0, 0]
    # t13 = [3, 0, 0, 1]
    #
    # x= [2,5,-1,3,4,5,0,2]
    # y = [2, 5, -1, 3, 50, 5, 0, 2]
    #
    # print(mean(x))
    # print(variance(x))
    # print(mean(y))
    # print(variance(y))
    # print(aad(x))
    # print(aad(y))
    # print(mad(x))
    # print(mad(y))
    #
    # print(iqr(x))
    # print(iqr(y))


    z= [17,5,3,9,49,53,11]
    print(range_of(z))
    print(median(z))
    print(mean(z))
    print(variance(z))
    print(aad(z))

    # print(mean(t11))
    # print(variance(t11))
    # print(mean(t12))
    # print(variance(t12))
    # print(mean(t13))
    # print(variance(t13))



