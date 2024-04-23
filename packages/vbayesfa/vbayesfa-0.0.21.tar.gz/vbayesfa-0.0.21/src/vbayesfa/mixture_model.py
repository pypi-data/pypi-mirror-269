import numpy as np
import pandas as pd
import plotnine as p9
from copy import copy
from itertools import combinations, product
from scipy.stats import multinomial as multinomial_dist
from scipy.stats import t as t_dist
from scipy.stats import norm as norm_dist
from scipy.special import digamma, loggamma
from scipy.spatial.distance import pdist, squareform
from abc import ABC, abstractmethod

class mixture_model(ABC):
    '''
    Abstract base class for mixture models.
    '''
    
    def __init__(self, x, T = 20, prior_hpar = None, phi = None, seed = 1234):
        """
        Parameters
        ----------
        x: data frame or array
            Observed data (data frame or matrix).  If a matrix then rows are variables and columns
            are observations; if a data frame then rows are observations and columns are variables.
            Missing values are replaced with 0 for computational reasons.
        T: integer, optional
            The maximum number of latent profiles that can be discovered.
        prior_hpar: dict, optional,
            Prior hyperparameters.
        phi: array or None, optional
            If None (the default) then profile membership probabilities (phi) are randomly
            sampled from a Dirichlet(1, 1, ...) distribution. Otherwise this is an array
            of starting values for phi, with a number columns equal to the number of 
            observations and number of rows equal to or less than T.
        seed: integer, optional
            The seed for random number generation.
        """
        # ----- SET UP SOME VARIABLES -----
        
        if isinstance(x, pd.DataFrame):
            self.x = x.values.copy().transpose()
            self.index = x.index.values
            self.x_names = pd.Categorical(x.columns.values, categories = x.columns.values, ordered = True)
        else:
            self.x = x
            self.index = None
            x_names = ['var ' + str(i) for i in range(self.x.shape[0])] # default variable names
            self.x_names = pd.Categorical(x_names, categories = x_names, ordered = True)
        self.mask = 1 - np.isnan(self.x) # = 1 if not missing, = 0 if missing
        self.x[np.isnan(self.x)] = 0 # this is an arbitrary value to make computations work
        self.n = self.x.shape[1] # number of observations
        self.n_per_var = self.mask.sum(axis = 1) # number of observations for each variable (accounting for missing data)
        self.m = self.x.shape[0] # number of observed variables
        self.T = T
        self.seed = seed
        self.rng = np.random.default_rng(seed = self.seed) # for generating random permutations
        # lists for storing the ELBO and its components at each iteration
        self.E_log_lik_list = []
        self.E_log_prior_list = []
        self.entropy_list = []
        self.elbo_list = []

        # ----- INITIALIZE VARIATIONAL HYPERPARAMETERS -----
        
        # initialize z's hyperparameters
        self.phi = np.zeros([self.T, self.n])
        if phi is None:
            for i in range(self.n):
                self.phi[:,i] = self.rng.dirichlet(self.T*[1.0])
        else:
            self.phi[range(phi.shape[0]),:] = phi
        # initialize variational distribution for likelihood parameters (eta)
        self._initialize_q_eta(prior_hpar)
        # initialize variational distribution over pi (latent class/profile base rates)
        self._initialize_q_pi(prior_hpar)
        
        # ----- OTHER STUFF -----
        self._update_hard_assignment()
    
    def fit(self, tolerance = 1e-05, max_iter = 50, min_iter = 20):
        """
        Parameters
        ----------
        tolerance: float, optional
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
            
            # update variational distribution over z
            for i in range(self.n):
                S = np.zeros(self.T)
                for t in range(self.T):
                    log_lik_term = np.sum(self.mask[:,i]*(self.E_xi_mu[:,t]*self.x[:,i] - 0.5*self.E_xi*self.x[:,i]**2 - 0.5*np.log(2*np.pi) - 0.5*self.E_xi_mu2[:,t] + 0.5*self.E_log_xi))
                    S[t] = self.E_log_pi[t] + log_lik_term
                S_max = np.max(S)
                log_sum_exp_S = S_max + np.log(np.sum(np.exp(S - S_max))) # = log(sum(exp(S))) but uses log-sum-exp trick for numerical accuracy
                log_phi = S - log_sum_exp_S
                self.phi[:,i] = np.exp(log_phi)
                self.phi[:,i] /= self.phi[:,i].sum() # shouldn't need to renormalize, but it helps with some rounding errors in annoying cases
                
            # update variational distribution of pi
            self._update_q_pi()
                    
            # update variational distribution of eta
            self._update_q_eta()

            # ----- COMPUTE ELBO -----
            
            self.E_log_lik_list += [self._E_log_lik()]
            self.E_log_prior_list += [self._E_log_prior_z() + self._E_log_prior_eta() + self._E_log_prior_pi()]
            self.entropy_list += [self._H_q_z() + self._H_q_eta() + self._H_q_pi()]
            self.elbo_list += [self.E_log_lik_list[-1] + self.E_log_prior_list[-1] + self.entropy_list[-1]]
            
            # ----- FINISH CURRENT ITERATION -----      
            
            itr += 1 # increment the iteration counter
            if itr < min_iter: # automatically continue if below the minimum number of iterations
                continue_loop = True
            else: # otherwise, continue if ELBO change is below threshold and we haven't yet hit the iteration limit
                relative_elbo_change = np.abs((self.elbo_list[-2] - self.elbo_list[-1])/self.elbo_list[-2])
                continue_loop = (relative_elbo_change > tolerance) and (itr < max_iter)
                
        # ----- FINISH UP -----
        self._update_hard_assignment()
    
    def _initialize_q_eta(self, prior_hpar):
        '''
        Initialize the variational distribution of eta (likelihood parameters).
        
        Parameters
        ----------
        prior_hpar: dict
            Should contain the following.
            
            lambda_mu: float
                Controls the width of the prior distribution on mu: 
                higher values -> tighter prior around 0.
            strength_for_xi: float
                Controls the strength of the gamma prior distribution on xi.
                This prior is assumed to have a mean of 1, with alpha = prior_strength_for_xi/2
                and beta = prior_strength_for_xi/2.
        '''
        # prior conventional hyperparameters
        self.prior_alpha_xi = 0.5*prior_hpar['strength_for_xi']
        self.prior_beta_xi = 0.5*prior_hpar['strength_for_xi']
        self.prior_m_mu = 0.0
        self.prior_lambda_mu = prior_hpar['lambda_mu']
        # prior natural hyperparameters
        self.prior_tau1 = self.prior_lambda_mu*self.prior_m_mu
        self.prior_tau2 = -self.prior_beta_xi - 0.5*self.T*self.prior_lambda_mu*self.prior_m_mu**2
        self.prior_tau3 = 2*self.prior_alpha_xi + self.T - 2
        self.prior_tau4 = 0.5*self.prior_lambda_mu
        self.h_prior_tau = 0.5*self.T*np.log(2*np.pi) + loggamma(self.prior_alpha_xi) - self.prior_alpha_xi*np.log(self.prior_beta_xi) - 0.5*self.T*np.log(self.prior_lambda_mu) # prior log-normalizer for each of the observed variables
        # set up other variables
        self.tau2 = self.prior_tau2 - 0.5*np.sum(self.mask*self.x**2, axis = 1)
        self.tau3 = self.prior_tau3 + self.n_per_var
        self.tau1 = np.zeros([self.m, self.T])
        self.tau4 = np.zeros([self.m, self.T])
        self.v_mu = np.zeros([self.m, self.T])
        self.E_xi_mu = np.zeros([self.m, self.T])
        self.E_xi_mu2 = np.zeros([self.m, self.T])
        # update based on the variational distribution of z
        self._update_q_eta()
    
    def _update_q_eta(self):
        '''
        Update the variational distribution of eta (likelihood parameters).
        '''
        # update natural hyperparameters (tau)
        for j in range(self.m):
            # tau2 and tau3 don't change, so we don't update them
            for t in range(self.T):
                self.tau1[j,t] = self.prior_tau1 + np.sum(self.mask[j,:]*self.phi[t,:]*self.x[j,:])
                self.tau4[j,t] = self.prior_tau4 + 0.5*np.sum(self.mask[j,:]*self.phi[t,:])      
        
        # convert natural hyperparameters to conventional ones
        self.alpha_xi = 0.5*(self.tau3 - self.T) - 1
        self.beta_xi = -self.tau2 - 0.25*np.sum((self.tau1**2)/self.tau4, axis = 1)
        self.m_mu = 0.5*self.tau1/self.tau4
        self.lambda_mu = 2*self.tau4
        
        # compute relevant expected values etc.
        self.E_xi = self.alpha_xi/self.beta_xi
        self.E_log_xi = digamma(self.alpha_xi) - np.log(self.beta_xi)
        self.h_tau = 0.5*self.T*np.log(2*np.pi) + loggamma(self.alpha_xi) - self.alpha_xi*np.log(self.beta_xi) - 0.5*np.sum(np.log(self.lambda_mu)) # log-normalizer
        for t in range(self.T):
            self.v_mu[:,t] = self.beta_xi/(self.lambda_mu[:,t]*(self.alpha_xi - 1))
            self.E_xi_mu[:,t] = (self.alpha_xi/self.beta_xi)*self.m_mu[:,t]
            self.E_xi_mu2[:,t] = (self.alpha_xi/self.beta_xi)*self.m_mu[:,t]**2 + 1/self.lambda_mu[:,t]
    
    def _H_q_eta(self):
        '''
        Entropy of the variational distribution of eta (likelihood parameters).
        '''
        return np.sum(-np.sum(self.tau1*self.E_xi_mu, axis = 1) - self.tau2*self.E_xi - 0.5*self.tau3*self.E_log_xi + np.sum(self.tau4*self.E_xi_mu2, axis = 1) + self.h_tau)
    
    def _E_log_lik(self):
        '''
        Variational expected value of the log-likelihood.
        '''
        # compute the variational expectation of the total log-likelihood (can make more efficient later)
        E_log_lik = -0.5*np.sum(self.n_per_var)*np.log(2*np.pi) + 0.5*np.sum(self.n_per_var*self.E_log_xi)
        for j in range(self.m):
            E_log_lik += np.sum( self.mask[j,:]*( np.inner(self.E_xi_mu[j,:], self.phi.T)*self.x[j,:] - 0.5*self.E_xi[j]*self.x[j,:]**2 - 0.5*np.inner(self.E_xi_mu2[j,:], self.phi.T) ) )
        return E_log_lik
    
    def _E_log_prior_eta(self):
        '''
        Variational expectation of the log-prior of likelihood parameters (eta).
        '''
        return np.sum(np.sum(self.prior_tau1*self.E_xi_mu, axis = 1) + self.prior_tau2*self.E_xi + 0.5*self.prior_tau3*self.E_log_xi - np.sum(self.prior_tau4*self.E_xi_mu2, axis = 1) - self.h_prior_tau)
    
    @abstractmethod
    def _initialize_q_pi(self, prior_hpar):
        '''
        Initialize the variational distribution of latent class/profile base rates (pi).
        '''
        pass
    
    @abstractmethod
    def _update_q_pi(self):
        '''
        Update the variational distribution of latent class/profile base rates (pi).
        '''
        pass
    
    @abstractmethod
    def _H_q_pi(self):
        '''
        Entropy of the variational distribution of latent class/profile base rates (pi).
        '''
        pass
    
    @abstractmethod
    def _E_log_prior_pi(self):
        '''
        Variational expectation of the log-prior of latent class/profile base rates (pi).
        '''
        pass
    
    def _H_q_z(self):
        '''
        Entropy of the variational distribution over z (profile membership).
        '''
        #H = 0.0
        #for i in range(self.n):
        #    H += multinomial_dist.entropy(1, self.phi[:,i])
        #return H
        return np.sum([multinomial_dist.entropy(1, self.phi[:,i]) for i in range(self.n)])
    
    def _E_log_prior_z(self):
        '''
        Variational expectation of the log-prior on profile membership (z).
        '''
        # UPDATE
        #E_log_z_prior = 0.0
        #for t in range(self.T): # this is taken from page 129 of Blei and Jordan (2006)
        #    q_z_greater_than_t = np.sum(self.phi[range(t+1, self.T), :], axis = 0)
        #    E_log_z_prior += np.sum(q_z_greater_than_t*self.E_log_1minusV[t] + self.phi[t,:]*self.E_log_V[t])
        #return E_log_z_prior
        return np.sum([self.phi[t,:]*self.E_log_pi[t] for t in range(self.T)])
    
    def _update_hard_assignment(self):
        # figure out which profiles are non-empty and sort them by count
        unsorted_z_hat = self.phi.argmax(axis = 0) # unsorted point estimates of z (hard assignment)
        unsorted_z_hat_1hot = np.zeros(self.phi.shape)
        for t in range(self.T):
            unsorted_z_hat_1hot[t, unsorted_z_hat == t] = 1.0
        unsorted_counts = unsorted_z_hat_1hot.sum(axis = -1)
        self.n_profiles = np.sum(unsorted_counts > 0) # number of non-empty profiles
        self.profile_order = np.argsort(unsorted_counts)[::-1][range(self.n_profiles)]
        
        # create sorted versions of phi, m_mu etc. that only include non-empty profiles
        self.sorted_phi = self.phi[self.profile_order, :]
        self.sorted_m_mu = self.m_mu[:, self.profile_order]
        self.sorted_v_mu = self.v_mu[:, self.profile_order]
        
        # sorted point estimates of z
        self.z_hat = self.sorted_phi.argmax(axis = 0) # point estimates of z (hard assignment)
        self.z_hat_1hot = np.zeros(self.sorted_phi.shape) # 1-hot matrix of profile assignment
        for t in range(self.n_profiles):
            self.z_hat_1hot[t, self.z_hat == t] = 1.0
        self.n_per_profile = self.z_hat_1hot.sum(axis = -1) # count how many people are in each profile
        self.prop_per_profile = self.n_per_profile/self.n # proportion of people in each profile
    
    def profile_similarity(self, figure_size = (6, 5), font_size = 11, start_profile_labels_from1 = False):
        '''
        Computes pairwise distance and similarity between latent profiles.
        
        Parameters
        ----------
        figure_size: list of floats, optional
            Size of plots.
        font_size: integer, optional
            Font size for plots.
        start_profile_labels_from1: boolean, optional
            Whether to label latent profiles starting from 0 (Python style)
            or from 1 (R/Matlab/ordinary counting style). This only affects
            output labeling, not any calculations.
        
        Returns
        -------
        A dict with the following data:
            
        similarity:
            Similarity between profiles.
        distance:
            Distance between profiles.
        max_similarity:
            Maximum similarity across all profile pairs.
        most_similar_pair: 
            Most similar pair of profiles.
        mean_similarity:
            Mean similarity across all profile pairs.
        min_distance:
            Minimum distance across all profile pairs (corresponds to maximum similarity).
        mean_distance:
            Mean distance across all profile pairs.
        plot:
            Plot of the profile means of the most similar two profiles.
            
        Notes
        -----
        This computes the Euclidean distance between each pair of profile means
        (m_mu) and converts it to a similarity measure as follows:
        
        squared_distance = sum(E_xi*(m_mu[:,j] - m_mu[:,k])^2)
        similarity = exp(-0.5*squared_distance)
        
        Two profiles with identical means will thus have a similarity of 1,
        while highly dissimilar profiles will have a similarity near 0.
        
        Distances are scaled by the estimated precision (E_xi) of each data
        dimension, so that variables with lower variances (higher E_xi) are
        given more weight.
        
        This similarity metric is proportional to the likelihood from each
        latent profile of the most typical (modal = mean) data point corresponding
        to each other latent profile (it is a diagonal multivariate normal density
        without the normalizing term).
        
        Profiles are numbered according to profile_order in the output, i.e.
        the profile with the largest estimated membership/base rate (pi)
        will be 0, the profile with the next largest membership will be 1
        etc.
        '''
        # compute similarity
        squared_distance = pdist(self.sorted_m_mu.T, metric = 'seuclidean', V = 1/self.E_xi)**2 # distances, scaled by estimated precision (E_xi)
        similarity = np.exp(-0.5*squareform(squared_distance)) # similarity matrix
        similarity_off_diag = similarity - 999*np.eye(similarity.shape[0]) # - 999*np.eye(similarity.shape[0]) effectively excludes the diagonal of the similarity matrix, which represents self-similarity (always 1)
        most_similar_pair = np.unravel_index(np.argmax(similarity_off_diag), similarity.shape) # find the most similar pair of profiles
        similarity_vector = np.exp(-0.5*squared_distance) # similarity vector (for taking the mean without redundant values)
        
        # make a plot of the two most similar profiles
        plot_df = pd.DataFrame({'mu': np.concatenate([self.sorted_m_mu[:, most_similar_pair[0]], self.sorted_m_mu[:, most_similar_pair[1]]]), 
                                'profile': self.m*['profile ' + str(most_similar_pair[0] + start_profile_labels_from1)] + self.m*['profile ' + str(most_similar_pair[1] + start_profile_labels_from1)], 
                                'variable': pd.Categorical(2*list(self.x_names), categories = self.x_names, ordered = True)})
        plot = p9.ggplot(plot_df, p9.aes(x = 'variable', y = 'mu')) + p9.geom_bar(stat = 'identity')
        plot += p9.theme_classic(base_size = font_size) + p9.theme(figure_size = figure_size, axis_text_x = p9.element_text(rotation = 90, hjust = 1))
        plot += p9.facet_wrap('profile', scales = 'free_x', ncol = 2)
        
        return {'similarity': similarity, 'distance': np.sqrt(squareform(squared_distance)), 'max_similarity': similarity_off_diag.max(), 'most_similar_pair': most_similar_pair, 'mean_similarity': np.mean(similarity_vector), 'min_distance': np.min(np.sqrt(squared_distance)), 'mean_distance': np.mean(np.sqrt(squared_distance)), 'plot': plot}            
    
    def classify_new_data(self, x_new):
        '''        
        Compute the (approximate) probability of new data points belonging to
        each profile given the model's current variational parameters.
        
        Parameters
        ----------
        x_new: data frame or array
            Observed data (data frame or matrix).  If a matrix then rows are variables and columns
            are observations; if a data frame then rows are observations and columns are variables.
            Missing values are replaced with 0 for computational reasons.
            
        Returns
        -------
        A dict with the following.
        
        phi: array
            Estimated probabilities of profile membership (phi), NOT sorted by profile membership counts.
        phi_sorted: array
            The same as phi, but sorted by profile membership counts.
        z_hat: array
            Point estimates of profile membership, with profiles labeled in order of
            profile membership counts.
        '''
        # set up variables
        if isinstance(x_new, pd.DataFrame):
            x_new = x_new.values.transpose()
        mask_new = 1 - np.isnan(x_new) # = 1 if not missing, = 0 if missing
        x_new[np.isnan(x_new)] = 0 # this is an arbitrary value to make computations work
        n_new = x_new.shape[1] # number of observations
        n_per_var_new = mask_new.sum(axis = 1) # number of observations for each variable (accounting for missing data)
        
        # compute log posterior predictive terms
        log_post_pred = np.zeros([self.m, self.T, n_new])
        for j in range(self.m):
            for t in range(self.T):
                # https://en.wikipedia.org/wiki/Conjugate_prior#When_likelihood_function_is_a_continuous_distribution ** DOUBLE CHECK THIS **
                t_dist_sd = np.sqrt(self.beta_xi[j]*(self.lambda_mu[j, t] + 1)/(self.alpha_xi[j]*self.lambda_mu[j, t]))
                log_post_pred[j, t, :] = t_dist.logpdf(x_new[j, :],
                                                       df = 2*self.alpha_xi[j],
                                                       loc = self.m_mu[j, t],
                                                       scale = t_dist_sd)
                log_post_pred[j, t, :] *= mask_new[j, :]
        
        # run the calculation
        phi_new = np.zeros([self.T, n_new])
        for i in range(n_new):
            S = np.zeros(self.T)
            for t in range(self.T):
                S[t] = np.log(self.E_pi[t]) + np.sum(log_post_pred[:, t, i])
            S_max = np.max(S)
            log_sum_exp_S = S_max + np.log(np.sum(np.exp(S - S_max))) # = log(sum(exp(S))) but uses log-sum-exp trick for numerical accuracy
            log_phi_new = S - log_sum_exp_S
            phi_new[:, i] = np.exp(log_phi_new)/np.exp(log_phi_new).sum()
            
        # create sorted version of phi_new that only includes non-empty profiles
        sorted_phi_new = phi_new[self.profile_order, :]
        # sorted point estimates of z
        z_hat_new = sorted_phi_new.argmax(axis = 0) # point estimates of z (hard assignment)
            
        return {'phi': phi_new, 'sorted_phi': sorted_phi_new, 'z_hat': z_hat_new}
    
    def print_summary(self, start_profile_labels_from1 = False):
        '''
        Display information about the model.
        
        Parameters
        ----------
        start_profile_labels_from1: boolean, optional
            Whether to label latent profiles starting from 0 (Python style)
            or from 1 (R/Matlab/ordinary counting style). This only affects
            output labeling, not any calculations.
        '''
        print('n = ' + str(self.n))
        
        H_z = 0.0
        for i in range(self.n):
            H_z += multinomial_dist.entropy(1, self.phi[:,i]) # using the entropy function avoids problems with very small logs
        max_H_z = self.n*np.log(self.T)
        print('\nM-Plus style entropy statistic: ' + str(np.round(1 - H_z/max_H_z, 2)))
        print('(= 1 - entropy of z/max entropy of z)')
        # see http://www.statmodel.com/download/UnivariateEntropy.pdf
        
        print('\nnumber of non-empty profiles: ' + str(self.n_profiles))
        if start_profile_labels_from1:
            profile_names = ['profile ' + str(i + 1) for i in range(self.n_profiles)]
        else:
            profile_names = ['profile ' + str(i) for i in range(self.n_profiles)]
        print('\npi (profile probabilties): ')
        print(np.round(pd.DataFrame(self.prop_per_profile, index = profile_names, columns = ['']).T, 2))
        print('\nnumber in each profile: ')
        print(pd.DataFrame(self.n_per_profile.astype(int), index = profile_names, columns = ['']).T)
        #print('\nalpha (concentration parameter): ' + str(np.round(self.E_alpha, 2)))
        print('\nmu: (means)')
        print(np.round(pd.DataFrame(self.sorted_m_mu, index = self.x_names, columns = profile_names), 2))
        print('\nxi: (precisions, i.e. inverse variances)')
        print(np.round(pd.DataFrame(self.E_xi, index = self.x_names, columns = ['']).T, 2))
        
        print('\nproportion of the sample contained in the K biggest profiles')
        print(np.round(pd.DataFrame(self.prop_per_profile.cumsum(),
                                    index = ['K = ' + str(K) for K in np.arange(self.n_profiles) + 1],
                                    columns = ['']).T,
                       2))
    
    def print_univariate_entropy_stats(self):
        '''
        Compute and print M-Plus style univariate entropy statistics.
        '''
        print('\nM-Plus style univariate entropy statistics')
        print('(= 1 - entropy of z given x[j,:]/max entropy of z)')
        univariate_H_z = np.zeros(self.m)
        for j in range(self.m):
            for i in range(self.n):
                S = np.zeros(self.T)
                for t in range(self.T):
                    log_lik_term = self.mask[j,i]*self.E_xi_mu[j,t]*self.x[j,i] - 0.5*self.E_xi[j]*self.x[j,i]**2 - 0.5*np.log(2*np.pi) - 0.5*self.E_xi_mu2[j,t] + 0.5*self.E_log_xi[j]
                    S[t] = self.E_log_pi[t] + log_lik_term
                S_max = np.max(S)
                log_sum_exp_S = S_max + np.log(np.sum(np.exp(S - S_max)))
                log_phi_given_xj = S - log_sum_exp_S
                phi_given_xj = np.exp(log_phi_given_xj)
                phi_given_xj /= phi_given_xj.sum()
                univariate_H_z[j] += multinomial_dist.entropy(1, phi_given_xj)
        max_H_z = self.n*np.log(self.T)
        univariate_entropy_stat = 1 - univariate_H_z/max_H_z
        print(np.round(pd.DataFrame(univariate_entropy_stat, index = self.x_names, columns = ['']).T, 2))
    
    def compute_x_hat(self):
        '''
        Compute posterior mean predicted observations (x_hat).
        
        Returns
        -------
        Posterior mean predicted observations.
        '''
        return np.inner(self.m_mu, self.phi.T)
    
    def compute_residuals(self):
        '''
        Compute and residuals (actual observations - posterior mean predicted observations).
        
        Returns
        -------
        A data frame of residuals.
        
        Notes
        -----
        Technically the residuals are random variables (because we're doing Bayesian stats)
        and we are computing their means.
        '''
        x_hat = self.compute_x_hat() # predicted observations
        resid = self.x - x_hat
        return pd.DataFrame(resid.T, columns = self.x_names)
    
    def plot_residuals(self, figure_size = (6, 5), font_size = 11, ncol = 4, bins = 20):
        '''
        Plot residuals (actual observations - posterior mean predicted observations).
        
        Parameters
        ----------
        figure_size: list of floats, optional
            Size of plots.
        font_size: integer, optional
            Font size for plots.
        ncol: integer, optional
            Number of columns to use in plots.
        bins: integer, optional
            Number of bins for histograms.
            
        Returns
        -------
        Plots of residual histograms, facetted by variable.
        
        Notes
        -----
        Technically the residuals are random variables (because we're doing Bayesian stats)
        and we are plotting their means.
        
        This plots a density histogram of residuals for each variable, plus the corresponding
        normal distribution (same mean and variance as the residuals) for comparison (as a
        blue line).
        '''
        # create histograms of residuals
        rdf = self.compute_residuals().stack().to_frame().reset_index().rename(columns = {'level_0': 'i', 'level_1': 'variable', 0: 'residuals'})
        plot = p9.ggplot(rdf, p9.aes(x = 'residuals', y = p9.after_stat('density')))
        plot += p9.geom_histogram(bins = bins, fill = 'gray')
        plot += p9.facet_wrap('variable', scales = 'free', ncol = ncol)
        plot += p9.theme_classic(base_size = font_size) + p9.theme(figure_size = figure_size)
        
        # add normal density plots for comparison
        r_values = np.arange(-3, 3, step = 0.01)
        pdf_df_list = []

        for var in self.x_names:
            r = rdf.loc[rdf['variable'] == var, 'residuals']
            m = r.mean()
            s = r.std()
            norm_pdf = norm_dist.pdf(r_values, m, s)
            pdf_df_list += [pd.DataFrame({'variable': var, 'x': r_values, 'norm_pdf': norm_pdf})]
        pdf_df = pd.concat(pdf_df_list)
        plot += p9.geom_line(p9.aes(x = 'x', y = 'norm_pdf'), data = pdf_df, color = 'blue')
        
        return plot
    
    def residual_correlations(self, round_decimal = 2):
        '''
        Compute correlations of data residuals 
        (actual observations - posterior mean predicted observations).
        
        Parameters
        ----------
        round_decimal: int or None, optional
            If an integer, then the number of places to round the
            correlation matrix. If None, then the matrix is not rounded.
            The default of two decimal places is there purely for convenience.
        
        Returns
        -------
        Correlation matrix of data residuals.
        
        Notes
        -----
        Latent profile analysis assumes local independence, i.e. given latent
        profile membership, indicator variables (x) are uncorrelated. To test this
        assumption, we can look at the correlations of data residuals. If local
        independence is a valid assumption, then these should be uncorrelated, i.e.
        the correlation matrix should have 1s on the diagonal and 0s everywhere else.
        
        If the local independence assumption is not valid (as indicated by non-zero 
        residual correlations), then there is a risk of extracting too many latent profiles.
        There are two options:
        1) Drop one of the indicator variables (x) with residual correlations that are too high.
        2) Switch from pure latent profile analysis to a model without the local independence 
        assumption, e.g. a factor mixture model.        
        '''
        if round_decimal is None:
            cor_matrix = self.compute_residuals().corr()
        else:
            cor_matrix = np.round(self.compute_residuals().corr(), round_decimal)
        return cor_matrix
    
    def plot_profile_probs(self, figure_size = (6, 5), font_size = 11, start_profile_labels_from1 = False):
        '''
        Plot estimated profile probabilities (pi).
        
        Returns
        -------
        A bar plot of estimated latent profile probabilities.
        
        Parameters
        ----------
        figure_size: list of floats, optional
            Size of plots.
        font_size: integer, optional
            Font size for plots.
        start_profile_labels_from1: boolean, optional
            Whether to label latent profiles starting from 0 (Python style)
            or from 1 (R/Matlab/ordinary counting style). This only affects
            output labeling, not any calculations.
        '''
        plot_df = pd.DataFrame({'profile': range(self.n_profiles),
                                'pi': self.prop_per_profile})
        if start_profile_labels_from1:
            plot_df['profile'] += 1
        plot_df['profile'] = plot_df['profile'].astype('string')
        plot = p9.ggplot(plot_df, p9.aes(x = 'profile', y = 'pi')) + p9.geom_bar(stat = 'identity')
        plot += p9.theme_classic(base_size = font_size)
        plot += p9.theme(figure_size = figure_size)
        return plot
    
    def plot_profile_means(self, figure_size = (6, 5), font_size = 11, kind = 'bar', facet_var = 'profile', ncol = 4, fancy_labels = True, start_profile_labels_from1 = False):
        '''
        Plot latent profile means.
        
        Parameters
        ----------
        figure_size: list of floats, optional
            Size of plots.
        font_size: integer, optional
            Font size for plots.
        kind: string, optional
            Type of plot. Options are 'bar', 'point', and 'point_and_errorbar'.
        facet_var: string, optional
            Faceting variable for plots.
        ncol: integer, optional
            Number of columns to use in plots.
        fancy_labels: boolean, optional
            If True, then profile labels are formatted like "profile 2 (19%)",
            giving the percent of people/observations in that profile.
        start_profile_labels_from1: boolean, optional
            Whether to label latent profiles starting from 0 (Python style)
            or from 1 (R/Matlab/ordinary counting style). This only affects
            output labeling, not any calculations.
            
        Returns
        -------
        Plots of profile means.
        '''
        # make a dataframe for plot data
        plot_df = pd.DataFrame(product(range(self.m), range(self.n_profiles)),
                               columns = ['j', 'profile'])
        plot_df['variable'] = self.x_names[plot_df['j'].values]
        plot_df['mu'] = 0.0
        plot_df['v'] = 0.0
        plot_df['mu_minus'] = 0.0
        plot_df['mu_plus'] = 0.0
        for r in range(plot_df.shape[0]):
            plot_df.loc[r, 'mu'] = self.sorted_m_mu[plot_df.iloc[r]['j'], plot_df.iloc[r]['profile']]
            plot_df.loc[r, 'v'] = self.sorted_v_mu[plot_df.iloc[r]['j'], plot_df.iloc[r]['profile']]
        plot_df['mu_minus'] = plot_df['mu'] - 1.96*np.sqrt(plot_df['v'])
        plot_df['mu_plus'] = plot_df['mu'] + 1.96*np.sqrt(plot_df['v'])
        if fancy_labels and facet_var == 'profile':
            # add information about pi (i.e. how many data points are in the profile) to labels
            pct_for_labels = np.round(100*self.prop_per_profile).astype(int) # pi, represented as percentages
            pct_info_list = [ ' (' + str(pct_for_labels[plot_df['profile'][r]]) + '%)' for r in range(plot_df.shape[0])]
            if start_profile_labels_from1:
                plot_df['profile'] += 1
            plot_df['profile'] = plot_df['profile'].astype('string')
            plot_df['profile'] = plot_df['profile'].str.cat(pct_info_list) # add pi information (as percentages)
            plot_df['profile'] = 'profile ' + plot_df['profile'] # add the word 'profile'
            plot_df['profile'] = pd.Categorical(plot_df['profile'].values, 
                                                categories = plot_df['profile'].values[range(self.n_profiles)], 
                                                ordered = True)
            
        else:
            if start_profile_labels_from1:
                plot_df['profile'] += 1
            plot_df['profile'] = plot_df['profile'].astype('string')
            plot_df['profile'] = pd.Categorical(plot_df['profile'].values, 
                                                categories = plot_df['profile'].values[range(self.n_profiles)], 
                                                ordered = True)
        
        # make the plot
        if facet_var == 'profile':
            plot = p9.ggplot(plot_df, p9.aes(x = 'variable', y = 'mu', ymin = 'mu_plus', ymax = 'mu_minus'))
        elif facet_var == 'variable':
            plot = p9.ggplot(plot_df, p9.aes(x = 'profile', y = 'mu', ymin = 'mu_plus', ymax = 'mu_minus'))
        
        if kind == 'bar':
            plot += p9.geom_bar(stat = 'identity')
        elif kind == 'point':
            plot += p9.geom_point()
            plot += p9.geom_hline(yintercept = 0, linetype = 'dashed')
        elif kind == 'point_and_errorbar':
            plot += p9.geom_point()
            plot += p9.geom_errorbar()
            plot += p9.geom_hline(yintercept = 0, linetype = 'dashed')
        plot += p9.theme_classic(base_size = font_size)
        plot += p9.theme(figure_size = figure_size)
        
        if facet_var == 'profile':
            plot += p9.facet_wrap('profile', scales = 'free_x', ncol = ncol)
            plot += p9.theme(axis_text_x = p9.element_text(rotation = 90, hjust = 1))
        elif facet_var == 'variable':
            plot += p9.facet_wrap('variable', scales = 'free_x', ncol = ncol)
        
        return plot