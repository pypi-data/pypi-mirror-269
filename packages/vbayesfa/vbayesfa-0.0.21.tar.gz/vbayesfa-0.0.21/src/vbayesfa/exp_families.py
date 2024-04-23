import numpy as np
import pandas as pd
from scipy.special import betaln, gammaln, multigammaln
from scipy.linalg import inv, det

# These classes are somewhat similar in spirit to this: https://pythonhosted.org/infpy/infpy.exp.html
# I used 1-indexing in the doc, so I'm using pseudo 1-indexing here to avoid mistakes in transcribing the math into Python.

class distribution:
    '''
    Class for exponential family probability distributions.
    
    Notes
    -----
    The LAST axis in each data array etc. indicate observation. This is the opposite
    of many applications.
    
    Here is a summary of the notation conventions used.
    
    natural parameters (of the likelihood): :math:`\theta = \theta_1, \ldots, \theta_p`
    data point: :math:`y_i`
    number of natural parameters (of the likelihood): :math:`p`
    number of data points: :math:`n`
    prior natural hyperparameters: :math:`\tau = \tau_1, \ldots, \tau_p, \tau_{p+1}`
    sufficient statistics: :math:`T(y_i) = T_1(y_i), \ldots, T_p(y_i)`
    posterior natural hyperparameters: :math:`\tau' = \tau_1 + \sum_{i=1}^n T_1(y_i), \ldots, \tau_p + \sum_{i=1}^n T_p(y_i), \tau_{p+1} + n`
    
    Likelihood
    .. math::
    p(y_i | \theta) = \exp\Big( \sum_{j=1}^p \ip{\theta_j, T_j(y_i)} - f(y_i) - g(\theta) \Big) \quad \quad i = 1, 2, \ldots, n
    
    Prior
    .. math::
    p(\theta) = \exp\Big( \sum_{j=1}^p \ip{\tau_j, \theta_j} - \tau_{p+1} g(\theta) - h(\tau) \Big)
    
    Posterior
    .. math::
    p(\theta | y_1, \ldots, y_n) = \exp\Big( \sum_{j=1}^p \ip{\tau_j + \sum_{i=1}^n T_j(y_i), \theta_j} - (\tau_{p+1} + n) g(\theta) - h\big(\tau'(y_1, \ldots, y_n)\big) \Big)
    '''
        
    def tau_prime(self, y):
        '''
        Hyperparameters (tau) plus sufficient statistics of data (T(y)).
        
        Parameters
        ----------
        y: array
            Data.
        '''
        T = self.T(y)
        n = y.shape[-1]
        return [self.tau[j] + np.sum(T[j], axis = -1) for j in range(self.p)] + [self.tau[self.p] + n]
    
    def weighted_tau_prime(self, y, weights):
        '''
        Hyperparameters (tau) plus sufficient statistics of data (T(y)), where each observation
        has a weight.
        
        Parameters
        ----------
        y: array
            Data.
            
        weights: array
            Vector of weights for each data point. Each should be in the range [0, 1].
        '''
        T = self.T(y)
        n = np.sum(weights)
        return [self.tau[j] + np.sum(weights*T[j], axis = -1) for j in range(self.p)] + [self.tau[self.p] + n]    
    
    def update(self, y, weights = None):
        '''
        Update hyperparameters (tau) with data (y).
        
        Parameters
        ----------
        y: array
            Data.
        weights: array, optional
            Vector of weights for each data point. Each should be in the range [0, 1].
            Defaults to None.
        '''
        if weights is None:
            self.tau = self.tau_prime(y)
        else:
            self.tau = self.weighted_tau_prime(y, weights)
        self.hpar = self.tau_to_hpar(self.tau)
    
    def log_density(self, theta):
        '''
        The log-density of parameters (theta) given current hyperparameters (tau).
        
        Parameters
        ----------
        theta: list
            Distribution parameters (in natural form).
        '''
        return np.sum([np.sum(self.tau[j]*theta[j]) for j in range(self.p)]) - self.tau[self.p]*self.g(theta) - self.h(self.tau)
        
    def density(self, theta):
        '''
        The density of parameters (theta) given current hyperparameters (tau).
        
        Parameters
        ----------
        theta: list
            Distribution parameters (in natural form).
        '''
        return np.exp(self.log_density(theta))
    
    def log_marginal(self, y):
        '''
        The log of the marginal likelihood of data.
        
        Parameters
        ----------
        y: array
            Data.
        '''
        return -np.sum(self.f(y)) - self.h(self.tau, False) + self.h(self.tau_prime(y), False)            
        
    def weighted_log_marginal(self, y, weights):
        '''
        The log-marginal with each data point given a weight.
        
        Parameters
        ----------
        y: array
            Data.
        weights: array
            Vector of weights for each data point. Each should be in the range [0, 1].
        '''
        return -np.sum(weights*self.f(y)) - self.h(self.tau, False) + self.h(self.weighted_tau_prime(y, weights), False)
    
    def frac_log_marginal(self, y, frac):
        '''
        The log-marginal with each data point given the same weight.
        Used in computing fractional Bayes factors.
        
        Parameters
        ----------
        y: array
            Data.
        frac: numeric
            Weighting fraction used for all data points. Should be in the range [0, 1].
        '''
        n = y.shape[-1]
        return self.weighted_log_marginal(y = y, weights = frac*np.ones(n))
    
    def marginal(self, y):
        '''
        The marginal likelihood of data.
        
        Parameters
        ----------
        y: array
            Data.
        '''
        return np.exp(self.log_marginal(y))
    
    def entropy(self):
        '''
        The entropy of the distribution over theta.
        
        Notes
        -----
        .. math::
        \text{entropy} = -E[\log p(\theta)] = -\sum_{j=1}^p \ip{\tau_j, E[\theta_j]} + \tau_{p+1} E[g(\theta)] + h(\tau)
        '''
        return -np.sum([np.sum(self.tau[j]*self.E_theta()[j]) for j in range(self.p)]) + self.tau[self.p]*self.E_g_theta() + self.h(self.tau)
        

class multi_group_distribution:
    '''
    Class for a collection exponential family distributions of the same type with different
    parameters for different groups of observations.
    
    Notes
    -----
    This assumes no shared parameter (e.g. variance/precision) across groups.
    
    z gives the 1-hot encoding of each observation's group (row = group, column = observation).
    
    I should revise __init__ in the future to allow the groups to have different starting hyperparameters.
    '''
    
    def __init__(self, base_dist, hpar, n_t):
        '''
        Parameters
        ----------
        base_dist: distribution
            The distribution class.
        hpar: dict
            Initial hyperparameters (the same for each group).
            Specified in conventional form.
        n_t: integer
            Number of groups.
        '''
        self.n_t = n_t
        self.dists = []
        for t in range(self.n_t):
            self.dists += [base_dist(hpar)]
        self.tau = [self.dists[t].tau for t in range(self.n_t)]
        self.hpar = [self.dists[t].hpar for t in range(self.n_t)]
        
    def hpar_table(self):
        '''
        Put all of the (conventional) hyperparameters in a table (Pandas data frame).
        '''
        hpar_names = list(self.dists[0].hpar.keys())
        table = pd.DataFrame(0.0, index = range(self.n_t), columns = hpar_names)
        for t in range(self.n_t):
            for hpar_name in hpar_names:
                table.loc[t, hpar_name] = self.dists[t].hpar[hpar_name]
        return table
        
    def update(self, y, z):
        '''
        Update hyperparameters (tau) with data (y).
        
        Parameters
        ----------
        y: array
            Data.
        z: array
            1-hot encoding of group membership.
        '''
        for t in range(self.n_t):
            self.dists[t].update(y, weights = z[t,:])
            self.tau[t] = self.dists[t].tau
            self.hpar[t] = self.dists[t].hpar
            
    def log_density(self, theta):
        '''
        The log-density of parameters (theta) given current hyperparameters (tau).
        
        Parameters
        ----------
        theta: list of lists
            Each i-th element of the list is another list representing the
            parameters (in natural form) of the i-th group's distribution.
        '''
        return np.sum([self.dists[t].log_density(theta[t]) for t in range(self.n_t)])
    
    def density(self, theta):
        '''
        The density of parameters (theta) given current hyperparameters (tau).
        
        Parameters
        ----------
        theta: list of lists
            Each i-th element of the list is another list representing the
            parameters (in natural form) of the i-th group's distribution.
        '''
        return np.exp(self.log_density(theta))
    
    def log_marginal(self, y, z):
        '''
        The log of the marginal likelihood of data.
        
        Parameters
        ----------
        y: array
            Data.
        z: array
            1-hot encoding of group membership.
        '''
        z_flat = z.argmax(axis = 0) # encodes group in a single vector (not 1-hot encoding)
        return np.sum([self.dists[t].log_marginal(y[z_flat == t]) for t in range(self.n_t)])
    
    def frac_log_marginal(self, y, z, frac):
        '''
        The log-marginal with each data point given the same weight.
        Used in computing fractional Bayes factors.
        
        Parameters
        ----------
        y: array
            Data.
        z: array
            1-hot encoding of group membership.
        frac: numeric
            Weighting fraction used for all data points. Should be in the range [0, 1].
        '''
        return np.sum([self.dists[t].weighted_log_marginal(y, weights = frac[t]*z[t,:]) for t in range(self.n_t)])
    
    def marginal(self, y, z):
        '''
        The marginal likelihood of data.
        
        Parameters
        ----------
        y: array
            Data.
        z: array
            1-hot encoding of group membership.
        '''
        return np.exp(self.log_marginal(y, z))
    
class distribution_with_predictor:
    '''
    Class for exponential familiy distributions with a predictor variable.
    
    Notes
    -----
    It is assumed that the last axis in T, z, S(z) etc. represents individual observations, e.g. participants.
    Thus, np.sum(T[j], axis = -1) takes the sum across observations.
    '''
        
    def tau_prime(self, y, z):
        '''
        Hyperparameters (tau) plus sufficient statistics of data (T(y, z)).
        
        Parameters
        ----------
        y: array
            Data.
        z: array
            Predictor variables.
        '''
        T = self.T(y, z)
        n = y.shape[-1]
        return [self.tau[j] + np.sum(T[j], axis = -1) for j in range(self.p)] + [self.tau[self.p] + n, self.tau[self.p + 1] + np.sum(self.S(z), axis = -1)]
    
    def weighted_tau_prime(self, y, z, weights):
        '''
        Hyperparameters (tau) plus sufficient statistics of data (T(y, z)), where each observation
        has a weight.
        
        Parameters
        ----------
        y: array
            Data.
        z: array
            Predictor variables.
        weights: array
            Vector of weights for each data point. Each should be in the range [0, 1].
        '''
        T = self.T(y, z)
        n = np.sum(weights)
        return [self.tau[j] + np.sum(weights*T[j], axis = -1) for j in range(self.p)] + [self.tau[self.p] + n, self.tau[self.p + 1] + np.sum(weights*self.S(z), axis = -1)] 
    
    def update(self, y, z):
        '''
        Update hyperparameters (tau) with data (y) and predictor variables (z).
        
        Parameters
        ----------
        y: array
            Data.
        z: array
            Predictor variables.
        '''
        self.tau = self.tau_prime(y, z)
        self.hpar = self.tau_to_hpar(self.tau)
    
    def log_density(self, theta):
        '''
        The log-density of parameters (theta) given current hyperparameters (tau).
        
        Parameters
        ----------
        theta: list
            Distribution parameters (in natural form).
        '''
        return np.sum([np.sum(self.tau[j]*theta[j]) for j in range(self.p)]) - self.tau[self.p]*self.g(theta) - np.sum(self.tau[self.p + 1]*self.k(theta)) - self.h(self.tau)
        
    def density(self, theta):
        '''
        The density of parameters (theta) given current hyperparameters (tau).
        
        Parameters
        ----------
        theta: list
            Distribution parameters (in natural form).
        '''
        return np.exp(self.log_density(theta))
    
    def log_marginal(self, y, z):
        '''
        The log of the marginal likelihood of data.
        
        Parameters
        ----------
        y: array
            Data.
        z: array
            Predictor variables.
        '''
        return -np.sum(self.f(y)) - self.h(self.tau, False) + self.h(self.tau_prime(y, z), False)
    
    def weighted_log_marginal(self, y, z, weights):
        '''
        The log-marginal with each data point given a weight.
        
        Parameters
        ----------
        y: array
            Data.
        z: array
            Predictor variables.
        weights: array
            Vector of weights for each data point. Each should be in the range [0, 1].
        '''
        return -np.sum(weights*self.f(y)) - self.h(self.tau, False) + self.h(self.weighted_tau_prime(y, z, weights), False)
    
    def frac_log_marginal(self, y, z, frac):
        '''
        The log-marginal with each data point given the same weight.
        Used in computing fractional Bayes factors.
        
        Parameters
        ----------
        y: array
            Data.
        z: array
            Predictor variables.
        frac: numeric
            Weighting fraction used for all data points. Should be in the range [0, 1].
        '''
        n = y.shape[-1]
        return self.weighted_log_marginal(y = y, z = z, weights = frac*np.ones(n))
    
    def marginal(self, y, z):
        '''
        The marginal likelihood of data.
        
        Parameters
        ----------
        y: array
            Data.
        z: array
            Predictor variables.
        '''
        return np.exp(self.log_marginal(y, z))   
    
class beta_bernoulli(distribution):
    
    def __init__(self, hpar = {'a': 1.0, 'b': 1.0}):
        '''
        Initialize the distribution with given hyperparameters.
        
        Parameters
        ----------
        hpar: dict
            Initial (conventional) hyperparameters.
        '''
        self.hpar = hpar # conventional hyperparameters
        self.tau = self.hpar_to_tau(self.hpar)
        self.p = 1 # number of likelihood parameters
    
    def hpar_to_tau(self, hpar):
        '''
        Convert conventional hyperparameters to natural ones (tau).
        '''
        return [hpar['a'] - 1, hpar['a'] + hpar['b'] - 2]
    
    def tau_to_hpar(self, tau):
        '''
        Convert natural hyperparameters (tau) to conventional ones.
        '''
        return {'a': tau[1-1] + 1, 'b': tau[2-1] - tau[1-1] + 1}
    
    def par_to_theta(self, par):
        '''
        Convert conventional parameters to natural ones (theta).
        
        Parameters
        ----------
        par: dict
            Conventional parameters. Should contain 'psi'.
        '''
        return [np.log(par['psi']/(1 - par['psi']))]
    
    def T(self, y):
        '''
        Sufficient statistics.
        
        Parameters
        ----------
        y: array
            Data.
        '''
        return [y]
        
    def f(self, y):
        return 0.0*y
        
    def g(self, theta):
        return np.log(1 + np.exp(theta))
        
    def h(self, tau, include_constant = True):
        '''
        Parameters
        ----------
        tau: list
            Distribution hyperparameters (in natural form).
        include_constant: logical, optional
            Whether to include constant terms, i.e. terms that do not
            depend on tau. Defaults to True.
            
        Notes
        -----
        Omitting constant terms improves the accuracy of calculating the marginal likelihood.
        This calculation involves the subtraction :math:`h(\tau) - h(\tau')`. The constant terms in h(tau)
        and h(tau') cancel out, so mathematically it's fine to omit them. Including them tends
        to cause more catastrophic cancellation in the floating point arithmetic.
        
        In this particular distribution there aren't actually any constant terms in h, but we retain
        the include_constant parameter and explanation for the sake of consistency.
        '''
        hpar = self.tau_to_hpar(tau)
        return betaln(hpar['a'], hpar['b'])

class normal_known_precision(distribution):
    '''
    Normal likelihood with known precision (xi) and a normal
    prior on the mean (mu).
    
    DOUBLE CHECK THIS (SOMETHING SEEMS TO BE WRONG).
    '''
    def __init__(self, hpar = {'m_mu': 0.0, 'xi_mu': 1.0}, xi = 1.0):
        '''
        Initialize the distribution with given hyperparameters.
        
        Parameters
        ----------
        hpar: dict
            Initial (conventional) hyperparameters.
        '''
        self.xi = xi
        self.sigma = 1/np.sqrt(self.xi)
        self.hpar = hpar
        self.tau = self.hpar_to_tau(self.hpar)
        self.p = 1
        
    def hpar_to_tau(self, hpar):
        '''
        Convert conventional hyperparameters to natural ones (tau).
        '''
        return [self.hpar['m_mu']*self.sigma*self.hpar['xi_mu'], self.hpar['xi_mu']/self.xi]
    
    def tau_to_hpar(self, tau):
        '''
        Convert natural hyperparameters (tau) to conventional ones.
        '''
        return {'m_mu': self.sigma*self.tau[1-1]/self.tau[2-1], 'xi_mu': self.xi*self.tau[2-1]}
    
    def par_to_theta(self, par):
        '''
        Convert conventional parameters to natural ones (theta).
        
        Parameters
        ----------
        par: dict
            Conventional parameters. Should contain 'mu'.
        '''
        return np.array(par['mu']/self.sigma)
    
    def T(self, y):
        '''
        Sufficient statistics.
        
        Parameters
        ----------
        y: array
            Data.
        '''
        return [y/self.sigma]
    
    def f(self, y):
        return 0.5*(self.xi*y**2 + np.log(2*np.pi) - np.log(self.xi))
    
    def g(self, theta):
        return 0.5*theta**2
        
    def h(self, tau, include_constant = True):
        '''
        Parameters
        ----------
        tau: list
            Distribution hyperparameters (in natural form).
        include_constant: logical, optional
            Whether to include constant terms, i.e. terms that do not
            depend on tau. Defaults to True.
            
        Notes
        -----
        Omitting constant terms improves the accuracy of calculating the marginal likelihood.
        This calculation involves the subtraction :math:`h(\tau) - h(\tau')`. The constant terms in h(tau)
        and h(tau') cancel out, so mathematically it's fine to omit them. Including them tends
        to cause more catastrophic cancellation in the floating point arithmetic.
        '''
        hpar = self.tau_to_hpar(tau)
        h = 0.5*(hpar['xi_mu']*hpar['m_mu']**2 - np.log(hpar['xi_mu']) + np.log(self.xi))
        if include_constant:
            h += 0.5*np.log(2*np.pi)
        return h
    
class normal_gamma_normal(distribution):
    '''
    Univariate normal likelihood with a normal-gamma prior.
    
    Notes
    -----
    ** ADD MATH **
    '''
    
    def __init__(self, hpar = {'m': 0.0, 'lambda': 1.0, 'alpha': 1.0, 'beta': 1.0}):
        '''
        Initialize the distribution with given hyperparameters.
        
        Parameters
        ----------
        hpar: dict
            Initial (conventional) hyperparameters.
        '''
        self.hpar = hpar
        self.tau = self.hpar_to_tau(self.hpar)
        self.p = 2 # number of parameters
    
    def hpar_to_tau(self, hpar):
        '''
        Convert conventional hyperparameters to natural ones (tau).
        '''
        return [hpar['lambda']*hpar['m'],
                -hpar['beta'] - 0.5*hpar['lambda']*hpar['m']**2,
                2*hpar['alpha'] - 1]
    
    def tau_to_hpar(self, tau):
        '''
        Convert natural hyperparameters (tau) to conventional ones.
        '''
        return {'m': tau[1-1]/tau[3-1],
                'lambda': tau[3-1],
                'alpha': 0.5*(tau[3-1] + 1),
                'beta': -0.5*tau[1-1]**2/tau[3-1] - tau[2-1]}
    
    def par_to_theta(self, par):
        '''
        Convert conventional parameters to natural ones (theta).
        
        Parameters
        ----------
        par: dict
            Conventional parameters. Should contain 'mu' and 'sigma'.
        '''
        return [par['mu']/par['sigma']**2, 
                1/par['sigma']**2]
    
    def T(self, y):
        '''
        Sufficient statistics.
        
        Parameters
        ----------
        y: array
            Data.
        '''
        return [y, -0.5*y**2]      
        
    def f(self, y):
        n = y.shape[-1]
        return np.array(n*[0.5*np.log(2*np.pi)])
        
    def g(self, theta):
        return 0.5*(theta[1-1]**2/theta[2-1] - np.log(theta[2-1]))
        
    def h(self, tau, include_constant = True):
        '''
        Parameters
        ----------
        tau: list
            Distribution hyperparameters (in natural form).
        include_constant: logical, optional
            Whether to include constant terms, i.e. terms that do not
            depend on tau. Defaults to True.
            
        Notes
        -----
        Omitting constant terms improves the accuracy of calculating the marginal likelihood.
        This calculation involves the subtraction h(tau) - h(tau'). The constant terms in h(tau)
        and h(tau') cancel out, so mathematically it's fine to omit them. Including them tends
        to cause more catastrophic cancellation in the floating point arithmetic.
        '''
        hpar = self.tau_to_hpar(tau)
        h = gammaln(hpar['alpha']) - hpar['alpha']*np.log(hpar['beta']) - 0.5*np.log(hpar['lambda'])
        if include_constant:
            h += 0.5*np.log(2*np.pi)
        return h
    
    def E_theta(self):
        '''
        Compute :math:`E[\theta]`
        '''
        return [] # FINISH
        
    def E_g_theta(self):
        '''
        Compute :math:`E[g(\theta)]`
        '''
        return [] # FINISH

class mvnormal_Wishart_mvnormal(distribution):
    '''
    Multivariate normal likelihood with a multivariate normal-Wishart prior.
    
    ** DOUBLE CHECK EVERYTHING **
    
    Notes
    -----
    
    ** ADD MATH **
    '''
    
    def __init__(self, hpar):
        '''
        Initialize the distribution with given hyperparameters.
        
        Parameters
        ----------
        hpar: dict
            Initial (conventional) hyperparameters, consisting of:
            m: 1-d array
                Prior mean vector for mu.
            lambda: int
                Prior scaling parameter (see the class documentation).
            V_inv: 2-d square array
                Inverse of the prior scale matrix for the Wishart prior on Sigma.
        '''
        self.hpar = hpar
        self.tau = self.hpar_to_tau(self.hpar)
        self.k = hpar['m'].shape[0] # size of mu
        self.p = 2 # number of parameters
        
    def hpar_to_tau(self, hpar):
        '''
        Convert conventional hyperparameters to natural ones (tau).
        '''
        return [hpar['lambda']*hpar['m'],
                -0.5*(hpar['lambda']*np.outer(hpar['m'], hpar['m']) + hpar['V_inv']),
                hpar['lambda']]
        
    def tau_to_hpar(self, tau):
        '''
        Convert natural hyperparameters (tau) to conventional ones.
        '''
        return {'m': tau[1-1]/tau[3-1],
                'V_inv': -2*tau[2-1] - (1/tau[3-1])*np.outer(tau[1-1], tau[1-1]),
                'lambda': tau[3-1]}
        
    def par_to_theta(self, par):
        '''
        Convert conventional parameters to natural ones (theta).
        
        Parameters
        ----------
        par: dict
            Conventional parameters. Should contain 'mu' and 'Sigma_inv'.
        '''
        return [par['Sigma_inv']@par['mu'], par['Sigma_inv']]
        
    def T(self, y):
        '''
        Sufficient statistics.
        
        Parameters
        ----------
        y: array
            Data.
        '''
        n = y.shape[-1]
        return [y, -0.5*np.stack([np.outer(y[:,i], y[:,i]) for i in range(n)], axis = -1)]
    
    def f(self, y):
        return 0.5*self.k*np.log(2*np.pi)
        
    def g(self, theta):
        return 0.5*( theta[1-1].T@inv(theta[2-1])@theta[1-1] - np.log(det(theta[2-1])) )
        
    def h(self, tau, include_constant = True):
        '''
        Parameters
        ----------
        tau: list
            Distribution hyperparameters (in natural form).
        include_constant: logical, optional
            Whether to include constant terms, i.e. terms that do not
            depend on tau. Defaults to True.
        '''
        h = -0.5*self.k*np.log(tau[3-1]) + 0.5*(tau[3-1] + self.k)*self.k*np.log(2) - 0.5*(tau[3-1] + self.k)*np.log(det( -2*tau[2-1] - (1/tau[3-1])*np.outer(tau[1-1], tau[1-1]) )) + multigammaln(0.5*(tau[3-1] + self.k), self.k)
        if include_constant:
            h += 0.5*self.k*np.log(2*np.pi)
        return h
    
class multi_group_normal(distribution_with_predictor):
    '''
    Notes
    -----
    z is an n_t x n array indicating group membership.
    z[t, i] = 1 if observation i is in group t and = 0 otherwise.
    
    theta = [xi*mu, xi]
    mu = the vector of the means for y in each group
    xi = the precision of y (shared across groups)
    '''
    
    def __init__(self, hpar = {'m': 0.0, 'lambda': 1.0, 'alpha': 1.0, 'beta': 1.0}, n_t = 2):
        '''
        Parameters
        ----------
        hpar: dict
            Initial (conventional) hyperparameters.
        n_t: int
            Number of groups.
        '''
        self.n_t = n_t
        self.hpar = {'m': hpar['m']*np.ones(n_t), 
                     'lambda': hpar['lambda']*np.ones(n_t), 
                     'alpha': hpar['alpha'], 
                     'beta': hpar['alpha']}
        self.tau = self.hpar_to_tau(self.hpar)
        self.p = 2
    
    def hpar_to_tau(self, hpar):
        '''
        Convert conventional hyperparameters to natural ones (tau).
        '''
        return [hpar['lambda']*hpar['m'], 
                -hpar['beta'] - 0.5*np.sum(hpar['lambda']*hpar['m']**2),
                2*hpar['alpha'] + self.n_t - 2,
                0.5*hpar['lambda']]
    
    def tau_to_hpar(self, tau):
        '''
        Convert natural hyperparameters (tau) to conventional ones.
        '''
        return {'m': 0.5*tau[1-1]/tau[4-1],
                'lambda': 2*tau[4-1],
                'alpha': 0.5*(tau[3-1] - self.n_t) + 1,
                'beta': -tau[2-1] - 0.25*np.sum(tau[1-1]**2/tau[4-1])}
    
    def T(self, y, z):
        '''
        Sufficient statistics.
        
        Parameters
        ----------
        y: array
            Data.
        z: array
            Predictor variables.
        '''
        return [z*y, -0.5*y**2]
    
    def S(self, z):
        return 0.5*z
    
    def f(self, y):
        n = y.shape[-1]
        return np.array(n*[0.5*np.log(2*np.pi)])
        
    def g(self, theta):
        return -0.5*np.log(theta[2-1])
        
    def k(self, theta):
        return theta[1-1]**2/theta[2-1]
        
    def h(self, tau, include_constant = True):
        '''
        Parameters
        ----------
        tau: list
            Distribution hyperparameters (in natural form).
        include_constant: logical, optional
            Whether to include constant terms, i.e. terms that do not
            depend on tau. Defaults to True.
            
        Notes
        -----
        Omitting constant terms improves the accuracy of calculating the marginal likelihood.
        This calculation involves the subtraction h(tau) - h(tau'). The constant terms in h(tau)
        and h(tau') cancel out, so mathematically it's fine to omit them. Including them tends
        to cause more catastrophic cancellation in the floating point arithmetic.
        '''
        hpar = self.tau_to_hpar(tau)
        h = gammaln(hpar['alpha']) - hpar['alpha']*np.log(hpar['beta']) - 0.5*np.sum(np.log(hpar['lambda']))
        if include_constant:
            h += 0.5*self.n_t*np.log(2*np.pi)
        return h
        
    