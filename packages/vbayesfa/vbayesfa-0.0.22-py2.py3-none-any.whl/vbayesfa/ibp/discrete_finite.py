import numpy as np
from itertools import combinations
from scipy.stats import norm as norm_dist
from scipy.stats import bernoulli as bernoulli_dist
from scipy.special import digamma, gamma, beta

class ibp_model:
    '''
    Factor analysis model with discrete factors.  This version includes include an intercept term.
    The precision of observed variables (xi) is fixed.
    
    Parameters
    ----------
    x: array
        Matrix of observed data.  Rows are variables and columns are observations.
    alpha: float, optional
        Parameter of the Indian buffet process.
    omega: float, optional
        Prior precision of A.
    xi: float, optional
        Precision of observed variables.
    p: integer, optional
        Number of latent factors used in the finite approximation to the Indian buffet process.
    include_intercept: logical, optional
        If True (default) then an intercept term is included.  If False then it is not.
    
    Notes
    -----
    *****
    '''
    
    def __init__(self, x, alpha = 2.0, omega = 0.2, xi = 1, p = 4, include_intercept = True):
        """
        Parameters
        ----------
        x: array
            Matrix of observed data.  Rows are variables and columns are observations.
        alpha: float, optional
            Parameter of the Indian buffet process.
        omega: float, optional
            Prior precision of A.
        xi: float, optional
            Precision of observed variables.
        p: integer, optional
            Number of latent factors used in the finite apporximation to the Indian buffet process.
        include_intercept: logical, optional
            If True (default) then an intercept term is included.  If False then it is not.
        """
        # ----- SET UP SOME VARIABLES -----
        self.n = x.shape[1] # number of observations
        self.m = x.shape[0] # number of observed variables
        self.p = p
        self.mu = 1 - np.isnan(x) # = 1 if not missing, = 0 if missing CHECK THIS
        self.x = x
        self.x[np.isnan(x)] = 0 # this is an arbitrary value to make computations work
        self.tilde_x = self.mu*x
        self.tilde_xsq = self.mu*x**2
        self.tilde_x_sum = np.sum(self.tilde_x)
        self.tilde_xsq_sum = np.sum(self.tilde_xsq)
        self.tilde_n = self.mu.sum(axis = 1)
        self.alpha = alpha
        self.omega = omega
        self.elbo_list = [] # list for storing ELBO values at each iteration
        self.rng = np.random.default_rng() # for generating random permutations
        self.xi = xi # fixed precision of observed variables
        self.include_intercept = include_intercept
        # indices used for computing E_q[(A_{j,:} z_{:,i})^2]
        index_combos = np.array(list(combinations(range(self.p + self.include_intercept), 2)))
        self.kneql = index_combos[:,0]
        self.lneqk = index_combos[:,1]
        # a variable used in several calculations
        self.E_Az_sq = np.zeros([self.m, self.n])

        # ----- INITIALIZE VARIATIONAL HYPERPARAMETERS -----
        
        # initialize A's hyperparameters
        #self.mA = self.rng.uniform(low = -0.05, high = 0.05, size = [self.m, self.p + self.include_intercept])
        self.mA = self.rng.normal(loc = 0.0, scale = 1/np.sqrt(self.omega), size = [self.m, self.p + self.include_intercept])
        self.vA = 2.0*np.ones([self.m, self.p + self.include_intercept])        
        # initialize z's hyperparameters
        #self.nu = self.rng.uniform(low = 0.1, high = 0.25, size = [self.p, self.n])
        #self.nu = self.rng.uniform(low = 0.2, high = 0.8, size = [self.p, self.n])
        self.nu = self.rng.uniform(low = 0.01, high = 0.99, size = [self.p, self.n])
        self.update_nu_plus() # if include_intercept then this adds a row of 1s for the intercept, otherwise it is equal to nu
        # initialize pi's hyperparameters
        nu_sum = self.nu.sum(axis = 1)
        self.tau1 = self.alpha/self.p + nu_sum
        self.tau2 = 1 + self.n - nu_sum
        self.E_pi = self.tau1/(self.tau1 + self.tau2)
    
    def fit(self, stop_threshold = 1e-05, max_iter = 50, min_iter = 30):
        """
        Parameters
        ----------
        stop_threshold: float, optional
            Relative change in the ELBO at which the optimization should stop.
        max_iter: integer, optional
            Maximum number of iterations to run the optimization.
        min_iter: integer, optional
            Minimum number of iterations to run the optimization.
        """
        
        relative_elbo_change = 1.0 # this is an arbitrary value for the first iteration
        itr = 0 # counter for iterations
        continue_loop = True
        int_elbo = -np.Inf        
        
        while continue_loop:
            # ----- UPDATE VARIATIONAL HYPERPARAMETERS -----
            
            # update A's hyperparameters
            self.update_nu_plus()
            for j in range(self.m):
                for k in range(self.mA.shape[1]):
                    lval = list(range(0, k)) + list(range(k+1, self.mA.shape[1])) # latent factor indices excluding k, i.e. l : l =/= k
                    self.vA[j,k] = (self.xi*np.sum(self.mu[j,:]*self.nu_plus[k,:]) + self.omega)**(-1)
                    self.mA[j,k] = self.vA[j,k]*self.xi*np.sum(self.nu_plus[k,:]*(self.tilde_x[j,:] - self.mu[j,:]*(self.mA[j,lval]@self.nu_plus[lval,:])))

            # update z's hyperparameters (in random order)
            for i in self.rng.permutation(self.n):
                for k in range(self.p):
                    self.update_nu_plus()
                    lval = list(range(0, k)) + list(range(k+1, self.mA.shape[1])) # latent factor indices excluding k, i.e. l : l =/= k
                    #theta_ki = np.sum(self.mu[:,i]*self.xi*( self.mA[:,k]*(self.x[:,i] - self.mA[:,lval]@self.nu_plus[lval,i]) - 0.5*(self.vA[:,k] + self.mA[:,k]**2) )) + digamma(self.tau1[k]) - digamma(self.tau2[k])
                    theta_ki = self.xi*( np.sum(self.mu[:,i]*self.mA[:,k]*self.x[:,i]) - np.sum(self.mu[:,i]*self.mA[:,k]*(self.mA[:,lval]@self.nu_plus[lval,i])) - 0.5*np.sum(self.mu[:,i]*(self.vA[:,k] + self.mA[:,k]**2)) ) + digamma(self.tau1[k]) - digamma(self.tau2[k])
                    self.nu[k,i] = 1/(1 + np.exp(-theta_ki))

            # update pi's hyperparameters
            nu_sum = self.nu.sum(axis = 1)
            self.tau1 = self.alpha/self.p + nu_sum
            self.tau2 = 1 + self.n - nu_sum
            self.E_pi = self.tau1/(self.tau1 + self.tau2)

            # ----- COMPUTE ELBO -----
            elbo = self.compute_elbo()
            # ----- FINISH CURRENT ITERATION -----            
            self.elbo_list += [elbo] # record the current ELBO
            itr += 1 # increment the iteration counter
            if itr < min_iter: # automatically continue if below the minimum number of iterations
                continue_loop = True
            else: # otherwise, continue if ELBO change is below threshold and we haven't yet hit the iteration limit
                relative_elbo_change = np.abs((self.elbo_list[-2] - self.elbo_list[-1])/self.elbo_list[-2])
                continue_loop = (relative_elbo_change > stop_threshold) and (itr < max_iter)

    def update_nu_plus(self):
        if self.include_intercept:
            self.nu_plus = np.append(self.nu, np.ones([1, self.n]), axis = 0)
        else:
            self.nu_plus = self.nu
                
    def compute_E_Az_sq(self):
        '''
        Compute E_q[(A_{j,:} z_{:,i})^2].
        '''
        self.update_nu_plus()
        for i in range(self.n):
            for j in range(self.m):
                self.E_Az_sq[j,i] = (self.vA[j,:] + self.mA[j,:]**2)@self.nu_plus[:,i] + 2*np.sum(self.mA[j,self.kneql]*self.mA[j,self.lneqk]*self.nu_plus[self.kneql,i]*self.nu_plus[self.lneqk,i])
    
    def compute_elbo(self):
        # compute expected log-likelihood
        self.compute_E_Az_sq()
        term1 = 0
        for j in range(self.m): # 1st term of E_log_lik
            term1 += self.xi*( self.mA[j,:]@(self.nu_plus@self.tilde_x[j,:].T) - 0.5*self.tilde_xsq_sum - 0.5*np.sum(self.mu[j,:]*self.E_Az_sq[j,:]) )
        term2 = 0.5*np.sum( self.tilde_n*( np.log(self.xi) - np.log(2*np.pi) ) ) # 2nd term of E_log_lik
        E_log_lik = term1 + term2 # this is split into two terms for convenience

        # compute expected log-prior
        E_log_A_prior = -0.5*self.omega*np.sum(self.vA + self.mA**2) - 0.5*self.m*self.p*(np.log(2*np.pi) - np.log(self.omega))
        E_log_z_prior = np.sum( (digamma(self.tau1) - digamma(self.tau2))*np.sum(self.nu, axis = 1) + self.n*(digamma(self.tau2) - digamma(self.tau1 + self.tau2)) )
        E_log_pi_prior = (self.alpha/self.p - 1)*np.sum(digamma(self.tau1) - digamma(self.tau1 + self.tau2)) + self.p*np.log(self.alpha/self.p)
        E_log_prior = E_log_A_prior + E_log_z_prior + E_log_pi_prior

        # compute entropy
        H_A = norm_dist.entropy(self.mA, np.sqrt(self.vA)).sum()
        H_z = bernoulli_dist.entropy(self.nu).sum()
        H_pi = np.sum(np.log(np.maximum(beta(self.tau1, self.tau2), 1e-320)) - (self.tau1 - 1)*digamma(self.tau1) - (self.tau2 - 1)*digamma(self.tau2) + (self.tau1 + self.tau2 - 2)*digamma(self.tau1 + self.tau2)) # the scipy.stats entropy method doesn't appear to work well with certain parameter values
        entropy = H_A + H_z + H_pi

        return E_log_lik + E_log_prior + entropy