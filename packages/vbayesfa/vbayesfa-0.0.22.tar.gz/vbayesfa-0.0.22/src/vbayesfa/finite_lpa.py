import numpy as np
from vbayesfa.mixture_model import mixture_model
from scipy.special import digamma, loggamma
from scipy.stats import dirichlet as dirichlet_dist

class finite_lpa_model(mixture_model):
    '''
    Bayesian latent profile analysis (LPA) model with a finite number of latent profiles that
    have a Dirichlet distribution prior with fixed concentration parameter (alpha)
    
    Latent profiles have different means for each variable but share a common precision (xi).
    These have a normal-gamma prior.
    
    ** UPDATE BELOW AS NEEDED **
    
    Attributes
    ----------
    * Data and related *
    
    x: array
        Matrix of observations (rows are variables and columns are participants/observations).
    T: integer
        The number of latent profiles.
    index: array or None
        Participant IDs.
    x_names: ordered categorical series
        Names of observed variables.
    mask: array
        Indicates missing observations (= 1 if not missing, = 0 if missing).
    n: int
        Number of observations.
    n_per_var: array of int
        Number of observations for each variable (accounting for missing data).
    m: int
        Number of observed variables.
    seed: int
        Random seed.
    rng: random generator
        Generator for random numbers.
    
    * Prior distribution hyperparameters *
    
    prior_alpha_xi: float
        Prior conventional hyperparameter for xi.
    prior_beta_xi: float
        Prior conventional hyperparameter for xi.
    prior_m_mu: float
        Prior conventional hyperparameter for mu.
    prior_lambda_mu: float
        Prior conventional hyperparameter for mu.
    prior_tau1: float
        Prior natural hyperparameter for mu and xi.
    prior_tau2: float
        Prior natural hyperparameter for mu and xi.
    prior_tau3: float
        Prior natural hyperparameter for mu and xi.
    prior_tau4: float
        Prior natural hyperparameter for mu and xi.
    h_prior_tau: float
        Prior log-normalizer for each of the observed variables.
    prior_w1: float
        First prior hyperparameter on alpha.
    prior_w2: float
        Second prior hyperparameter on alpha.
    
    * Lists for storing the ELBO and its components at each iteration *
    
    E_log_lik_list: list
        List of expected log-likelihood values across updates.
    E_log_prior_list: list
        List of expected log-prior values across updates.
    entropy_list: list
        List of variational distribution entropy values across updates.
    elbo_list: list
        List of ELBO (evidence lower bound) values across updates.
    
    * Variational hyperparameters and related quantities *
    
    phi: array
        Latent profile membership probabilities.
    v_mu: array
        Variance of mu.
    E_xi_mu: array
        Expected value of xi*mu.
    E_xi_mu2: array
        Expected value of xi*mu^2.
    E_xi: array
        Expected value of xi.
    E_log_xi: array
        Expected value of log(xi).
    
    ** ADD HYPERPARAMETERS FOR PI **
    
    E_log_pi: array
        Expected value of log(pi).
    E_pi: array
        Expected value of pi.
    
    * Results arranged for interpretation and analysis *
    
    n_profiles: int
        Number of non-empty profiles (based on hard profile assignment).
    profile_order: array
        Order of profiles by number of members, i.e. profile size (based on hard profile assignment).
    sorted_phi: array
        Version of phi (profile membership probabilities) sorted by profile size
        and omitting empty profiles.
    sorted_m_mu: array
        Version of m_mu (posterior mean of mu) sorted by profile size and omitting empty profiles.
    sorted_v_mu: array
        Version of v_mu (posterior variance of mu) sorted by profile size and omitting empty profiles.
    z_hat: array
        Point estimates of z (profile membership) based on hard assignment, with profiles labeled in size order.
    z_hat_1hot: array
        The same information as z_hat, but in 1-hot encoding, i.e. z_hat_1hot[j,i] = 1 if person/observation i
        is in profile j and = 0 otherwise.
    n_per_profile: array
        Profile size, i.e. the number of members of each profile based on hard assignment (ordered by profile size).
    prop_per_profile: array
        Similar to n_per_profile, but gives proportions rather than numbers.
    '''
    def __init__(self, x, T = 4, prior_alpha_pi = 0.5, prior_lambda_mu = 0.5, prior_strength_for_xi = 10.0, phi = None, seed = 1234):
        '''
        Parameters
        ----------
        x: data frame or array
            Observed data (data frame or matrix).  If a matrix then rows are variables and columns
            are observations; if a data frame then rows are observations and columns are variables.
            Missing values are replaced with 0 for computational reasons.
        T: integer, optional
            The number of latent profiles.
        prior_alpha_pi: float, optional
            Prior strength of the Dirichlet prior distribution on pi.
        prior_lambda_mu: float, optional
            Controls the width of the prior distribution on mu: 
            higher values -> tighter prior around 0.
        prior_strength_for_xi: float, optional
            Controls the strength of the gamma prior distribution on xi.
            This prior is assumed to have a mean of 1, with alpha = prior_strength_for_xi/2
            and beta = prior_strength_for_xi/2.
        phi: array or None, optional
            If None (the default) then profile membership probabilities (phi) are randomly
            sampled from a Dirichlet(1, 1, ...) distribution. Otherwise this is an array
            of starting values for phi, with a number columns equal to the number of 
            observations and number of rows equal to or less than T.
        seed: integer, optional
            The seed for random number generation.
            
        Notes
        -----
        The means (mu) and precisions (xi) have a multi-mean normal-gamma prior.
        
        The fact that the prior alpha_xi = prior beta_xi implies that the prior distribution on xi
        has a mean of 1.
        '''
        super().__init__(x = x, T = T, prior_hpar = {'alpha_pi': prior_alpha_pi, 'lambda_mu': prior_lambda_mu, 'strength_for_xi': prior_strength_for_xi}, phi = phi, seed = seed)
    
    def _initialize_q_pi(self, prior_hpar):
        '''
        Initialize the variational distribution of latent class/profile base rates (pi).
        '''
        self.prior_alpha_pi = prior_hpar['alpha_pi']
        self.alpha_pi = self.prior_alpha_pi*np.ones(self.T)
        self._update_q_pi()
    
    def _update_q_pi(self):
        '''
        Update the variational distribution of latent class/profile base rates (pi).
        '''
        self.alpha_pi = self.prior_alpha_pi + self.phi.sum(axis = 1)
        self.E_pi = self.alpha_pi/self.alpha_pi.sum()
        self.E_log_pi = digamma(self.alpha_pi) - digamma(self.alpha_pi.sum())
    
    def _H_q_pi(self):
        '''
        Entropy of the variational distribution of latent class/profile base rates (pi).
        '''
        return dirichlet_dist.entropy(self.alpha_pi)
    
    def _E_log_prior_pi(self):
        '''
        Variational expectation of the log-prior on latent class/profile base rates (pi).
        '''
        return np.sum((self.alpha_pi - 1)*self.E_log_pi) - np.sum(loggamma(self.alpha_pi)) + loggamma(self.alpha_pi.sum())  