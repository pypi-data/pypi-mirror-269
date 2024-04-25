import numpy as np
import pandas as pd
import plotnine as p9
from itertools import product
from scipy.stats import beta as beta_dist
from scipy.stats import t as t_dist
from . import bayes_factors
from . import exp_families
from scipy.special import betaln

def _remove_nan(y, z):
    '''
    Convenience function to remove observations with missing data.
    '''
    is_nan = np.isnan(y)
    if np.sum(is_nan) > 0:
        y = y[~is_nan].copy()
        z = z[:, ~is_nan].copy()
    return (y, z)

def fit_y_normal(model,
                 y,
                 x_new = None,
                 y_new = None,
                 index = None,
                 profile_labels = None,
                 start_profile_labels_from1 = False,
                 prior_alpha = 1.0,
                 prior_beta = 1.0,
                 prior_m = 0.0,
                 prior_lambda = 1.0,
                 figure_size = [10, 12],
                 font_size = 11,
                 facet_var = 'variable',
                 ncol = 4):
    '''
    Analyze the relationship between dependent variables (y) -
    that are assumed to be normally distributed - and the profiles.
    This is done without changing the model's other variational parameters.
    
    Parameters
    ----------
    model: LPA model
        The fitted LPA model.
    y: dataframe
        Outcome data.
    x_new:
        New LPA model data (from participants not used to fit the LPA model).
    y_new: dataframe
        New outcome data (from participants not used to fit the LPA model).
    index: array-like, optional
        Optional individual participant/observation labels.
    profile_labels: array-like, optional
        Optional labels for latent profiles.
    start_profile_labels_from1: boolean, optional
        Whether to label latent profiles starting from 0 (Python style)
        or from 1 (R/Matlab/ordinary counting style). This only affects
        output labeling, not any calculations.
    prior_alpha: float, optional
        Prior alpha parameter.
    prior_beta: float, optional
        Prior beta parameter.
    prior_m: float, optional
        Prior m parameter.
    prior_lambda: float, optional
        Prior lambda parameter.
    figure_size: list of floats, optional
        Size of plots.
    font_size: integer, optional
        Font size for plots.
    facet_var: string, optional
        Faceting variable for plots.
    ncol: integer, optional
        Number of columns to use in plots.
        
    Returns
    -------
    A dict with the following data:
    
    plot: plot
        A plot displaying 95% posterior credible intervals of group means for each outcome variable.
    plot_df: dataframe
        Table of statistics used to create the plot.
    bayes_factors: dataframe
        Table of Bayesian 1-way ANOVA results.
            bf10: Bayes factor for comparing H1 (all latent profiles have different means) to H0 (all latent profiles have the same mean).
            log10_bf10: The base-10 logarithm of the above (this is easier to interpret).
            post_hoc_result: The best partition of latent profiles into sets with equal means within each set and different means between sets. This is the result of post-hoc analysis, which is performed only when log10_bf10 > *ASDF* (indicating substantial evidence for H1 according to the criteria of *REF*).
    r2: series
        Coefficient of determination (r^2) for each outcome, based on LPA categorization of participants/
        observations.
    post_hpar: dataframe
        Posterior hyperparameters of each outcome for each latent profile.
        
    Notes
    -----
    
    Outcome means/variances are given a normal-gamma prior distribution with the specified hyperparameters (prior alpha,
    prior_beta, prior_m, and prior_lambda).
    
    All calculations relating latent profiles to outcome variables (y) use hard assignment of participants/observations
    to latent profiles, i.e. each participant is assigned to their most probable profile, which is then treated as known.
    
    Outcome variance is treated as shared across profiles in computing the Bayes factors, but not when computing posterior
    hyperparameters or r^2. This does not seem to make much practical difference, but is an inconsistency that could be changed
    later.
    
    Currently y_new and x_new are not used. In a previous version, they were used to compute r^2 values for observations/
    participants that had not been used in fitting either the LPA model or the outcome variable relationship. This
    provided a measure of out of sample generalization of outcome relationships. This should be added back into a future version.
    
    *UPDATE THIS LAST POINT*
    In a future version, we should change the Bayes factors to perform Rouder et al Bayesian ANOVA calculations
    rather than the somewhat naive versions I've used here. Also, the pairwise mean comparisons should be replaced with
    a partition-based post-hoc analysis as described in our paper.
    '''
    ##### SET UP DATA ETC #####
    y_names = pd.Categorical(y.columns.values, categories = y.columns.values, ordered = True)
    if index is None:
        y = y.copy()
    else:
        y = y.iloc[index].copy().transpose()
    n_y = y.shape[1] # number of dependent variables
        
    bayes_factor_df = pd.DataFrame(columns = ['bf10', 'log10_bf10', 'conclusion', 'post_hoc_result'],
                                   index = y_names) # empty dataframe for results
    
    ##### COMPUTE BAYES FACTORS (BAYESIAN ANOVAS) #####
    for j in range(n_y):
        y_j = y[y_names[j]].values
        bayes_factor_df.loc[y_names[j], 'bf10'] = bayes_factors.bf10_1way_anova(y = y_j, groups = model.z_hat, rscale = 0.5, epsrel = 1e-4, limit = 50)
        bayes_factor_df.loc[y_names[j], 'log10_bf10'] = np.log10(bayes_factor_df.loc[y_names[j], 'bf10'])
        if bayes_factor_df.loc[y_names[j], 'log10_bf10'] > 0.5:
            bayes_factor_df.loc[y_names[j], 'conclusion'] = 'profile means differ'
            bayes_factor_df.loc[y_names[j], 'post_hoc_result'] = bayes_factors.partition_posthoc(y = y_j, groups = model.z_hat, rscale = 0.5, epsrel = 1e-4, limit = 50)['best_partition'] # post-hoc analysis (partition-based)
        elif bayes_factor_df.loc[y_names[j], 'log10_bf10'] < 0.5:
            bayes_factor_df.loc[y_names[j], 'conclusion'] = 'profile means ='
        else:
            bayes_factor_df.loc[y_names[j], 'conclusion'] = 'indecisive'
    
    ##### POSTERIOR HYPERPARAMETERS #####
    post_hpar = {'m': np.zeros([n_y, model.n_profiles]), 'lambda': np.zeros([n_y, model.n_profiles]), 'alpha': np.zeros(n_y), 'beta': np.zeros(n_y)}
    v_mu = np.zeros([n_y, model.n_profiles])
    for j in range(n_y):
        (y_j, z_hat_j) = _remove_nan(y[y_names[j]].values, model.z_hat_1hot)
        dist = exp_families.multi_group_normal({'m': prior_m, 'lambda': prior_lambda, 'alpha': prior_alpha, 'beta': prior_beta}, model.n_profiles)
        dist.update(y_j, z_hat_j)
        post_hpar['m'][j,:] = dist.hpar['m']
        post_hpar['lambda'][j,:] = dist.hpar['lambda']
        post_hpar['alpha'][j] = dist.hpar['alpha']
        post_hpar['beta'][j] = dist.hpar['beta']
        v_mu[j, :] = dist.hpar['beta']/(dist.hpar['lambda']*(dist.hpar['alpha'] - 1))
    
    ##### COMPUTE THE COEFFICIENT OF DETERMINATION (R^2) #####
    r2 = pd.Series(0.0, index = y_names)
    for j in range(n_y):
        (y_j, z_hat_j) = _remove_nan(y[y_names[j]].values, model.z_hat_1hot)
        y_hat = np.inner(post_hpar['m'][j, :], z_hat_j.T)
        ss_residuals = np.sum((y_j - y_hat)**2)
        ss_total = np.sum((y_j - np.mean(y_j))**2)
        r2[y_names[j]] = 1 - ss_residuals/ss_total
    
    ##### MAKE PLOT #####
    plot_df = pd.DataFrame(product(range(n_y), range(model.n_profiles)),
                                columns = ['j', 'profile'])
    plot_df['variable'] = y_names[plot_df['j'].values]
    plot_df['mu'] = 0.0
    plot_df['v'] = 0.0
    hard_m_mu = np.zeros([n_y, model.n_profiles])
    hard_v_mu = np.zeros([n_y, model.n_profiles])
    for r in range(plot_df.shape[0]):
        plot_df.loc[r, 'mu'] = post_hpar['m'][plot_df.iloc[r]['j'].astype(int), plot_df.iloc[r]['profile'].astype(int)]
        plot_df.loc[r, 'v'] = v_mu[plot_df.iloc[r]['j'].astype(int), plot_df.iloc[r]['profile'].astype(int)]
    plot_df['mu_minus'] = plot_df['mu'] - 1.96*np.sqrt(plot_df['v'])
    plot_df['mu_plus'] = plot_df['mu'] + 1.96*np.sqrt(plot_df['v'])
    if start_profile_labels_from1:
        plot_df['profile'] += 1
    plot_df['profile'] = plot_df['profile'].astype('string')
    
    if facet_var == 'profile':
        if profile_labels is None:
            plot = p9.ggplot(plot_df, p9.aes(x = 'variable', y = 'mu', ymin = 'mu_minus', ymax = 'mu_plus'))
        else:
            plot = p9.ggplot(plot_df, p9.aes(shape = 'profile label', x = 'variable', y = 'mu', ymin = 'mu_minus', ymax = 'mu_plus'))
    elif facet_var == 'variable' or n_y == 1:
        if profile_labels is None:
            plot = p9.ggplot(plot_df, p9.aes(x = 'profile', y = 'mu', ymin = 'mu_minus', ymax = 'mu_plus'))
        else:
            plot = p9.ggplot(plot_df, p9.aes(shape = 'profile label', x = 'profile', y = 'mu', ymin = 'mu_minus', ymax = 'mu_plus'))

    plot += p9.geom_point()
    plot += p9.geom_errorbar()
    plot += p9.theme_classic(base_size = font_size)
    plot += p9.theme(figure_size = figure_size)
    if not profile_labels is None:
        plot += p9.scale_shape_manual(values = len(profile_labels)*["o"]) # this is just a hack to display the legend (we don't want different shapes) 
        
    if n_y > 1:
        if facet_var == 'profile':
            plot += p9.facet_wrap('profile', scales = 'free_x', ncol = ncol)
        elif facet_var == 'variable':
            plot += p9.facet_wrap('variable', scales = 'free', ncol = ncol)
    
    ##### OUTPUT #####
    output = {'plot': plot, 'plot_df': plot_df, 'bayes_factors': bayes_factor_df, 'r2': r2, 'post_hpar': post_hpar}
    
#    if not y_new is None:
        # TOTALLY REVISE THIS
        ##### GET THE APPROXIMATE LOG POSTERIOR PREDICTIVE (p(y | x)) AND PREDICTED MEAN FOR NEW DATA #####
#        n_new = y_new.shape[0]
#        log_post_pred = pd.DataFrame(0.0, index = y_new.index, columns = y_new.columns)
#        post_pred_mean = pd.DataFrame(0.0, index = y_new.index, columns = y_new.columns)
#        phi_new = model.classify_new_data(x_new) # approximately p(z_new = t | x_new, old data)
#        for j in range(n_y):
#            var = y_new.columns[j]
#            post_pred_by_profile = np.zeros([model.T, n_new])
#            for t in range(model.T):
                # https://en.wikipedia.org/wiki/Conjugate_prior#When_likelihood_function_is_a_continuous_distribution ** DOUBLE CHECK THIS **
#                t_dist_sd = np.sqrt(beta[j]*(lamb[j, t] + 1)/(alpha[j]*lamb[j, t]))
#                post_pred_by_profile[t, :] = t_dist.pdf(y_new.loc[:, var],
#                                                        df = 2*alpha[j],
#                                                        loc = m[j, t],
#                                                        scale = t_dist_sd)
#            log_post_pred.loc[:, var] = np.log(np.sum(post_pred_by_profile*phi_new, axis = 0))
#            post_pred_mean.loc[:, var] = np.inner(m[j, :], phi_new.T)
            
        ##### COMPUTE THE PREDICTIVE COEFFICIENT OF DETERMINATION #####
#        predictive_r2 = pd.Series(0.0, index = y_names)
#        for var in y_names:
#            ss_residuals = np.sum((y_new[var] - post_pred_mean[var])**2)
#            ss_total = np.sum((y_new[var] - y_new[var].mean())**2)
#            predictive_r2[var] = 1 - ss_residuals/ss_total

#        output['predictive_r2'] = predictive_r2 # TOTALLY REVISE THIS
    return output
    
def fit_y_bernoulli(model, 
                    y,
                    index = None,
                    profile_labels = None,
                    start_profile_labels_from1 = False,
                    prior_a = 0.5,
                    prior_b = 0.5,
                    y_names = None, 
                    figure_size = [10, 8], 
                    font_size = 11, 
                    facet_var = 'variable', 
                    ncol = 4):
    '''
    Analyze the relationship between dependent variables (y) -
    that are assumed to be Bernoulli distributed - and the profiles.
    This is done without changing the model's other variational parameters.
    
    Parameters
    ----------
    model: LPA model
        The fitted LPA model.
    y: dataframe
        Outcome data.
    index: array-like, optional
        Optional individual participant/observation labels.
    profile_labels: array-like, optional
        Optional labels for latent profiles.
    start_profile_labels_from1: boolean, optional
        Whether to label latent profiles starting from 0 (Python style)
        or from 1 (R/Matlab/ordinary counting style). This only affects
        output labeling, not any calculations.
    prior_a: float, optional
        Prior a parameter.
    prior_b: float, optional
        Prior b parameter.
    figure_size: list of floats, optional
        Size of plots.
    font_size: integer, optional
        Font size for plots.
    facet_var: string, optional
        Faceting variable for plots.
    ncol: integer, optional
        Number of columns to use in plots.
    
    Returns
    -------
    A dict with the following data:
    
    plot: plot
        A plot displaying 95% posterior credible intervals of psi (outcome probability) for each outcome variable.
    plot_df: dataframe
        Table of statistics used to create the plot.
    bayes_factors: dataframe
        Table of Bayes factors, posterior Bayes factors, and fractional Bayes factors testing
        equality of group outcome means.
    log10_bayes_factors: dataframe
        The Bayes factor table in base-10 logarithmic scale.
    pairwise_log10_frac_bf10: dataframe
        Table of pairwise Bayes factors testing equality of means between groups, in log-10 scale.
    bss: series
        Brier skill scores for each outcome (a measure of effect size similar to r^2), based on LPA categorization 
        of participants/observations.
    post_hpar: dataframe
        Posterior hyperparameters of each outcome for each latent profile.
    
    Notes
    -----
    Statistical model:
    y_i | z_i = t ~ Bernoulli(psi_t)
    psi_t ~ Beta(prior_a, prior_b)
    
    All calculations relating latent profiles to outcome variables (y) use hard assignment of participants/observations
    to latent profiles, i.e. each participant is assigned to their most probable profile, which is then treated as known.
    
    In a future version, the pairwise mean comparisons should be replaced with a partition-based post-hoc analysis as 
    described in our paper. Also, it would be nice to add a generalization test using new data (x_new and y_new) as
    in previous versions of the normal outcome analysis function.
    '''
    ##### SET UP DATA ETC #####
    y_names = pd.Categorical(y.columns.values, categories = y.columns.values, ordered = True)
    if index is None:
        y = y.copy()
    else:
        y = y.iloc[index].copy().transpose()
    n_y = y.shape[1] # number of dependent variables
    bayes_factor_df = pd.DataFrame(1.0,
                                   columns = ['bf10', 'frac_bf10'],
                                   index = y_names) # empty dataframe for results
    
    ##### COMPUTE BAYES FACTORS AND FRACTIONAL BAYES FACTORS #####
    for j in range(n_y):
        y_j = y[y_names[j]].values
        bayes_factor_df.loc[y_names[j], 'bf10'] = bayes_factors.bernoulli(y_j,
                                                                          model.z_hat_1hot,
                                                                          prior_a,
                                                                          prior_b)
        bayes_factor_df.loc[y_names[j], 'frac_bf10'] = bayes_factors.frac_bernoulli(y_j,
                                                                                    model.z_hat_1hot,
                                                                                    prior_a,
                                                                                    prior_b)
        bayes_factor_df.loc[y_names[j], 'post_bf10'] = bayes_factors.post_bernoulli(y_j,
                                                                                    model.z_hat_1hot,
                                                                                    prior_a,
                                                                                    prior_b)
    ##### POSTERIOR HYPERPARAMETERS #####
    post_hpar = dict()
    for j in range(n_y):
        (y_j, z_hat_j) = _remove_nan(y[y_names[j]].values, model.z_hat_1hot)
        dist = exp_families.multi_group_distribution(exp_families.beta_bernoulli, {'a': prior_a, 'b': prior_b}, model.n_profiles)
        dist.update(y_j, z_hat_j)
        post_hpar[y_names[j]] = dist.hpar_table()
        
    ##### PAIRWISE COMPARISONS (FRACTIONAL BAYES FACTORS) TO PROFILE 0 #####
    pairwise_log10_frac_bf10 = pd.DataFrame(0.0,
                                            columns = ['profile ' + str(t + start_profile_labels_from1) for t in range(1, model.n_profiles)],
                                            index = y_names)
    for j in range(n_y):
        for t in range(1, model.n_profiles):
            in_profiles = np.isin(model.z_hat, [0, t])
            y_used = y.loc[in_profiles, y_names[j]].values # only include data from people in these profiles
            z_hat_used = model.z_hat_1hot[:, in_profiles][[0, t], :]
            pairwise_log10_frac_bf10.loc[y_names[j], 'profile ' + str(t + start_profile_labels_from1)] = np.log10(bayes_factors.frac_bernoulli(y_used, z_hat_used, prior_a, prior_b))
    
    
    ##### COMPUTE THE BRIER SKILL SCORE (BSS) #####
    bss = pd.Series(0.0, index = y_names)
    for j in range(n_y):
        E_psi = post_hpar[y_names[j]]['a']/(post_hpar[y_names[j]]['a'] + post_hpar[y_names[j]]['b'])
        (y_j, z_hat_j) = _remove_nan(y[y_names[j]].values, model.z_hat_1hot)
        y_hat = np.inner(E_psi, z_hat_j.T)
        n_j = y_j.shape[0]
        Brier_skill = np.sum((y_j - y_hat)**2)/n_j
        reference_skill = np.sum((y_j - np.mean(y_j))**2)/n_j
        bss[y_names[j]] = 1 - Brier_skill/reference_skill
    
    ##### MAKE PLOT #####
    plot_df = pd.DataFrame(product(y_names, range(model.n_profiles)),
                           columns = ['variable', 'profile'])
    plot_df['E_psi'] = 0.0
    plot_df['lower'] = 0.0
    plot_df['upper'] = 0.0
    for j in range(n_y):
        rows_j = plot_df['variable'] == y_names[j]
        plot_df.loc[rows_j, 'E_psi'] = np.array(post_hpar[y_names[j]]['a']/(post_hpar[y_names[j]]['a'] + post_hpar[y_names[j]]['b']))
        plot_df.loc[rows_j, 'lower'] = beta_dist.ppf(0.05, post_hpar[y_names[j]]['a'], post_hpar[y_names[j]]['b'])
        plot_df.loc[rows_j, 'upper'] = beta_dist.ppf(0.95, post_hpar[y_names[j]]['a'], post_hpar[y_names[j]]['b'])
    if start_profile_labels_from1:
        plot_df['profile'] += 1
    plot_df['profile'] = plot_df['profile'].astype('string')
    if not profile_labels is None:
        plot_df['profile label'] = int(plot_df.shape[0]/len(profile_labels))*profile_labels

    if facet_var == 'profile':
        if profile_labels is None:
            plot = p9.ggplot(plot_df, p9.aes(x = 'variable', y = 'E_psi', ymin = 'lower', ymax = 'upper'))
        else:
            plot = p9.ggplot(plot_df, p9.aes(shape = 'profile label', x = 'variable', y = 'E_psi', ymin = 'lower', ymax = 'upper'))
    elif facet_var == 'variable' or n_y == 1:
        if profile_labels is None:
            plot = p9.ggplot(plot_df, p9.aes(x = 'profile', y = 'E_psi', ymin = 'lower', ymax = 'upper'))
        else:
            plot = p9.ggplot(plot_df, p9.aes(shape = 'profile label', x = 'profile', y = 'E_psi', ymin = 'lower', ymax = 'upper'))

        plot += p9.geom_point()
        plot += p9.geom_errorbar()
        plot += p9.theme_classic(base_size = font_size)
        plot += p9.theme(figure_size = figure_size)
        if not profile_labels is None:
            plot += p9.scale_shape_manual(values = len(profile_labels)*["o"]) # this is just a hack to display the legend (we don't want different shapes)

        if n_y > 1:
            if facet_var == 'profile':
                plot += p9.facet_wrap('profile', scales = 'free_x', ncol = ncol)
            elif facet_var == 'variable':
                plot += p9.facet_wrap('variable', scales = 'free', ncol = ncol)

    return {'plot': plot, 'plot_df': plot_df, 'bayes_factors': bayes_factor_df, 'log10_bayes_factors': np.log10(bayes_factor_df), 'pairwise_log10_frac_bf10': pairwise_log10_frac_bf10, 'Brier_skill_score': bss, 'post_hpar': post_hpar}