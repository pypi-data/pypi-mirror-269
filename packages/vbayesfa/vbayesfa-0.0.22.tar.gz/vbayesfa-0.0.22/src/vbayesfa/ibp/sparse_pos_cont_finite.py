import numpy as np
from numpy.linalg import inv
from itertools import combinations
from scipy.stats import norm as norm_dist
from scipy.stats import gamma as gamma_dist
from scipy.stats import bernoulli as bernoulli_dist
from scipy.special import polygamma, digamma, gamma, beta
from scipy.optimize import minimize

class ibp_model:
    '''
    Factor analysis model with positive sparse continuous factors.  This version includes include an intercept term.
    The precision of observed variables (xi) is fixed.
    
    ***** FINISH UPDATING *****
    
    Parameters
    ----------
    x: array
        Matrix of observed data.  Rows are variables and columns are observations.
    alpha: float, optional
        Parameter of the Indian buffet process.
    omega: float, optional
        Prior precision of A.
    prior_mS: float, optional
        Prior mean of S.
    prior_nS: float, optional
        Prior "strength" (virtual number of observations) for S.
    xi: float, optional
        Precision of observed variables.
    p: integer, optional
        Number of latent factors used in the finite apporximation to the Indian buffet process.
    include_intercept: logical, optional
        If True (default) then an intercept term is included.  If False then it is not.
    
    Notes
    -----
    The continuous latent factor component (S) has a gamma distribution, and thus is strictly positive. 
    *****
    '''
    
    def __init__(self, x, alpha = 2.0, omega = 0.2, prior_mS = 1.0, prior_nS = 5.0, xi = 1, p = 4, include_intercept = True):
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
        self.prior_aS = prior_nS/2 # one conventional prior hyperparameter for S
        self.prior_bS = prior_nS/(2*prior_mS) # the other conventional prior hyperparameter for S
        # lists for storing the ELBO and its components at each iteration
        self.E_log_lik_list = []
        self.E_log_prior_list = []
        self.entropy_list = []
        self.elbo_list = []
        self.rng = np.random.default_rng() # for generating random permutations
        self.xi = xi # fixed precision of observed variables
        self.include_intercept = include_intercept
        # indices used for computing E_q[(A_{j,:} z_{:,i})^2]
        index_combos = np.array(list(combinations(range(self.p + self.include_intercept), 2)))
        self.kneql = index_combos[:,0]
        self.lneqk = index_combos[:,1]
        self.n_combos = self.lneqk.shape[0]

        # ----- INITIALIZE VARIATIONAL HYPERPARAMETERS -----
        
        # initialize A's hyperparameters
        self.mA = self.rng.normal(loc = 0.0, scale = 1/np.sqrt(self.omega), size = [self.m, self.p + self.include_intercept])
        self.vA = 0.1*np.ones([self.m, self.p + self.include_intercept])
        self.E_Asq = self.mA**2 + self.vA
        # initialize u's hyperparameters
        self.nu = self.rng.uniform(low = 0.2, high = 0.8, size = [self.p, self.n])
        # initialize S's hyperparameters
        self.aS = self.prior_aS*np.ones([self.p, self.n])
        self.bS = self.prior_bS*np.ones([self.p, self.n])
        self.E_S = self.aS/self.bS
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
            update_s = True
            if update_s:
                # update S's hyperparameters (in random order)
                for i in self.rng.permutation(self.n):
                    for k in self.rng.permutation(self.p):
                        # constants used for computing the ELBO gradient
                        lval = list(range(0, k)) + list(range(k+1, self.mA.shape[1])) # l : l =/= k
                        C1 = self.nu[k,i]*np.sum(self.xi*self.mu[:,i]*self.mA[:,k]*(self.x[:,i] - self.mA[:,lval]@self.nu[lval,i]))
                        C2 = -0.5*self.nu[k,i]*np.sum(self.xi*self.mu[:,i]*self.E_Asq[:,k])
                        p0 = np.log(self.aS[k,i])
                        p1 = np.log(self.bS[k,i])
                        for s in range(5):
                            new_a = np.exp(p0)
                            new_b = np.exp(p1)
                            # compute the ELBO gradient (log scale)
                            gradient0 = new_a*((1/new_b)*(C1 - self.prior_bS) + ((2*new_a + 1)/(new_b**2))*C2 + (self.prior_aS - new_a)*polygamma(1, new_a) + 1) # partial derivative of the ELBO wrt p0 = log(a)
                            gradient1 = new_b*((new_a/(new_b**2))*(self.prior_bS - C1) - ((2*new_a*(new_a + 1))/(new_b**3))*C2 - self.prior_aS/new_b) # partial derivative of the ELBO wrt p1 = log(b)
                            # do the gradient ascent step (log scale)
                            p0 += 0.005*gradient0
                            p1 += 0.005*gradient1
                        # update aS and bS
                        self.aS[k,i] = np.exp(p0)
                        self.bS[k,i] = np.exp(p1)
                # compute mean and variance of S
                self.mS = self.aS/self.bS
                self.vS = self.aS/self.bS**2
                        
                        # function to compute -ELBO as a function of aS[k,i] and bS[k,i], and its gradient
                       # def neg_ELBO_and_gradient(pars):
                       #     new_a = np.exp(pars[0])
                       #     new_b = np.exp(pars[1])
                       #     new_full_aS = self.aS.copy()
                       #     new_full_aS[k,i] = new_a
                       #     new_full_bS = self.bS.copy()
                       #     new_full_bS[k,i] = new_b
                            
                            # compute the ELBO
                       #     E_log_lik = self.compute_E_log_lik(aS = new_full_aS, bS = new_full_bS)
                       #     E_log_prior = self.compute_E_log_prior(aS = new_full_aS, bS = new_full_bS)
                       #     entropy = self.compute_entropy(aS = new_full_aS, bS = new_full_bS)
                       #     ELBO = E_log_lik + E_log_prior + entropy
                            
                            # compute the gradient of the ELBO
                       #     gradient = np.zeros(2)
                       #     gradient[0] = new_a*((1/new_b)*(C1 - self.prior_bS) + ((2*new_a + 1)/(new_b**2))*C2 + (self.prior_aS - new_a)*polygamma(1, new_a) + 1) # partial derivative of the ELBO wrt pars[0]
                       #     gradient[1] = new_b*((new_a/(new_b**2))*(self.prior_bS - C1) - ((2*new_a*(new_a + 1))/(new_b**3))*C2 - self.prior_aS/new_b) # partial derivative of the ELBO wrt pars[1]
                            
                       #     return -ELBO, -gradient
                            
                        # use the BFGS algorithm to find to optimal values of aS[k,i] and bS[k,i] (on the log scale)
                        #result = minimize(fun = neg_ELBO_and_gradient,
                        #                  #x0 = np.array([np.log(self.aS[k,i]), np.log(self.bS[k,i])]),
                        #                  x0 = np.ones(2),
                        #                  method = 'BFGS',
                        #                  jac = True) # specifies that the gradient is contained in the function
                        
                        #self.aS[k,i] = np.exp(result['x'][0])
                        #self.bS[k,i] = np.exp(result['x'][1])
            
            update_u = True
            if update_u:
                # update u's hyperparameters (in random order)
                for i in self.rng.permutation(self.n):
                    for k in self.rng.permutation(self.p):
                        E_z = self.compute_E_z()
                        lval = list(range(0, k)) + list(range(k+1, self.mA.shape[1])) # latent factor indices excluding k, i.e. l : l =/= k
                        theta_ki = np.sum(self.mu[:,i]*self.xi*( self.mA[:,k]*self.mS[k,i]*(self.x[:,i] - self.mA[:,lval]@E_z[lval,i]) - 0.5*(self.mA[:,k]**2 + self.vA[:,k])*(self.mS[k,i]**2 + self.vS[k,i]) )) + digamma(self.tau1[k]) - digamma(self.tau2[k])
                        self.nu[k,i] = 1/(1 + np.exp(-theta_ki))
            
            # update pi's hyperparameters
            nu_sum = self.nu.sum(axis = 1)
            self.tau1 = self.alpha/self.p + nu_sum
            self.tau2 = 1 + self.n - nu_sum
            self.E_pi = self.tau1/(self.tau1 + self.tau2)
            
            # update A's hyperparameters
            E_z = self.compute_E_z()
            E_z_sq = self.compute_E_z_sq()
            for k in self.rng.permutation(self.mA.shape[1]):
                lval = list(range(0, k)) + list(range(k+1, self.mA.shape[1])) # l : l =/= k
                for j in range(self.m):
                    self.vA[j,k] = (self.xi*np.sum(self.mu[j,:]*E_z_sq[k,:]) + self.omega)**(-1)
                    self.mA[j,k] = self.vA[j,k]*self.xi*np.sum(self.mu[j,:]*E_z[k,:]*(self.x[j,:] - self.mA[j,lval]@E_z[lval,:]))
            self.E_Asq = self.mA**2 + self.vA

            # ----- COMPUTE ELBO -----
            self.E_log_lik_list += [self.compute_E_log_lik()]
            self.E_log_prior_list += [self.compute_E_log_prior()]
            self.entropy_list += [self.compute_entropy()]
            self.elbo_list += [self.E_log_lik_list[-1] + self.E_log_prior_list[-1] + self.entropy_list[-1]]
            # ----- FINISH CURRENT ITERATION -----      
            itr += 1 # increment the iteration counter
            if itr < min_iter: # automatically continue if below the minimum number of iterations
                continue_loop = True
            else: # otherwise, continue if ELBO change is below threshold and we haven't yet hit the iteration limit
                relative_elbo_change = np.abs((self.elbo_list[-2] - self.elbo_list[-1])/self.elbo_list[-2])
                continue_loop = (relative_elbo_change > stop_threshold) and (itr < max_iter)
                
    def compute_E_z(self, nu = None, aS = None, bS = None):
        if aS is None:
            aS = self.aS
        if bS is None:
            bS = self.bS
        if nu is None:
            nu = self.nu
        E_z = nu*aS/bS
        if self.include_intercept:
            E_z = np.append(E_z, np.ones([1, self.n]), axis = 0)
        return E_z
            
    def compute_E_z_sq(self, nu = None, aS = None, bS = None):
        if aS is None:
            aS = self.aS
        if bS is None:
            bS = self.bS
        if nu is None:
            nu = self.nu
        E_S_sq = (aS/(bS**2))*(aS + 1)
        E_z_sq = nu*E_S_sq
        if self.include_intercept:
            E_z_sq = np.append(E_z_sq, np.ones([1, self.n]), axis = 0)
        return E_z_sq
                
    def compute_E_Az_sq(self, nu = None, aS = None, bS = None, mA = None, vA = None):
        '''
        Compute E_q[(A_{j,:} z_{:,i})^2].
        '''
        if aS is None:
            aS = self.aS
        if bS is None:
            bS = self.bS
        if nu is None:
            nu = self.nu
        if mA is None:
            mA = self.mA
        if vA is None:
            vA = self.vA
        E_z = self.compute_E_z(nu, aS, bS)
        E_z_sq = self.compute_E_z_sq(nu, aS, bS)
        E_Az_sq = np.zeros([self.m, self.n])
        for i in range(self.n):
            for j in range(self.m):
                E_Az_sq[j,i] = (vA[j,:] + mA[j,:]**2)@E_z_sq[:,i] + 2*np.sum(mA[j,self.kneql]*mA[j,self.lneqk]*E_z[self.kneql,i]*E_z[self.lneqk,i])
        return E_Az_sq
    
    def compute_E_log_lik(self, aS = None, bS = None, nu = None, tau1 = None, tau2 = None, mA = None, vA = None):
        if aS is None:
            aS = self.aS
        if bS is None:
            bS = self.bS
        if nu is None:
            nu = self.nu
        if tau1 is None:
            tau1 = self.tau1
        if tau2 is None:
            tau2 = self.tau2
        if mA is None:
            mA = self.mA
        if vA is None:
            vA = self.vA
        E_z = self.compute_E_z()
        E_Az_sq = self.compute_E_Az_sq()
        term1 = 0
        for j in range(self.m): # 1st term of E_log_lik
            term1 += self.xi*np.sum(self.mu[j,:]*( (mA[j,:]@E_z)*self.x[j,:] -0.5*self.x[j,:]**2 - 0.5*E_Az_sq[j,:] ))
        term2 = 0.5*np.sum( self.tilde_n*( np.log(self.xi) - np.log(2*np.pi) ) ) # 2nd term of E_log_lik
        return term1 + term2 # this is split into two terms for convenience
    
    def compute_E_log_prior(self, aS = None, bS = None, nu = None, tau1 = None, tau2 = None, mA = None, vA = None):
        if aS is None:
            aS = self.aS
        if bS is None:
            bS = self.bS
        if nu is None:
            nu = self.nu
        if tau1 is None:
            tau1 = self.tau1
        if tau2 is None:
            tau2 = self.tau2
        if mA is None:
            mA = self.mA
        if vA is None:
            vA = self.vA
        E_log_A_prior = -0.5*self.omega*np.sum(vA + mA**2) + 0.5*self.m*self.p*(np.log(self.omega) - np.log(2*np.pi))
        E_log_u_prior = np.sum( (digamma(tau1) - digamma(tau2))*np.sum(nu, axis = 1) + self.n*(digamma(tau2) - digamma(tau1 + tau2)) )
        E_log_S_prior = self.n*self.p*( self.prior_aS*np.log(self.prior_bS) - np.log(gamma(self.prior_aS)) ) + np.sum( (self.prior_aS - 1)*(digamma(aS) - np.log(bS)) - self.prior_bS*aS/bS )
        E_log_pi_prior = (self.alpha/self.p - 1)*np.sum(digamma(tau1) - digamma(tau1 + tau2)) + self.p*np.log(self.alpha/self.p)
        return E_log_A_prior + E_log_u_prior + E_log_S_prior + E_log_pi_prior
    
    def compute_entropy(self, aS = None, bS = None, nu = None, tau1 = None, tau2 = None, mA = None, vA = None):
        if aS is None:
            aS = self.aS
        if bS is None:
            bS = self.bS
        if nu is None:
            nu = self.nu
        if tau1 is None:
            tau1 = self.tau1
        if tau2 is None:
            tau2 = self.tau2
        if mA is None:
            mA = self.mA
        if vA is None:
            vA = self.vA
        H_A = norm_dist.entropy(mA, np.sqrt(vA)).sum()
        H_u = bernoulli_dist.entropy(nu + 1e-16).sum()
        H_S = gamma_dist.entropy(aS + 1e-16, bS + 1e-16).sum()
        H_pi = gamma_dist.entropy(tau1 + 1e-16, tau2 + 1e-16).sum()
        return H_A + H_u + H_S + H_pi