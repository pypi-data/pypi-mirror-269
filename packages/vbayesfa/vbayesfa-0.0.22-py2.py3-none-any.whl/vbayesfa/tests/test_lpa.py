import numpy as np
import pandas as pd
from numpy.testing import *
from vbayesfa.fit_lpa import fit_lpa
from scipy.stats import norm as norm_dist

# to run all tests: pytest /Users/sampaskewitz/Documents/vbayesfa/src/vbayesfa/tests

def _simulate_test_lpa_data():
    # create simple synthetic data
    z = np.array(5*[0, 0, 0, 0, 0, 1, 1, 1, 2, 2]) # profile membership
    n = z.shape[0] # number of participants/observations
    m = 4 # number of observed variables
    mu = np.array(m*[0, 2, -2]).reshape([m, 3]) # profile means
    x = np.zeros([m, n]) # empty array for observed data
    for i in range(n):
        x[:, i] = norm_dist.rvs(loc = mu[:, z[i]], random_state = i) # fill in x
    return x

def test_fit_lpa():
    # create simple synthetic data
    x = _simulate_test_lpa_data()

    # fit the model
    model = fit_lpa(x, T = 20, seed = 1234)['best_model']

    # spot check results
    assert_equal(model.z_hat,
                 np.array([1, 0, 0, 0, 0, 1, 1, 1, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2]))
    assert_almost_equal(model.sorted_m_mu[:,0],
                        np.array([0.28440915, -0.00614277, -0.21887377, -0.39339402]))
    assert_almost_equal(model.sorted_m_mu[:,1],
                        np.array([2.13501792, 1.87225139, 2.12624529, 1.92444134]))
    assert_almost_equal(model.sorted_m_mu[:,2],
                        np.array([-1.82014314, -1.62427792, -2.09733365, -2.02264288]))
    assert_almost_equal(model.E_xi,
                        np.array([1.21540675, 0.93334809, 0.99248329, 0.82400854]))