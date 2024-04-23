import numpy as np
import pandas as pd
from numpy.testing import *
from vbayesfa.fit_lpa import fit_lpa
from vbayesfa.lpa_outcome_analysis import fit_y_normal
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
    y = pd.DataFrame({'var1': norm_dist.rvs(loc = np.array([-2, -2, 1])[z], size = n, random_state = 1234),
                      'var2': norm_dist.rvs(0.0, size = n, random_state = 1234)})
    return x, y

def test_lpa_normal_outcome_analysis():
    # create simple synthetic data
    x, y = _simulate_test_lpa_data()
    
    # fit the model
    model = fit_lpa(x, seed = 1234)['best_model']
    
    # do outcome analysis
    result = fit_y_normal(model, y)
    
    # check results
    assert_almost_equal(result['bayes_factors']['log10_bf10'], np.array([8.308400339407193, -0.7093694320419682]))
    assert_equal(result['bayes_factors']['conclusion'][0], 'profile means differ')
    assert_equal(result['bayes_factors']['conclusion'][1], 'profile means =')
    assert_equal(result['bayes_factors']['post_hoc_result'][0], [[0, 1], [2]])
    assert_equal(result['bayes_factors']['post_hoc_result'][1], np.NaN)
    assert_almost_equal(result['r2'], np.array([0.6425029, 0.0115215]))
    assert_almost_equal(result['post_hpar']['m'], np.array([[-1.85968036, -1.90913725,  1.14785841], [ 0.06339656, -0.03413725,  0.2387675]]))
    assert_almost_equal(result['post_hpar']['lambda'], np.array([[26., 16., 11.], [26., 16., 11.]]))
    assert_almost_equal(result['post_hpar']['beta'], np.array([28.38825005, 23.9553788]))
    
    
# ***** ADD THE BINARY OUTCOME ANALYSIS TEST AT SOME POINT *****
    