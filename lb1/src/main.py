from math import log10

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SIZE = 110
N_INT = int(1 + 3.322 * log10(SIZE))


def pretty_print_by_5(series):
    step = 5
    for i in range(SIZE // step):
        print(*series[i * step: i * step + step].tolist(), sep="\t&\t", end="\t\\\\\\hline\n")


def pretty_print_by_10(series1, series2):
    series1 = series1.tolist()
    series2 = series2.tolist()
    series = list(zip(series1, series2))
    series = [y for x in series for y in x]
    step = 10
    for i in range(SIZE * 2 // step):
        print(*series[i * step:i * step + step], sep=" & ", end="\\\\\\hline\n")


def intervals(series, width):
    beg = []
    end = []
    avg = []
    count1 = []
    count2 = []
    for i_interval in range(N_INT):
        b = series.min() + width * i_interval
        beg.append(b)
        e = series.min() + width * (i_interval + 1)
        end.append(e)
        avg.append((b + e) / 2)
        count1.append(len(series[series.between(b, e)]))
        count2.append(len(series[series.between(b, e)]) / SIZE)
    print(*list(zip([round(num, 3) for num in beg], [round(num, 3) for num in end])), sep="\t")
    print(*[round(num, 3) for num in avg], sep="\t")
    print(*count1, sep="\t")
    print(*[round(num, 3) for num in count2], sep="\t")
    return list(zip(avg, count1, count2))


data = pd.read_csv('https://raw.githubusercontent.com/nechepurenkoN/spbetu2022_stats_methods/master/cropped_sample.csv')
male = data.iloc[:SIZE, 1]
female = data.iloc[:SIZE, 2]

print("ALL")
pretty_print_by_10(male, female)
print("MALE")
pretty_print_by_5(male)
print("FEMALE")
pretty_print_by_5(female)

sorted_male = male.sort_values()
sorted_female = female.sort_values()

print("MALE")
pretty_print_by_5(sorted_male)
print("FEMALE")
pretty_print_by_5(sorted_female)

unique, counts = np.unique(male, return_counts=True)
male_var = pd.DataFrame((unique, counts))
unique, counts = np.unique(female, return_counts=True)
female_var = pd.DataFrame((unique, counts))

print("MALE")
pretty_print_by_10(male_var.iloc[0, :], male_var.iloc[1, :])
print("FEMALE")
pretty_print_by_10(female_var.iloc[0, :], female_var.iloc[1, :])

print(N_INT)

male_int_width = (sorted_male.iloc[-1] - sorted_male.iloc[0]) / N_INT
female_int_width = (sorted_female.iloc[-1] - sorted_female.iloc[0]) / N_INT
print(f"MALE INT WIDTH = {male_int_width}")
print(f"FEMALE INT WIDTH = {female_int_width}")


def histograms(sorted_series, int_width, color):
    hist = intervals(sorted_series, int_width)
    plt.plot([str(round(x[0], 2)) for x in hist], [x[1] for x in hist], c=color)
    plt.grid(True)
    plt.xlabel("Середина интервала")
    plt.ylabel("Частота")
    plt.title
    plt.show()
    plt.plot([str(round(x[0], 2)) for x in hist], [x[2] for x in hist], c=color)
    plt.grid(True)
    plt.xlabel("Середина интервала")
    plt.ylabel("Частота")
    plt.show()
    plt.bar([str(round(x[0], 2)) for x in hist], [x[1] for x in hist], color=color)
    plt.grid(axis="y")
    plt.xlabel("Середина интервала")
    plt.ylabel("Частота")
    plt.show()
    plt.bar([str(round(x[0], 2)) for x in hist], [x[2] for x in hist], color=color)
    plt.grid(axis="y")
    plt.xlabel("Середина интервала")
    plt.ylabel("Частота")
    plt.show()
    hist, edges = np.histogram(sorted_series, bins=N_INT)
    Y = hist.cumsum() / SIZE
    for i in range(len(Y)):
        plt.plot([edges[i], edges[i + 1]], [Y[i], Y[i]], c=color)
    for i in range(len(Y) - 1):
        plt.plot([edges[i + 1], edges[i + 1]], [Y[i], Y[i + 1]], c=color, ls=":")
    plt.grid()
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.show()


histograms(sorted_male, male_int_width, "blue")
histograms(sorted_female, female_int_width, "#ff00ee")
