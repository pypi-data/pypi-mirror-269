import numpy as np

def latent_profile(n_profiles = 4, m = 10, n = 500, separation = 2.0, mu = None, pi = None, sample_z = True, seed = None):
    '''
    Simulate data from a latent profile analysis (LPA) model.
    
    Parameters
    ----------
    n_profiles: int, optional
        Number of latent profiles. Ignored if either mu (latent profile means)
        or pi (latent profile base rates) is manually specified.
    m: int, optional
        Number of observed (indicator) variables. Ignored if either mu 
        (latent profile means) is manually specified.
    n: int, optional
        Number of participants (observations) to simulate.
    mu: array or None, optional
        Optionally specify profile means as a m x n_profiles array.
        If None (default) then profile means are sampled from a
        a normal distribution.
    separation: float, optional
        Variance for generating mu (latent profile means).
    pi: array or None, optional
        Base rates (prior probabilities) for latent profiles.
        If None (the default) then these are sampled from a flat
        Dirichlet distribution.
    sample_z: logical, optional
        If True (default) then values of z (profile membership) are sampled
        from the profile base rates (pi). If False, then profiles will be
        deterministically assigned so that their proportions will be as close
        as possible to the profile base rates, with any extra observations being
        assigned to the last profile.
    seed: int or None, optional
        If an integer, then this is the seed for random number generation.
        Using the same seed for repeated calls to the function will always
        produce the same simulated data. If None (the default) then repeated
        calls to the function will produce different simulated data.
        
    Output
    ------
    pi: Profile base rates (prior probabilties).
    mu: Profile means.
    z: Latent profile membership for each participant (observation).
    z_1hot: 1-hot encoding of z (= 1 for the correct profile, = 0 for all others).
    x: Observed (indicator) variables.
    n_profiles: Number of latent profiles.
    m: Number of observed (indicator) variables.
    n: Number of participants (observations).
    
    Notes
    -----
    The residual variance of simulated data (x) is set at 1.0.
    
    Because of this fact and the fact that profile means (mu) are
    drawn from a normal distribution with mean 0, the following relationship
    hold between Mahalanobis distance and the 'separation' parameter (variance
    for drawing profile means):
    
    separation = (average squared Mahalanobis distance)/(2*m)
    '''
    if seed is None:
        rng = np.random.default_rng()
    else:
        rng = np.random.default_rng(seed = seed)

    # overwrite n_profiles if pi is manually specified
    if not pi is None:
        n_profiles = pi.shape[0]
    # overwrite n_profiles and m if mu is manually specified
    if not mu is None:
        m = mu.shape[0]
        n_profiles = mu.shape[1]
    
    # sample profile base rates if not specified (sort highest to lowest)
    if pi is None:
        pi = np.sort(rng.dirichlet(alpha = np.ones(n_profiles)))[::-1]

    # sample profile centers if not specified
    if mu is None:
        mu = rng.normal(loc = 0.0, scale = np.sqrt(separation), size = [m, n_profiles])

    # assign observations to profiles
    if sample_z == True:
        z = np.zeros(n, dtype = int)
        for i in range(n):
            z[i] = rng.choice(np.arange(n_profiles), p = pi)
    else:
        number_in_each = np.floor(pi*n).astype(int)
        z = np.array(sum([number_in_each[t]*[t] for t in range(n_profiles)], (n - number_in_each.sum())*[n_profiles-1]))
    z_1hot = np.zeros([n_profiles, n])
    for i in range(n):
        z_1hot[z[i], i] = 1.0

    # sample observed data
    x = np.zeros([m, n])
    for i in range(n):
        x[:,i] = rng.normal(loc = mu[:, z[i]], scale = 1.0)

    return {'pi': pi, 'mu': mu, 'z': z, 'z_1hot': z_1hot, 'x': x, 'n_profiles': n_profiles, 'm': m, 'n': n}
        
def latent_factor(n_factors = 2, m = 10, n = 500, loading_var = 3.0, loadings = None, seed = None):
    '''
    Simulate data from a factor analysis model.
    
    Parameters
    ----------
    n_factors: int, optional
        Number of latent factors.
    m: int, optional
        Number of observed (indicator) variables.
    n: int, optional
        Number of participants (observations) to simulate.
    loading_var: float, optional
        Variance for generating factor loadings. This is not
        used if factor loadings are manually specified.
    loadings: float or None, optional
        Factor loadings. If None (the default), then
        these are randomly generated (see notes for details).
    seed: int or None, optional
        If an integer, then this is the seed for random number generation.
        Using the same seed for repeated calls to the function will always
        produce the same simulated data. If None (the default) then repeated
        calls to the function will produce different simulated data.
        
    Output
    ------
    loadings: Factor loadings.
    f: Individual factor scores.
    x: Observed (indicator) variables.
    n_factors: Number of latent factors.
    m: Number of observed (indicator) variables.
    n: Number of participants (observations).
    
    Notes
    -----
    The residual variance of simulated data (x) is set at 1.0.
    Factor scores (f) are drawn from independent standard normal distributions.
    
    If not specified by the user, loadings are randomly generated from the following process:
        1) Factor loadings are initialized to 0.0.
        2) Observed variables are divided up as evenly as possible among the latent factors,
        so that each observed variable depends on one latent factor.
        3) The factor loadings from step 2 are drawn from a normal distribution with mean 0 and variance loading_var.
    '''
    if seed is None:
        rng = np.random.default_rng()
    else:
        rng = np.random.default_rng(seed = seed)
    
    # sample loadings (if needed)
    if loadings is None:
        size = int(np.round(m/n_factors))
        loadings = np.zeros([m, n_factors])
        for k in range(n_factors):
            start = k*size
            if k < n_factors - 1:
                end = (k + 1)*size
            else:
                end = m
            loadings[range(start, end), k] = rng.normal(loc = 0.0, scale = np.sqrt(loading_var), size = end - start)
                
    # sample latent factor scores
    f = rng.normal(loc = 0.0, scale = 1.0, size = [n_factors, n])
    
    # sample observed data
    x = rng.normal(loc = loadings@f, scale = 1.0, size = [m, n])
    
    return {'loadings': loadings, 'f': f, 'x': x, 'n_factors': n_factors, 'm': m, 'n': n}

def latent_profile_factor(n_profiles = 3, n_factors = 4, m = 10, n = 500, separation = 2.0, pi = None, loading_var = 3.0, loadings = None, seed = 1234):
    '''
    Simulate data from a two-stage process:
    1) Factor scores are generated from latent profiles.
    2) Observed data are generated from factor scores.
    
    Thus, latent profiles specify points in factor space rather than
    observed variable space. This is implicitly the model used when 
    additive scores (as opposed to individual item responses) are fed into
    a latent profile analysis model.
    
    Parameters
    ----------
    n_profiles: int, optional
        Number of latent profiles.
    n_factors: int, optional
        Number of latent factors.
    m: int, optional
        Number of observed (indicator) variables.
    n: int, optional
        Number of participants (observations) to simulate.
    separation: float, optional
        Variance for generating mu (latent profile means).
    pi: float or None, optional
        Base rates (prior probabilities) for latent profiles.
        If None (the default) then these are sampled from a flat
        Dirichlet distribution.
    loading_var: float, optional
        Variance for generating factor loadings. This is not
        used if factor loadings are manually specified.
    loadings: float or None, optional
        Factor loadings. If None (the default), then
        these are randomly generated.
    seed: int or None, optional
        If an integer, then this is the seed for random number generation.
        Using the same seed for repeated calls to the function will always
        produce the same simulated data. If None (the default) then repeated
        calls to the function will produce different simulated data.
        
    Output
    ------
    pi: Profile base rates (prior probabilties).
    mu: Profile means.
    loadings: Factor loadings.
    z: Latent profile membership for each participant (observation).
    z_1hot: 1-hot encoding of z (= 1 for the correct profile, = 0 for all others).
    f: Individual factor scores.
    x: Observed (indicator) variables.
    n_profiles: Number of latent profiles.
    n_factors: Number of latent factors.
    m: Number of observed (indicator) variables.
    n: Number of participants (observations).
    '''
    if seed is None:
        rng = np.random.default_rng()
    else:
        rng = np.random.default_rng(seed = seed)

    # sample profile base rates if not specified (sort highest to lowest)
    if pi is None:
        pi = np.sort(rng.dirichlet(alpha = np.ones(n_profiles)))[::-1]

    # sample profile means (in latent factor space)
    mu = rng.normal(loc = 0.0, scale = np.sqrt(separation), size = [n_factors, n_profiles])

    # assign observations to profiles
    z = np.zeros(n, dtype = int)
    z_1hot = np.zeros([n_profiles, n])
    for i in range(n):
        z[i] = rng.choice(np.arange(n_profiles), p = pi)
        z_1hot[z[i], i] = 1.0

    # sample factor scores based on latent profiles
    f = np.zeros([n_factors, n])
    for i in range(n):
        f[:,i] = rng.normal(loc = mu[:, z[i]], scale = 1.0)

    # sample loadings (if needed)
    if loadings is None:
        size = int(np.round(m/n_factors))
        loadings = np.zeros([m, n_factors])
        for k in range(n_factors):
            start = k*size
            if k < n_factors - 1:
                end = (k + 1)*size
            else:
                end = m
            loadings[range(start, end), k] = rng.normal(loc = 0.0, scale = np.sqrt(loading_var), size = end - start)

    # sample observed data
    x = rng.normal(loc = loadings@f, scale = 1.0, size = [m, n])
    
    return {'pi': pi, 'mu': mu, 'loadings': loadings, 'z': z, 'z_1hot': z_1hot, 'f': f, 'x': x, 'n_profiles': n_profiles, 'n_factors': n_factors, 'm': m, 'n': n}