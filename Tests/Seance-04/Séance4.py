#coding:utf8

import numpy as np
import pandas as pd
import scipy
import scipy.stats
from scipy import stats 
import matplotlib.pyplot as plt

#https://docs.scipy.org/doc/scipy/reference/stats.html


dist_names = ['norm', 'beta', 'gamma', 'pareto', 't', 'lognorm', 'invgamma', 'invgauss',  'loggamma', 'alpha', 'chi', 'chi2', 'bradford', 'burr', 'burr12', 'cauchy', 'dweibull', 'erlang', 'expon', 'exponnorm', 'exponweib', 'exponpow', 'f', 'genpareto', 'gausshyper', 'gibrat', 'gompertz', 'gumbel_r', 'pareto', 'pearson3', 'powerlaw', 'triang', 'weibull_min', 'weibull_max', 'bernoulli', 'betabinom', 'betanbinom', 'binom', 'geom', 'hypergeom', 'logser', 'nbinom', 'poisson', 'poisson_binom', 'randint', 'zipf', 'zipfian']

print(dist_names)
dist_names = ['dirac', 'randint', 'binom', 'poisson', 'zipf', 'zipf_mandelbrot']
#écrire la loi de dirac qui n'est pas disponible dans scipy.stats
def pmf_dirac(k, a):
    return np.where(k == a, 1.0, 0.0)
#valable aussi pour la loi de Zipf-Mandelbrot
def pmf_zipf_mandelbrot(k, s, q):
    pmf = 1 / ( (k + q)**s )
    pmf /= pmf.sum()
    return pmf

def plot_discrete_dist(dist_name, **params):
    k = np.arange(params.get("kmin", 0), params.get("kmax", 20) + 1)

    # Dirac
    if dist_name == 'dirac':
        pmf = pmf_dirac(k, params.get("a", 0))

    # Uniforme discrète (scipy.stats.randint)
    elif dist_name == 'randint':
        low = params.get("low", 0)
        high = params.get("high", 10)
        pmf = scipy.stats.randint.pmf(k, low, high)

    # Binomiale B(n,p) (scipy.stats.binom)
    elif dist_name == 'binom':
        n = params.get("n", 10)
        p = params.get("p", 0.5)
        pmf = scipy.stats.binom.pmf(k, n, p)

    # Poisson (scipy.stats.poisson)
    elif dist_name == 'poisson':
        lam = params.get("lam", 4)
        pmf = scipy.stats.poisson.pmf(k, lam)

    # Zipf de scipy (scipy.stats.zipf)
    elif dist_name == 'zipf':
        a = params.get("a", 2)
        pmf = scipy.stats.zipf.pmf(k, a)

    #  Zipf-Mandelbrot (fonction maison) 
    elif dist_name == 'zipf_mandelbrot':
        s = params.get("s", 1.2)
        q = params.get("q", 2)
        pmf = pmf_zipf_mandelbrot(k, s, q)

    else:
        raise ValueError("Distribution inconnue : " + dist_name)

    plt.stem(k, pmf)
    plt.title(dist_name)
    plt.xlabel("k")
    plt.ylabel("P(X=k)")
    plt.grid(True)
    plt.show()

plot_discrete_dist("dirac", a=3, kmin=0, kmax=10)
plot_discrete_dist("randint", low=2, high=10)
plot_discrete_dist("binom", n=20, p=0.4)
plot_discrete_dist("poisson", lam=4)
plot_discrete_dist("zipf", a=1.5)
plot_discrete_dist("zipf_mandelbrot", s=1.2, q=2)

#Variables continues suivantes 

def plot_distribution(dist, params=(), xmin=-5, xmax=5, n=500, discrete=False):
    """
    dist : objet de distribution scipy.stats
    params : paramètres de la distribution
    discrete : True si distribution discrète (Poisson)
    """

    x = np.linspace(xmin, xmax, n)

    plt.figure(figsize=(7, 4))

    if discrete:
        # Pour les distributions discrètes, on utilise le PMF
        k = np.arange(xmin, xmax+1)
        pmf = dist.pmf(k, *params)
        plt.stem(k, pmf)
        plt.title(f"Distribution discrète : {dist.name}")
        plt.xlabel("k")
        plt.ylabel("pmf")
    else:
        # Pour les distributions continues : PDF
        pdf = dist.pdf(x, *params)
        plt.plot(x, pdf, lw=2)
        plt.title(f"Distribution continue : {dist.name}")
        plt.xlabel("x")
        plt.ylabel("pdf")

    plt.grid(True)
    plt.show()


# Loi de Poisson (discrète)
plot_distribution(stats.poisson, params=(5,), xmin=0, xmax=15, discrete=True)

# Loi normale
plot_distribution(stats.norm, params=(0, 1), xmin=-4, xmax=4)

#Loi log-normale
plot_distribution(stats.lognorm, params=(0.5,), xmin=0, xmax=5)

# Loi uniforme
plot_distribution(stats.uniform, params=(0, 1), xmin=0, xmax=1)

# Loi du χ²
plot_distribution(stats.chi2, params=(4,), xmin=0, xmax=15)

# Loi de Pareto
plot_distribution(stats.pareto, params=(3,), xmin=0, xmax=5)

