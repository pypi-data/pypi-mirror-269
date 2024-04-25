import numpy as np
import pandas as pd
import functools
import multiprocessing
from .finite_lpa import finite_lpa_model
from time import perf_counter

def fit_finite_lpa(x, n_workers = 4, restarts = 10, T_range = np.arange(2, 11), prior_alpha_pi = 1.0, prior_lambda_mu = 0.5, prior_strength_for_xi = 10.0, seed = 1234, tolerance = 1e-05, max_iter = 50, min_iter = 30):
    """
    Fit series of finite latent profile analysis (DPM-LPA) models of different sizes (number of profile, T)
    using mean field variational Bayes.
    
    Parameters
    ----------
    x: data frame or array
        Observed data (data frame or matrix).  If a matrix then rows are variables and columns
        are observations; if a data frame then rows are observations and columns are variables.
    n_workers: int, optional
        Number of workers in the pool for parallel processing; should be less than
        or equal to the number of available CPUs.
    restarts: int, optional
        Number of random restarts per value of T (number of latent profiles).
    T_range: array of integers, optional
        Range of values of T (number of latent profiles) to fit.
    prior_alpha_pi: float, optional
        Prior strength of the Dirichlet prior distribution on pi.
    prior_lambda_mu: float, optional
        Controls the width of the prior distribution on mu: 
        higher values -> tighter prior around 0.
    prior_strength_for_xi: float, optional
        Controls the strength of the gamma prior distribution on xi.
        This prior is assumed to have a mean of 1, with alpha = prior_strength_for_xi/2
        and beta = prior_strength_for_xi/2.
    seed: int, optional
        Random seed (determines starting conditions of each optimization).
    tolerance: float, optional
        Relative change in the ELBO at which the optimization should stop.
    max_iter: integer, optional
        Maximum number of iterations to run the optimization.
    min_iter: integer, optional
        Minimum number of iterations to run the optimization.
        
    Notes
    -----
    This creates multiple finite_lpa_model objects from the finite_lpa.py module and fits them with using parallel
    processing. See the documentation for the lpa_model object for more details.
    """
    tic = perf_counter()
    # set up an empty data frame to hold results
    n_T = T_range.shape[0]
    all_results = pd.DataFrame({'final_elbo': n_T*[0.0], 'best_model': n_T*[np.nan]}, index = pd.Index(T_range, name = 'T'))
    
    # generate random seeds for each model based on the seed parameter
    seed_list = []
    rng = np.random.default_rng(seed)
    for i in range(restarts):
        seed_list += [rng.integers(low = 1000, high = 9999)]
    
    # loop through values of T (number of latent profiles)
    for T in T_range:
        model_list = []
        final_elbo = []

        with multiprocessing.Pool(n_workers) as pool:
            fun = functools.partial(__model_fit_wrapper__, x = x, T = T, prior_alpha_pi = prior_alpha_pi, prior_lambda_mu = prior_lambda_mu, prior_strength_for_xi = prior_strength_for_xi, tolerance = tolerance, max_iter = max_iter, min_iter = min_iter)
            results = pool.map(fun, seed_list)
            for result in results:
                model_list += [result]
                final_elbo += [result.elbo_list[-1]]

        all_results.loc[T, 'final_elbo'] = np.array(final_elbo).max()
        all_results.loc[T, 'best_model'] = model_list[np.array(final_elbo).argmax()]
    
    toc = perf_counter()
    print(f"Fit in {toc - tic:0.4f} seconds.")
    
    return all_results

def __model_fit_wrapper__(seed, x, T, prior_alpha_pi, prior_lambda_mu, prior_strength_for_xi, tolerance, max_iter, min_iter):
    """
    Defines a finite LPA model and fits it to the data, returning the result.
    This function is only defined in order to get the parallelization to work.
    """
    new_model = finite_lpa_model(x = x, T = T, prior_alpha_pi = prior_alpha_pi, prior_lambda_mu = prior_lambda_mu, prior_strength_for_xi = prior_strength_for_xi, seed = seed)
    new_model.fit(tolerance = tolerance, max_iter = max_iter, min_iter = min_iter)
    return new_model