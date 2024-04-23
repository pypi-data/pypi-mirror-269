import numpy as np

def make_sim_data(n = 500, m = 10, alpha = 4.0, omega = 2, continuous_z = False, include_intercept = True, sample_xi = True, missing_data_prob = None):
    '''
    Generate simulated data from the Indian Buffet Process using the
    stick-breaking construction.
    
    Parameters
    ----------
    n: int, optional
        Number of observations to simulate.
    m: int, optional
        Number of observed variables.
    alpha: float, optional
        Parameter of the Indian buffet process.
    omega: float, optional
        Prior precision of A (and intercept if it is sampled).
    continuous_z: logical, optional
        If True then z is a product of normal and Bernoulli distributions.
        If False then only Bernoulli distributions are used to sample z.
    include_intercept: logical, optional
        If True then an intercept term is sampled from N(0, 1/sqrt(omega)).
        If False then no intercept term is included.
    sample_xi: logical, optional
        If True then xi (the observed variable precision) is sampled from uniform(0.8, 1.2).
        If False then xi is set to 1.
    missing_data_prob: float or None, optional
        If None (the default) then no data are missing.  If specified then this is the
        independent probability of each observed variable being missing in each observation
        (up to a maximum of 2 missing variables per observation). 
    '''
    # --sample latent features (IBP stick-breaking construction)--
    rng = np.random.default_rng()
    v = np.array([rng.beta(alpha, 1)])
    pi = np.array([v])
    # keep sampling feature probabilities (pi) until they become 
    # negligibly small and we have at least 8 of them
    while (pi[-1] > 0.01) or (len(pi) < 8):
        v = np.append(v, rng.beta(alpha, 1))
        pi = np.append(pi, v[-1] * pi[-1])
    p = len(pi) # true number of non-negligible latent features
    z = np.zeros([p, n])
    if continuous_z:
        for i in range(n):
            z[:, i] = rng.binomial(1, pi)
    else:
        for i in range(n):
            z[:, i] = rng.binomial(1, pi)*rng.normal(0, 1, size = p)

    # --sample loading matrix--
    A = rng.normal(0, 1/np.sqrt(omega), [m, p])

    # --sample intercept terms--
    if include_intercept:
        intercept = rng.normal(0, 1/np.sqrt(omega), m)
    else:
        intercept = np.zeros(m)
        
    # --sample observed variable precision--
    if sample_xi:
        xi = rng.uniform(0.8, 1.2, m) # noise standard deviation
    else:
        xi = np.ones(m)

    # --sample observations--
    x = np.zeros([m, n])
    for j in range(m):
        x[j, :] = rng.normal(A[j, :]@z + intercept[j], 1/np.sqrt(xi[j]))
        
    # --determine which data are missing, if any--
    if not missing_data_prob is None:
        for i in range(n):
            missing_count = 0
            for j in range(m):
                if rng.binomial(1, missing_data_prob) == 1:
                    x[j,i] = np.nan
                    missing_count += 1
                if missing_count >= 2:
                    break
    
    return {'x': x, 'A': A, 'intercept': intercept, 'xi': xi, 'z': z, 'v': v, 'pi': pi}