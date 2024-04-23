import numpy as np
import pandas as pd
from numpy.testing import *
from scipy.stats import beta as beta_dist
from scipy.stats import gamma as gamma_dist
from scipy.stats import norm as norm_dist
from scipy.stats import multivariate_normal, multivariate_t, wishart
from scipy.stats import t as t_dist
from scipy.linalg import inv
from vbayesfa import exp_families as ef

# to run all tests: pytest /Users/sampaskewitz/Documents/vbayesfa/src/vbayesfa/tests

def _assert_dict_almost_equal(dict1, dict2):
    # This is just a convenience function to test equality of the elements of two dicts.
    for key in dict1.keys():
        assert_almost_equal(dict1[key], dict2[key])

def test_normal():
    # define the distribution
    dist = ef.normal_gamma_normal()
    
    # test updating
    y = norm_dist.rvs(size = 4, random_state = 1234) # some data
    dist.update(y)
    assert_almost_equal(list(dist.hpar.values()), # updated hyperparameters from my code
                        [0.0801029082720826, 5.0, 3.0, 2.8794961524616207]) # correct hyperparameters

    # test parameter distribution
    test_par = {'mu': 1.2, 'sigma': 0.39} # some values to test
    scipy_result = norm_dist.logpdf(test_par['mu'], dist.hpar['m'], test_par['sigma']/np.sqrt(dist.hpar['lambda'])) + gamma_dist.logpdf(1/test_par['sigma']**2, a = dist.hpar['alpha'], scale = 1/dist.hpar['beta']) # result from scipy.stats
    our_result = dist.log_density(dist.par_to_theta(test_par))
    assert_almost_equal(our_result, 
                        scipy_result)
    
    # test marginal distribution
    y_new = np.array([-9.0]) # some data value to test
    scipy_log_marginal = t_dist.logpdf(y_new, 
                                       df = 2*dist.hpar['alpha'],
                                       loc = dist.hpar['m'],
                                       scale = np.sqrt(dist.hpar['beta']*(dist.hpar['lambda'] + 1)/(dist.hpar['lambda']*dist.hpar['alpha'])))
    assert_almost_equal(dist.log_marginal(y_new), # result from my code
                        scipy_log_marginal) # result from scipy.stats

    
def test_bernoulli():
    # define the distribution
    dist = ef.beta_bernoulli()
    
    # test updating
    y = np.array([1, 0, 0, 1, 1, 0, 1]) # some data
    dist.update(y)
    assert_almost_equal(list(dist.hpar.values()), # updated hyperparameters from my code
                        [5.0, 4.0]) # correct hyperparameters

    # test parameter distribution
    test_par = {'psi': 0.4} # some value of the parameter to test
    assert_almost_equal(dist.log_density(dist.par_to_theta(test_par)), # result from my code
                        beta_dist.logpdf(test_par['psi'], dist.hpar['a'], dist.hpar['b'])) # result from scipy.stats
    
    # test marginal distribution
    y_new = 1 # some data value to test
    prob = dist.hpar['a']/(dist.hpar['a'] + dist.hpar['b']) # marginal probability that y_new = 1
    assert_almost_equal(dist.log_marginal(np.array([y_new])), # result from my code
                        y_new*np.log(prob) + (1 - y_new)*np.log(1 - prob)) # correct result
    
def test_mvnormal():
    # define the distribution
    dist = ef.mvnormal_Wishart_mvnormal({'m': np.zeros(2),
                                         'lambda': 2,
                                         'V_inv': np.eye(2)})
    
    # test hyperparameter conversion (convert hpar to tau then back to hpar and check that it's the same)
    test_hpar = {'m': np.array([0.3, -1.2]), 
                 'V_inv': inv(np.array([2.0, 0.1, 0.1, 2.0]).reshape([2, 2])), 
                 'lambda': 9}
    _assert_dict_almost_equal(dist.tau_to_hpar(dist.hpar_to_tau(test_hpar)),
                              test_hpar)
    
    # test updating
    n = 5
    y = multivariate_normal.rvs(size = n, cov = inv(np.array([1.0, 0.3, 0.3, 1.0]).reshape([2, 2])), random_state = 1234).T # some data (transposed so that observations are indexed by the last axis)
    ybar = y.mean(axis = -1)
    comparison_updated_hpar = {'m': (dist.hpar['lambda']*dist.hpar['m'] + n*ybar)/(dist.hpar['lambda'] + n),
                              'V_inv': dist.hpar['V_inv'] + np.sum(np.stack([np.outer(y[:,i] - ybar, y[:,i] - ybar) for i in range(n)], axis = -1), axis = -1) + ((dist.hpar['lambda']*n)/(dist.hpar['lambda'] + n))*np.outer(ybar - dist.hpar['m'], ybar - dist.hpar['m']), 
                              'lambda': dist.hpar['lambda'] + n}
    dist.update(y)
    _assert_dict_almost_equal(dist.hpar, # updated hyperparameters from my code
                              comparison_updated_hpar) # correct hyperparameters
    
    # test parameter distribution
    test_par = {'mu': np.array([1.2, -2.0]),
                'Sigma_inv': inv(np.array([2.3, -0.9, -0.9, 2.3]).reshape([2, 2]))} # some values to test
    scipy_result = multivariate_normal.logpdf(test_par['mu'], dist.hpar['m'], inv(test_par['Sigma_inv'])/dist.hpar['lambda']) + wishart.logpdf(test_par['Sigma_inv'], dist.hpar['lambda'] + dist.k, inv(dist.hpar['V_inv']))
    assert_almost_equal(dist.log_density(dist.par_to_theta(test_par)), # our result
                        scipy_result)
    
    # test marginal distribution
    y_new = multivariate_normal.rvs(size = 1, cov = inv(np.array([1.0, 0.3, 0.3, 1.0]).reshape([2, 2])), random_state = 9876).reshape([2, 1]) # some data value to test
    scipy_result = multivariate_t.logpdf(y_new.squeeze(),
                                         loc = dist.hpar['m'], 
                                         shape = dist.hpar['V_inv']/dist.hpar['lambda'],
                                         df = dist.hpar['lambda'] + 1) # from the conjugate prior article, with a little extra algebra
    assert_almost_equal(dist.log_marginal(y_new), # our result
                        scipy_result)
    