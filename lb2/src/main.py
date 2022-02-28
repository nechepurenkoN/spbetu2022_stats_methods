from math import log10, sqrt

import pandas as pd

SIZE = 110
N_INT_FLOAT = 1 + 3.322 * log10(SIZE)
N_INT = int(N_INT_FLOAT)

data = pd.read_csv('https://raw.githubusercontent.com/nechepurenkoN/spbetu2022_stats_methods/master/cropped_sample.csv')
male = data.iloc[:SIZE, 1]
female = data.iloc[:SIZE, 2]

sorted_male = male.sort_values()
sorted_female = female.sort_values()

male_int_width = (sorted_male.iloc[-1] - sorted_male.iloc[0]) / N_INT
female_int_width = (sorted_female.iloc[-1] - sorted_female.iloc[0]) / N_INT


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
    return list(zip(beg, end, avg, count1, count2, pd.Series(count1).cumsum()))


male_hist = intervals(sorted_male, male_int_width)
print('MALE INTERVAL SERIES')
for i in range(N_INT):
    print(
        f'[{round(male_hist[i][0], 2)} {round(male_hist[i][1], 2)}) & {round(male_hist[i][2], 2)} & {round(male_hist[i][3], 2)} & {round(male_hist[i][5], 2)} \\\\\hline')

female_hist = intervals(sorted_female, female_int_width)
print('FEMALE INTERVAL SERIES')
for i in range(N_INT):
    print(
        f'[{round(female_hist[i][0], 2)} {round(female_hist[i][1], 2)}) & {round(female_hist[i][2], 2)} & {round(female_hist[i][3], 2)} & {round(female_hist[i][5], 2)} \\\\\hline')


def cond_moments(data, h):
    x = pd.Series([d[2] for d in data])
    u = pd.Series(list(range(-3, 4)))
    n = pd.Series([d[3] for d in data])
    un = u * n
    u2n = u ** 2 * n
    u3n = u ** 3 * n
    u4n = u ** 4 * n
    u14n = (u + 1) ** 4 * n
    for i in range(N_INT):
        print(f'{x[i]} & {u[i]} & {n[i]} & {un[i]} & {u2n[i]} & {u3n[i]} & {u4n[i]} & {u14n[i]} \\\\\\hline')
    print()
    print(f'{n.sum()} & {un.sum()} & {u2n.sum()} & {u3n.sum()} & {u4n.sum()} & {u14n.sum()} \\\\\\hline')
    print()
    M1 = un.sum() / SIZE
    M2 = u2n.sum() / SIZE
    M3 = u3n.sum() / SIZE
    M4 = u4n.sum() / SIZE
    print(f'{round(M1, 2)} & {round(M2, 2)} & {round(M3, 2)} & {round(M4, 2)} & \\\\\\hline')
    print()
    print("ПРОВЕРКА: ", u4n.sum(), 4 * u3n.sum(), 6 * u2n.sum(), 4 * un.sum(), n.sum())
    print("ПРОВЕРКА: ", u4n.sum() + 4 * u3n.sum() + 6 * u2n.sum() + 4 * un.sum() + n.sum())

    print("Эмпирические моменты")
    mu1 = M1 * h + data[3][2]
    mu2 = (M2 - M1 ** 2) * h ** 2
    mu3 = (M3 - 3 * M2 * M1 + 2 * M1 ** 3) * h ** 3
    mu4 = (M4 - 4 * M3 * M1 + 6 * M2 * M1 ** 2 - 3 * M1 ** 4) * h ** 4

    print(f'mu1 = {mu1}')
    print(f'mu2 = {mu2}')
    print(f'mu3 = {mu3}')
    print(f'mu4 = {mu4}')
    x_avg = M1 * h + x[N_INT // 2]
    print(f'x_avg = {x_avg}')
    print(f'D_v = {mu2}')
    print(f'sigma = {sqrt(mu2)}')
    S2 = SIZE / (SIZE - 1) * mu2
    print(f'S2 = {S2}')
    s = sqrt(S2)
    print(f'S = {s}')
    As = mu3 / s ** 3
    print(f'As = {As}')
    Ex = mu4 / s ** 4
    print(f'Ex = {Ex}')
    print(f'M0 = {data[0][1] + (n[1] - n[0]) / ((n[1] - n[0]) + (n[1] - n[2])) * h}')
    print(f'Me = {data[0][1] + (0.5 * SIZE) / n[1]}')


print('MALE COND MOMENTS')
cond_moments(male_hist, male_int_width)
print('FEMALE COND MOMENTS')
cond_moments(female_hist, male_int_width)
