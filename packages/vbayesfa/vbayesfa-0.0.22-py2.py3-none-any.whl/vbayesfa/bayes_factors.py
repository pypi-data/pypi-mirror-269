import numpy as np
import pandas as pd
from scipy.special import gamma as Gamma
from scipy.integrate import quad
from scipy.linalg import det, inv
from scipy.stats import invgamma
from . import exp_families

def _Helmert_contrast_matrix(p):
    '''
    Create a matrix of Helmert contrast codes for a 1-way ANOVA.
    
    Parameters
    ----------
    p: integer
        Number of factor levels/groups.
    '''
    Q_transpose = np.zeros([p-1, p])
    for i in range(p-1):
        new_row = np.array(i*[0] + [1] + (p-1-i)*[-1/(p-1-i)])
        new_row = new_row/np.sqrt(np.sum(new_row**2))
        Q_transpose[i,:] = new_row
    return Q_transpose.T

def _design_matrix(groups):
    '''
    Turn a "flat" representation of groups in a 1-way ANOVA into a design matrix with dummy variables.
    
    Parameters
    ----------
    groups: array-like
       "Flat" representation of groups/factor levels.
    '''
    n = groups.shape[0] # number of observations
    group_names = np.unique(groups) # names of factor levels
    p = group_names.shape[0] # number of factor levels (does not include the intercept)
    X = np.zeros([n, p])
    for j in range(p):
        X[groups == group_names[j], j] = 1.0
    return X

def _partition(collection):
    '''
    Generate the partitions of a collection.
    
    Parameters
    ----------
    collection: list or similar
        Collection of things to partition.
    
    This is based on the following: https://stackoverflow.com/questions/19368375/set-partitions-in-python
    '''
    if len(collection) == 1:
        yield [ collection ]
        return

    first = collection[0]
    for smaller in _partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset 
        yield [ [ first ] ] + smaller
        
def _remove_nan_groups(y, groups):
    '''
    Convenience function to remove observations with missing data.
    '''
    is_nan = np.isnan(y)
    if np.sum(is_nan) > 0:
        y = y[~is_nan].copy()
        groups = groups[~is_nan].copy()
    return (y, groups)

def _remove_nan_1hot(y, z):
    '''
    Convenience function to remove observations with missing data.
    '''
    is_nan = np.isnan(y)
    if np.sum(is_nan) > 0:
        y = y[~is_nan].copy()
        z = z[:, ~is_nan].copy()
    return (y, z)

def bf10_1way_anova(y, groups, rscale = 0.5, epsrel = 1e-4, limit = 50):
    '''
    Bayes factor vs. the null model for the 1-way fixed effects ANOVA model,
    using JZS priors (not conjugate ones).
    See Equations 8, 13 etc. in the Rouder et al paper.
    
    Parameters
    ----------
    y: array
        Dependent variable array.
    groups: array
        Array (vector) of groups (specified e.g. with character strings).
    rscale: float
        Specifies the width of the inverse gamma distribution on fixed effects.
    epsrel: float, optional
        Relative error tolerance for numerical integration.
    limit: int, optional
        An upper bound on the number of subintervals used in the adaptive algorithm
        for numerical integration.
    
    Returns
    ------
    A tuple containing the Bayes factor (element 0) and numerical integration 
    error (element 1).
    
    Notes
    -----
    
    This uses the following prior distribution:
    
    g ~ InvGamma(0.5, 0.5*rscale^2)
    
    With this interpretation, rscale corresponds to the rscaleFixed parameter
    from the BayesFactor R package. Note that the documentation for that package
    incorrectly specifies that g ~ InvGamma(0.5, 0.5*rscale), i.e. that rscale
    is not squared. I have confirmed that rscale is in fact squared in their
    implementation, so I have also squared rscale here for consistency.
    
    The BayesFactor R package gives the following labels to different values of
    rscale:
    
    1/2 = "medium"
    sqrt(2)/2 = "wide"
    1 = "ultrawide"
    
    I have decided to implement the "medium" size as the default.
    '''
    # remove missing data, if any
    (y, groups) = _remove_nan_groups(y, groups)
    
    # make the design matrix (omitting the intercept term)
    X = _design_matrix(groups)
    n = X.shape[0] # number of participants/observations
            
    # project the design matrix down into a lower subspace
    p = X.shape[1] # number of factor levels
    Q = _Helmert_contrast_matrix(p)
    X_star = X@Q
    
    # define a wrapper function for T_m times the inverse gamma prior on g    
    P0 = np.ones([n, n])/n
    y_tilde = (np.eye(n) - P0)@y
    X_tilde = (np.eye(n) - P0)@X_star
    numerator = y.T@y - n*y.mean()**2
    y_tilde_inner = y_tilde.T@y_tilde
    def _integrand(g):
        G_inv = np.diag(1/np.array((p-1)*[g]))
        det_G = g**(p-1)
        Vg = X_tilde.T@X_tilde + G_inv
        Vg_inv = inv(Vg, check_finite = False)
        denominator = y_tilde_inner - y_tilde.T@X_tilde@Vg_inv@X_tilde.T@y_tilde
        term1 = (numerator/denominator)**(n-1)
        term2 = 1/(det_G*det(Vg, overwrite_a = True, check_finite = False))
        S = (term1*term2)**0.5
        return S*invgamma.pdf(g, a = 0.5, scale = 0.5*rscale**2)
    
    # numerically integrate across g to obtain the marginal likelihood
    return quad(_integrand, a = 0, b = np.inf, epsrel = epsrel, limit = limit)[0]

def partition_posthoc(y, groups, rscale = 0.5, epsrel = 1e-2, limit = 50):
    '''
    Find the best partition of groups/factor levels as a post-hoc analysis
    following a Bayesian 1-way ANOVA.
    
    Parameters
    ----------
    y: array
        Dependent variable array.
    groups: array
        Array (vector) of groups (specified e.g. with character strings).
    rscale: float
        Specifies the width of the inverse gamma distribution on fixed effects.
    epsrel: float, optional
        Relative error tolerance for numerical integration.
    limit: int, optional
        An upper bound on the number of subintervals used in the adaptive algorithm
        for numerical integration.
    
    Returns
    -------
    A dictionary with the following elements:
    
    best_partition:
        The best partition (the one with the highest evidence).
    partition_list:
        List of all partitions.
    evidence:
        The evidence for each partition.
    
    Notes
    -----
    
    ** ADD THIS **
    '''
    # remove missing data, if any
    (y, groups) = _remove_nan_groups(y, groups)
    
    # count things etc.
    n = y.shape[0] # number of observations
    group_names = np.unique(groups) # names of factor levels
    p = group_names.shape[0] # number of factor levels (does not include the intercept)
    
    # list partitions
    partition_list = list(_partition(list(range(p)))) # list of all partitions
    partition_list.pop(0) # remove the initial partition, which has everyone in the same group (H0)
    n_partitions = len(partition_list) # number of partitions
    
    # compute the Bayes factor (vs. the null model) for each partition
    bf = np.zeros(n_partitions) # array for storing each partition's Bayes factor
    for i in range(n_partitions):        
        # create a mapper from the original groups to those based on the current partition        
        mapper = pd.Series(index = group_names)
        for j in range(len(partition_list[i])):
            mapper[partition_list[i][j]] = j
        
        # compute the Bayes factor (vs. the null model) for this partition
        bf[i] = bf10_1way_anova(y, mapper[groups].values, epsrel = epsrel, limit = limit)
        
    return {'best_partition': partition_list[bf.argmax()],
            'partition_list': partition_list,  
            'bf': bf}

def normal_shared_var(y, z, prior_m = 0.0, prior_lambda = 1.0, prior_alpha = 1.0, prior_beta = 1.0):
    '''
    Bayes factor for equality of group means (ANOVA), assuming equal variance across groups.
    This uses a conjugate prior.
    
    Parameters
    ----------
    y: array
        Data.
    z: array
        1-hot encoding of group membership.
    prior_m: float, optional
        Prior m hyperparameter.
    prior_lambda: float, optional
        Prior lambda hyperparameter.
    prior_alpha: float, optional
        Prior alpha hyperparameter.
    prior_beta: float, optional
        Prior beta hyperparameter.
    '''
    (y, z) = _remove_nan_1hot(y, z)
    n_t = z.shape[0] # number of groups
    hpar = {'m': prior_m, 'lambda': prior_lambda, 'alpha': prior_alpha, 'beta': prior_beta} # prior hyperparameters
    H1 = exp_families.multi_group_normal(hpar, n_t)
    H0 = exp_families.normal_gamma_normal(hpar)
    log_bf10 = H1.log_marginal(y, z) - H0.log_marginal(y)
    return np.exp(log_bf10)

def post_normal_shared_var(y, z, prior_m = 0.0, prior_lambda = 1.0, prior_alpha = 1.0, prior_beta = 1.0):
    '''
    Posterior Bayes factor for equality of group means (ANOVA), assuming equal variance across groups.
    This uses a conjugate prior.
    
    Parameters
    ----------
    y: array
        Data.
    z: array
        1-hot encoding of group membership.
    prior_m: float, optional
        Prior m hyperparameter.
    prior_lambda: float, optional
        Prior lambda hyperparameter.
    prior_alpha: float, optional
        Prior alpha hyperparameter.
    prior_beta: float, optional
        Prior beta hyperparameter.
    '''
    (y, z) = _remove_nan_1hot(y, z)
    n_t = z.shape[0] # number of groups
    hpar = {'m': prior_m, 'lambda': prior_lambda, 'alpha': prior_alpha, 'beta': prior_beta} # prior hyperparameters
    H1 = exp_families.multi_group_normal(hpar, n_t)
    H0 = exp_families.normal_gamma_normal(hpar)
    H1.update(y, z)
    H0.update(y)
    log_bf10 = H1.log_marginal(y, z) - H0.log_marginal(y)
    return np.exp(log_bf10)

def frac_normal_shared_var(y, z, prior_m = 0.0, prior_lambda = 1.0, prior_alpha = 1.0, prior_beta = 1.0):
    '''
    Fractional Bayes factor for equality of group means (ANOVA), assuming equal variance across groups.
    This uses a conjugate prior.
    
    Parameters
    ----------
    y: array
        Data.
    z: array
        1-hot encoding of group membership.
    prior_m: float, optional
        Prior m hyperparameter.
    prior_lambda: float, optional
        Prior lambda hyperparameter.
    prior_alpha: float, optional
        Prior alpha hyperparameter.
    prior_beta: float, optional
        Prior beta hyperparameter.
        
    Notes
    -----
    Each group has a different training fraction, determined as 1/sqrt(n), where n is the
    sample size of that group.
    '''
    (y, z) = _remove_nan_1hot(y, z)    
    n_per_group = z.sum(axis = -1)
    z_flat = z.argmax(axis = 0) # encodes group in a single vector (not 1-hot encoding)
    frac = 1/np.sqrt(n_per_group) # different training fractions for each group
    n_t = z.shape[0] # number of groups
    hpar = {'m': prior_m, 'lambda': prior_lambda, 'alpha': prior_alpha, 'beta': prior_beta} # prior hyperparameters
    H1 = exp_families.multi_group_normal(hpar, n_t)
    H0 = exp_families.normal_gamma_normal(hpar)
    log_bf10 = (H1.log_marginal(y, z) - H1.weighted_log_marginal(y, z, weights = frac[z_flat])) - (H0.log_marginal(y) - H0.weighted_log_marginal(y, weights = frac[z_flat]))
    return np.exp(log_bf10)

def normal_dif_var(y, z, prior_m = 0.0, prior_lambda = 1.0, prior_alpha = 1.0, prior_beta = 1.0):
    '''
    Bayes factor for equality of group means (ANOVA), assuming different variances across groups.
    
    Parameters
    ----------
    y: array
        Data.
    z: array
        1-hot encoding of group membership.
    prior_m: float, optional
        Prior m hyperparameter.
    prior_lambda: float, optional
        Prior lambda hyperparameter.
    prior_alpha: float, optional
        Prior alpha hyperparameter.
    prior_beta: float, optional
        Prior beta hyperparameter.
    '''
    (y, z) = _remove_nan_1hot(y, z)
    n_t = z.shape[0] # number of groups
    hpar = {'m': prior_m, 'lambda': prior_lambda, 'alpha': prior_alpha, 'beta': prior_beta} # prior hyperparameters
    H1 = exp_families.multi_group_distribution(exp_families.normal_gamma_normal, hpar, n_t)
    H0 = exp_families.normal_gamma_normal(hpar)
    log_bf10 = H1.log_marginal(y, z) - H0.log_marginal(y)
    return np.exp(log_bf10)

def frac_normal_dif_var(y, z, prior_m = 0.0, prior_lambda = 1.0, prior_alpha = 1.0, prior_beta = 1.0):
    '''
    Fractional Bayes factor for equality of group means (ANOVA), assuming different variances across groups.
    This uses a conjugate prior.
    
    Parameters
    ----------
    y: array
        Data.
    z: array
        1-hot encoding of group membership.
    prior_m: float, optional
        Prior m hyperparameter.
    prior_lambda: float, optional
        Prior lambda hyperparameter.
    prior_alpha: float, optional
        Prior alpha hyperparameter.
    prior_beta: float, optional
        Prior beta hyperparameter.
        
    Notes
    -----
    Each group has a different training fraction, determined as 1/sqrt(n), where n is the
    sample size of that group.
    '''
    (y, z) = _remove_nan_1hot(y, z)
    n_per_group = z.sum(axis = -1)
    z_flat = z.argmax(axis = 0) # encodes group in a single vector (not 1-hot encoding)
    frac = 1/np.sqrt(n_per_group) # different training fractions for each group
    n_t = z.shape[0] # number of groups
    hpar = {'m': prior_m, 'lambda': prior_lambda, 'alpha': prior_alpha, 'beta': prior_beta} # prior hyperparameters
    H1 = exp_families.multi_group_distribution(exp_families.normal_gamma_normal, hpar, n_t)
    H0 = exp_families.normal_gamma_normal(hpar)
    log_bf10 = (H1.log_marginal(y, z) - H1.frac_log_marginal(y, z, frac = frac)) - (H0.log_marginal(y) - H0.weighted_log_marginal(y, weights = frac[z_flat]))
    return np.exp(log_bf10)

def bernoulli(y, z, prior_a = 0.5, prior_b = 0.5):
    '''
    Bayes factor for testing equality of outcome probabilities across groups.
    
    Parameters
    ----------
    y: array
        Data.
    z: array
        1-hot encoding of group membership.
    prior_a: float, optional
        Prior a hyperparameter.
    prior_b: float, optional
        Prior b hyperparameter.
    '''
    (y, z) = _remove_nan_1hot(y, z)
    n_t = z.shape[0] # number of groups
    H1 = exp_families.multi_group_distribution(exp_families.beta_bernoulli, 
                                               {'a': prior_a, 'b': prior_b}, 
                                               n_t)
    H0 = exp_families.beta_bernoulli({'a': prior_a, 'b': prior_b})
    log_bf10 = H1.log_marginal(y, z) - H0.log_marginal(y)
    return np.exp(log_bf10)

def post_bernoulli(y, z, prior_a = 0.5, prior_b = 0.5):
    '''
    Posterior Bayes factor for testing equality of outcome probabilities across groups.
    
    Parameters
    ----------
    y: array
        Data.
    z: array
        1-hot encoding of group membership.
    prior_a: float, optional
        Prior a hyperparameter.
    prior_b: float, optional
        Prior b hyperparameter.
    '''
    (y, z) = _remove_nan_1hot(y, z)
    n_t = z.shape[0] # number of groups
    H1 = exp_families.multi_group_distribution(exp_families.beta_bernoulli, 
                                               {'a': prior_a, 'b': prior_b}, 
                                               n_t)
    H0 = exp_families.beta_bernoulli({'a': prior_a, 'b': prior_b})
    H1.update(y, z)
    H0.update(y)
    log_bf10 = H1.log_marginal(y, z) - H0.log_marginal(y)
    return np.exp(log_bf10)

def frac_bernoulli(y, z, prior_a = 0.5, prior_b = 0.5):
    '''
    Fractional Bayes factor for testing equality of outcome probabilities across groups.
    
    Parameters
    ----------
    y: array
        Data.
    z: array
        1-hot encoding of group membership.
    prior_a: float, optional
        Prior a hyperparameter.
    prior_b: float, optional
        Prior b hyperparameter.
        
    Notes
    -----
    Each group has a different training fraction, determined as 1/sqrt(n), where n is the
    sample size of that group.
    '''
    (y, z) = _remove_nan_1hot(y, z)
    n_per_group = z.sum(axis = -1)
    z_flat = z.argmax(axis = 0) # encodes group in a single vector (not 1-hot encoding)
    frac = 1/np.sqrt(n_per_group) # different training fractions for each group
    n_t = z.shape[0] # number of groups
    H1 = exp_families.multi_group_distribution(exp_families.beta_bernoulli, 
                                               {'a': prior_a, 'b': prior_b}, 
                                               n_t)
    H0 = exp_families.beta_bernoulli({'a': prior_a, 'b': prior_b})
    log_bf10 = (H1.log_marginal(y, z) - H1.frac_log_marginal(y, z, frac = frac)) - (H0.log_marginal(y) - H0.weighted_log_marginal(y, weights = frac[z_flat]))
    return np.exp(log_bf10)