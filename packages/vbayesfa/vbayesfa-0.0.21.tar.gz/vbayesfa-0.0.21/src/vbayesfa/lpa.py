import numpy as np
from vbayesfa.mixture_model import mixture_model
from scipy.special import digamma, loggamma
from scipy.stats import beta as beta_dist
from scipy.stats import gamma as gamma_dist

class lpa_model(mixture_model):
    '''
    Bayesian latent profile analysis (LPA) model with a Dirichlet process prior to
    allow for a potentially unbounded number of latent profiles.
    
    Latent profiles have different means for each variable but share a common precision (xi).
    These have a normal-gamma prior.
    
    The concentration parameter (alpha) is learned.
    
    Attributes
    ----------
    * Data and related *
    
    x: array
        Matrix of observations (rows are variables and columns are participants/observations).
    T: integer
        Truncation level for the variational approximation. Represents the maximum number of
        latent profiles that can be discovered.
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
    w1: float
        First hyperparameter of alpha.
    w2: float
        Second hyperparameter of alpha.
    E_alpha: float
        Expected value of alpha.
    E_log_alpha: float
        Expected value of log(alpha).
    gamma1: array
        First hyperparameter of V.
    gamma2: array
        Second hyperparameter of V.
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
    
    Notes
    -----
    This is based on Blei and Jordan (2006).
    
    The concentration parameter is given a Gamma(3, 1) prior and learned via variational
    Bayes as described in Appendix B.
    '''
    def __init__(self, x, T = 20, prior_w1 = 3.0, prior_w2 = 1.0, prior_lambda_mu = 0.5, prior_strength_for_xi = 10.0, phi = None, seed = 1234):
        '''
        Parameters
        ----------
        x: data frame or array
            Observed data (data frame or matrix).  If a matrix then rows are variables and columns
            are observations; if a data frame then rows are observations and columns are variables.
            Missing values are replaced with 0 for computational reasons.
        T: integer, optional
            Truncation level for the variational approximation. Represents the maximum number of
            latent profiles that can be discovered.
        prior_w1: float, optional,
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
        phi: array or None, optional
            If None (the default) then profile membership probabilities (phi) are randomly
            sampled from a Dirichlet(1, 1, ...) distribution. Otherwise this is an array
            of starting values for phi, with a number columns equal to the number of 
            observations and number of rows equal to or less than T.
        seed: integer, optional
            The seed for random number generation.
            
        Notes
        -----
        This is based on Blei and Jordan (2006).

        The concentration parameter (alpha) is given a Gamma(prior_w1, prior_w2) prior and learned via variational
        Bayes as described in Appendix B.
        
        Thus the prior mean of alpha is prior_w1/prior_w2.

        The means (mu) and precisions (xi) have a multi-mean normal-gamma prior.
        
        The fact that the prior alpha_xi = prior beta_xi implies that the prior distribution on xi
        has a mean of 1.
        '''
        super().__init__(x = x, T = T, prior_hpar = {'lambda_mu': prior_lambda_mu, 'strength_for_xi': prior_strength_for_xi, 'w1': prior_w1, 'w2': prior_w2}, phi = phi, seed = seed)
    
    def _initialize_q_pi(self, prior_hpar):
        '''
        Initialize the variational distribution of latent class/profile base rates (pi),
        broken into stick-breaking lengths (V) and the Dirichlet process concentration
        parameter (alpha).
        '''
        # initialize distribution of the Dirichlet process concentration parameter (alpha)
        self.prior_w1 = prior_hpar['w1']
        self.prior_w2 = prior_hpar['w2']
        self.w1 = self.prior_w1 + self.T - 1
        self.w2 = self.prior_w2
        self.E_alpha = self.w1/self.w2
        self.E_log_alpha = digamma(self.w1) - np.log(self.w2)
        # initialize distribution of stick-breaking lengths (V)
        self.gamma1 = np.zeros(self.T)
        self.gamma2 = np.zeros(self.T)
        self.E_log_V = np.zeros(self.T)
        self.E_log_1minusV = np.zeros(self.T)
        self.E_log_pi = np.zeros(self.T)
        # update distribution of V
        self._update_q_V()
    
    def _update_q_V(self):
        # update distribution of stick-breaking lengths (V)
        for t in range(self.T):
            self.gamma1[t] = 1 + np.sum(self.phi[t,:])
            self.gamma2[t] = self.E_alpha + np.sum(self.phi[range(t+1,self.T),:])
            self.E_log_V[t] = digamma(self.gamma1[t]) - digamma(self.gamma1[t] + self.gamma2[t])
            self.E_log_1minusV[t] = digamma(self.gamma2[t]) - digamma(self.gamma1[t] + self.gamma2[t]) 
        for t in range(self.T):
            self.E_log_pi[t] = self.E_log_V[t] + np.sum(self.E_log_1minusV[range(t-1)])
        self.E_V = self.gamma1/(self.gamma1 + self.gamma2)
        product_term = np.concatenate([np.array([1]), np.cumprod(1 - self.E_V)[range(self.T-1)]])
        self.E_pi = self.E_V*product_term
        
    def _update_q_alpha(self):
        # update distribution of the Dirichlet process concentration parameter (alpha)
        self.w2 = self.prior_w2 - np.sum(self.E_log_1minusV[range(self.T - 1)]) # self.w1 stays constant, so we only update self.w2
        self.E_alpha = self.w1/self.w2
        self.E_log_alpha = digamma(self.w1) - np.log(self.w2)
    
    def _update_q_pi(self):
        '''
        Update the variational distribution of latent class/profile base rates (pi),
        broken into stick-breaking lengths (V) and the Dirichlet process concentration
        parameter (alpha).
        '''
        self._update_q_V()
        self._update_q_alpha()
    
    def _H_q_pi(self):
        '''
        Entropy of the variational distribution of latent class/profile base rates (pi),
        broken into stick-breaking lengths (V) and the Dirichlet process concentration
        parameter (alpha).
        '''
        H_q_V = beta_dist.entropy(self.gamma1, self.gamma2).sum()
        H_q_alpha = gamma_dist.entropy(a = self.w1, scale = 1/self.w2)
        return H_q_V + H_q_alpha
    
    def _E_log_prior_pi(self):
        '''
        Variational expectation of the log-prior on latent class/profile base rates (pi),
        broken into stick-breaking lengths (V) and the Dirichlet process concentration
        parameter (alpha).
        '''
        E_log_prior_V = np.sum((self.E_alpha - 1)*self.E_log_1minusV + self.E_log_alpha)
        E_log_prior_alpha = -self.w2*self.E_alpha + (self.w1 - 1)*self.E_log_alpha - loggamma(self.w1) + self.w1*np.log(self.w2)
        return E_log_prior_V + E_log_prior_alpha