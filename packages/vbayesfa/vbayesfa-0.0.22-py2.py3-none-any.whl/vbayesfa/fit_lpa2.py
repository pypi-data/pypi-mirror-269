import numpy as np
import functools
import multiprocessing
from .fit_finite_lpa import fit_finite_lpa
from .lpa import lpa_model
from time import perf_counter

def fit_lpa2(x, n_workers = 4, restarts = 4, T = 20, prior_w1 = 3.0, prior_w2 = 1.0, prior_lambda_mu = 0.5, prior_strength_for_xi = 10.0, seed = 1234, tolerance = 1e-05, max_iter = 50, min_iter = 30):
    """
    Fit a Dirichlet process latent profile analysis (DPM-LPA) model using mean field
    variational Bayes.
    
    This version of the function fits finite LPA models first to provide starting points
    for DPM-LPA of varying sizes.
    
    Parameters
    ----------
    x: data frame or array
        Observed data (data frame or matrix).  If a matrix then rows are variables and columns
        are observations; if a data frame then rows are observations and columns are variables.
    n_workers: int, optional
        Number of workers in the pool for parallel processing; should be less than
        or equal to the number of available CPUs.
    restarts: int, optional
        Number of random restarts for finite LPA models.
    T: integer, optional
        Truncation level of the variational approximation.
    prior_w1: float, optional
        First prior hyperparameter on alpha.
    prior_w2: float, optional
        Second prior hyperparameter on alpha.
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
    This creates multiple lpa_model objects from the lpa.py module and fits them with using parallel
    processing. See the documentation for the lpa_model object for more details.
    """
    finite_fits = fit_finite_lpa(x, T_range = np.arange(2, T + 1), prior_alpha_pi = 0.5, prior_lambda_mu = prior_lambda_mu, prior_strength_for_xi = prior_strength_for_xi, restarts = restarts, seed = seed)
    phi_list = [finite_fits.loc[Tval, 'best_model'].phi for Tval in np.arange(2, T + 1)]
    model_list = []
    final_elbo = []
    
    with multiprocessing.Pool(n_workers) as pool:
        fun = functools.partial(_model_fit_wrapper, x = x, T = T, prior_w1 = prior_w1, prior_w2 = prior_w2, prior_lambda_mu = prior_lambda_mu, prior_strength_for_xi = prior_strength_for_xi, tolerance = tolerance, max_iter = max_iter, min_iter = min_iter)        
        results = pool.map(fun, phi_list)
    for result in results:
        model_list += [result]
        final_elbo += [result.elbo_list[-1]]
        
    final_elbo = np.array(final_elbo)
    
    return {'final_elbo': final_elbo, 'model_list': model_list, 'best_model': model_list[final_elbo.argmax()]}

    
def _model_fit_wrapper(phi, x, T, prior_w1, prior_w2, prior_lambda_mu, prior_strength_for_xi, tolerance, max_iter, min_iter):
    """
    Defines an LPA model and fits it to the data, returning the result.
    This function is only defined in order to get the parallelization to work.
    """
    new_model = lpa_model(x = x, phi = phi, T = T, prior_w1 = prior_w1, prior_w2 = prior_w2, prior_lambda_mu = prior_lambda_mu, prior_strength_for_xi = prior_strength_for_xi, seed = None)
    new_model.fit(tolerance = tolerance, max_iter = max_iter, min_iter = min_iter)
    return new_model