import numpy as np
import functools
import multiprocessing
from itertools import product
from .discrete_finite import ibp_model as discrete_model
from .sparse_cont_finite import ibp_model as cont_model

def fit_ibp(x, n_workers = 4, restarts = 4, alpha_values = [1.0, 2.0, 4.0, 8.0], omega_values = [0.1, 0.2, 0.4, 0.8], xi = 1, p = 4, include_intercept = True, use_cont_model = False, stop_threshold = 1e-05, max_iter = 50, min_iter = 30):
    """
    Parameters
    ----------
    x: array
        Matrix of observed data.  Rows are variables and columns are observations.
    n_workers: int, optional
        Number of workers in the pool for parallel processing; should be less than
        or equal to the number of available CPUs.
    restarts: int, optional
        Number of random restarts per set of alpha and omega values.
    alpha_values: array or list of floats, optional
        Parameter of the Indian buffet process.
    omega_values: array or list of floats, optional
        Prior precision of A.
    p: integer, optional
        Number of latent factors used in the finite approximation to the Indian buffet process.
    include_intercept: logical, optional
        If True (default) then an intercept term is included.  If False then it is not.
    use_cont_model: logical, optional
        If False (default) then use the discrete model.  If True then use the sparse continuous model.
    stop_threshold: float, optional
        Relative change in the ELBO at which the optimization should stop.
    max_iter: integer, optional
        Maximum number of iterations to run the optimization.
    min_iter: integer, optional
        Minimum number of iterations to run the optimization.
    """
    model_list = []
    final_elbo = []
    
    with multiprocessing.Pool(n_workers) as pool:
        if use_cont_model:
            fun = functools.partial(__cont_model_fit_wrapper__, x = x, xi = xi, p = p, include_intercept = include_intercept, stop_threshold = stop_threshold, max_iter = max_iter, min_iter = min_iter)
        else:
            fun = functools.partial(__discrete_model_fit_wrapper__, x = x, xi = xi, p = p, include_intercept = include_intercept, stop_threshold = stop_threshold, max_iter = max_iter, min_iter = min_iter)
        alpha_omega_values = n_workers*list(product(alpha_values, omega_values))
        
        results = pool.starmap(fun, alpha_omega_values)
        for result in results:
            model_list += [result]
            final_elbo += [result.elbo_list[-1]]
        
    final_elbo = np.array(final_elbo)
        
    return {'model_list': model_list, 'final_elbo': final_elbo, 'best_model': model_list[final_elbo.argmax()]}

def __discrete_model_fit_wrapper__(alpha, omega, x, xi, p, include_intercept, stop_threshold, max_iter, min_iter):
    """
    Defines a discrete IBP model and fits it to the data, returning the result.
    This is only defined in order to get the parallelization to work.
    """
    new_model = discrete_model(x = x, alpha = alpha, omega = omega, xi = xi, p = p, include_intercept = include_intercept)
    new_model.fit(stop_threshold = stop_threshold, max_iter = max_iter, min_iter = min_iter)
    return new_model
    
def __cont_model_fit_wrapper__(alpha, omega, x, xi, p, include_intercept, stop_threshold, max_iter, min_iter):
    """
    Defines a sparse continuous IBP model and fits it to the data, returning the result.
    This is only defined in order to get the parallelization to work.
    """
    new_model = cont_model(x = x, alpha = alpha, omega = omega, xi = xi, p = p, include_intercept = include_intercept)
    new_model.fit(stop_threshold = stop_threshold, max_iter = max_iter, min_iter = min_iter)
    return new_model