from scipy.special import erf


def lab3(data, x_avg, s):
    t = 1.981967489688474
    di_avg = [x_avg - (t * s) / sqrt(SIZE), x_avg + (t * s) / sqrt(SIZE)]
    print(f'DI: {di_avg}')
    di_s = [sqrt(2 * SIZE) / (sqrt(2 * SIZE - 3) + t) * s, sqrt(2 * SIZE) / (sqrt(2 * SIZE - 3) - t) * s]
    print(f'DI: {di_s}')

    z = []
    z.append(-inf)
    for i in range(N_INT - 1):
        z.append((data[i][1] - x_avg) / s)
    z.append(inf)
    print(z)

    phi_fn = lambda x: erf(x / 2 ** 0.5) / 2
    phi = []
    p = []
    for i in range(N_INT):
        phi.append(phi_fn(z[i]))
        p.append(phi_fn(z[i + 1]) - phi_fn(z[i]))
    phi.append(phi_fn(z[7]))
    print(phi)
    print(p)
    p = pd.Series(p)
    n_ = p * SIZE
    print(f'N_: {n_}')
    n = pd.Series([data[i][3] for i in range(N_INT)])
    chi2 = sum((n - n_) ** 2 / n_)
    print(f'chi2: {chi2}')

lab3(male_hist, x_avg_m, s_m)
lab3(female_hist, x_avg_f, s_f)