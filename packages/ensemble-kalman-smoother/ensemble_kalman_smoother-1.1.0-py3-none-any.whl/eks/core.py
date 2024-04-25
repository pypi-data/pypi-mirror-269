from collections import defaultdict
import numpy as np
from scipy.optimize import minimize


def ensemble(markers_list, keys, mode='median'):
    """Computes ensemble median (or mean) and variance of list of DLC marker dataframes
    Args:
        markers_list: list
            List of DLC marker dataframes`
        keys: list
            List of keys in each marker dataframe
        mode: string
            Averaging mode which includes 'median', 'mean', or 'confidence_weighted_mean'.

    Returns:
        ensemble_preds: np.ndarray
            shape (samples, n_keypoints)
        ensemble_vars: np.ndarray
            shape (samples, n_keypoints)
        ensemble_stacks: np.ndarray
            shape (n_models, samples, n_keypoints)
        keypoints_avg_dict: dict
            keys: marker keypoints, values: shape (samples)
        keypoints_var_dict: dict
            keys: marker keypoints, values: shape (samples)
        keypoints_stack_dict: dict(dict)
            keys: model_ids, keys: marker keypoints, values: shape (samples)
    """
    ensemble_stacks = []
    ensemble_vars = []
    ensemble_preds = []
    keypoints_avg_dict = {}
    keypoints_var_dict = {}
    keypoints_stack_dict = defaultdict(dict)
    if mode != 'confidence_weighted_mean':
        if mode == 'median':
            average_func = np.median
        elif mode == 'mean':
            average_func = np.mean
        else:
            raise ValueError(f"{mode} averaging not supported")
    for key in keys:
        if mode != 'confidence_weighted_mean':
            stack = np.zeros((len(markers_list), markers_list[0].shape[0]))
            for k in range(len(markers_list)):
                # print(markers_list[k][key].shape) Debugging list size from frame rate
                stack[k] = markers_list[k][key]
            stack = stack.T
            avg = average_func(stack, 1)
            var = np.var(stack, 1)
            ensemble_preds.append(avg)
            ensemble_vars.append(var)
            ensemble_stacks.append(stack)
            keypoints_avg_dict[key] = avg
            keypoints_var_dict[key] = var
            for i, keypoints in enumerate(stack.T):
                keypoints_stack_dict[i][key] = stack.T[i]
        else:
            likelihood_key = key[:-1] + 'likelihood'
            if likelihood_key not in markers_list[0]:
                raise ValueError(f"{likelihood_key} needs to be in your marker_df to use {mode}")
            stack = np.zeros((len(markers_list), markers_list[0].shape[0]))
            likelihood_stack = np.zeros((len(markers_list), markers_list[0].shape[0]))
            for k in range(len(markers_list)):
                stack[k] = markers_list[k][key]
                likelihood_stack[k] = markers_list[k][likelihood_key]
            stack = stack.T
            likelihood_stack = likelihood_stack.T
            conf_per_keypoint = np.sum(likelihood_stack, 1)
            mean_conf_per_keypoint = np.sum(likelihood_stack, 1) / likelihood_stack.shape[1]
            avg = np.sum(stack * likelihood_stack, 1) / conf_per_keypoint
            var = np.var(stack, 1)
            var = var / mean_conf_per_keypoint  # low-confidence --> inflated obs variances
            ensemble_preds.append(avg)
            ensemble_vars.append(var)
            ensemble_stacks.append(stack)
            keypoints_avg_dict[key] = avg
            keypoints_var_dict[key] = var
            for i, keypoints in enumerate(stack.T):
                keypoints_stack_dict[i][key] = stack.T[i]

    ensemble_preds = np.asarray(ensemble_preds).T
    ensemble_vars = np.asarray(ensemble_vars).T
    ensemble_stacks = np.asarray(ensemble_stacks).T
    return ensemble_preds, ensemble_vars, ensemble_stacks, \
        keypoints_avg_dict, keypoints_var_dict, keypoints_stack_dict


def forward_pass(y, m0, S0, C, R, A, Q, ensemble_vars):
    """Implements Kalman-filter
    Args:
        y: np.ndarray
            shape (samples, n_keypoints)
        m0: np.ndarray
            shape (n_latents)
        S0: np.ndarray
            shape (n_latents, n_latents)
        C: np.ndarray
            shape (n_keypoints, n_latents)
        R: np.ndarray
            shape (n_keypoints, n_keypoints)
        A: np.ndarray
            shape (n_latents, n_latents)
        Q: np.ndarray
            shape (n_latents, n_latents)
        ensemble_vars: np.ndarray
            shape (samples, n_keypoints)

    Returns:
        mf: np.ndarray
            shape (samples, n_keypoints)
        Vf: np.ndarray
            shape (samples, n_latents, n_latents)
        S: np.ndarray
            shape (samples, n_latents, n_latents)
    """
    # time-varying observation variance
    for i in range(ensemble_vars.shape[1]):
        R[i, i] = ensemble_vars[0][i]
    T = y.shape[0]
    mf = np.zeros(shape=(T, m0.shape[0]))
    Vf = np.zeros(shape=(T, m0.shape[0], m0.shape[0]))
    S = np.zeros(shape=(T, m0.shape[0], m0.shape[0]))
    K_array, _ = kalman_dot(y[0, :] - np.dot(C, m0), S0, C, R)
    mf[0] = m0 + K_array
    K_array, _ = kalman_dot(np.dot(C, m0), S0, C, R)
    mf[0] = m0 + K_array
    Vf[0, :] = S0 - K_array
    S[0] = S0
    innovation_cov = np.zeros((T, C.shape[0], C.shape[0]))
    innovations = np.zeros((T, y.shape[1]))  # Assuming y is m x T
    innovations[0] = y[0] - np.dot(C, mf[0])
    innovation_cov[0] = np.dot(C, np.dot(S0, C.T)) + R

    for t in range(1, T):
        for i in range(ensemble_vars.shape[1]):
            R[i, i] = ensemble_vars[t][i]
            S[t - 1] = np.dot(A, np.dot(Vf[t - 1, :], A.T)) + Q
            innovations[t] = y[t, :] - np.dot(C, np.dot(A, mf[t - 1, :]))
            K_array, _ = kalman_dot(innovations[t], S[t - 1], C, R)
            mf[t, :] = np.dot(A, mf[t - 1, :]) + K_array
            K_array, innovation_cov[t] = kalman_dot(np.dot(C, S[t - 1]), S[t - 1], C, R)
            Vf[t, :] = S[t - 1] - K_array
    return mf, Vf, S, innovations, innovation_cov


def kalman_dot(innovation, V, C, R):
    innovation_cov = R + np.dot(C, np.dot(V, C.T))
    innovation_cov_inv = np.linalg.solve(innovation_cov, innovation)
    K_array = np.dot(V, np.dot(C.T, innovation_cov_inv))
    return K_array, innovation_cov


def backward_pass(y, mf, Vf, S, A, Q, C):
    """Implements Kalman-smoothing backwards
    Args:
        y: np.ndarray
            shape (samples, n_keypoints)
        mf: np.ndarray
            shape (samples, n_keypoints)
        Vf: np.ndarray
            shape (samples, n_latents, n_latents)
        S: np.ndarray
            shape (samples, n_latents, n_latents)
        A: np.ndarray
            shape (n_latents, n_latents)
        Q: np.ndarray
            shape (n_latents, n_latents)
        C: np.ndarray
            shape (n_keypoints, n_latents)

    Returns:
        ms: np.ndarray
            shape (samples, n_keypoints)
        Vs: np.ndarray
            shape (samples, n_latents, n_latents)
        CV: np.ndarray
            shape (samples, n_latents, n_latents)
    """
    T = y.shape[0]
    ms = np.zeros(shape=(T, mf.shape[1]))
    Vs = np.zeros(shape=(T, mf.shape[1], mf.shape[1]))
    CV = np.zeros(shape=(T - 1, mf.shape[1], mf.shape[1]))

    # Last-time smoothed posterior is equal to last-time filtered posterior
    ms[-1, :] = mf[-1, :]
    Vs[-1, :, :] = Vf[-1, :, :]

    # Smoothing steps
    for i in range(T - 2, -1, -1):
        J = np.linalg.solve(S[i], np.dot(A, Vf[i])).T

        Vs[i] = Vf[i] + np.dot(J, np.dot(Vs[i + 1] - S[i], J.T))
        ms[i] = mf[i] + np.dot(J, ms[i + 1] - np.dot(A, mf[i]))
        CV[i] = np.dot(Vs[i + 1], J.T)

    return ms, Vs, CV


def eks_zscore(eks_predictions, ensemble_means, ensemble_vars, min_ensemble_std=2):
    """Computes zscore between eks prediction and the ensemble for a single keypoint.
    Args:
        eks_predictions: list
            EKS prediction for each coordinate (x and y) for as single keypoint - (samples, 2)
        ensemble_means: list
            Ensemble mean for each coordinate (x and y) for as single keypoint - (samples, 2)
        ensemble_vars: string
            Ensemble var for each coordinate (x and y) for as single keypoint - (samples, 2)
        min_ensemble_std:
            Minimum std threshold to reduce the effect of low ensemble std (default 2).
    Returns:
        z_score
            z_score for each time point - (samples, 1)
    """
    ensemble_std = np.sqrt(
        # trace of covariance matrix - multi-d variance measure
        ensemble_vars[:, 0] + ensemble_vars[:, 1])
    num = np.sqrt(
        (eks_predictions[:, 0]
         - ensemble_means[:, 0]) ** 2
        + (eks_predictions[:, 1] - ensemble_means[:, 1]) ** 2)
    thresh_ensemble_std = ensemble_std.copy()
    thresh_ensemble_std[thresh_ensemble_std < min_ensemble_std] = min_ensemble_std
    z_score = num / thresh_ensemble_std
    return z_score


'''
# Kept for reference -- Returns high-precision but low speed result

def optimize_smoothing_param(cov_matrix, y, m0, s0, C, A, R, ensemble_vars):
    guess = compute_initial_guess(y, ensemble_vars)
    result = minimize(
        return_nll_only,
        x0=guess,  # initial smooth param guess
        args=(cov_matrix, y, m0, s0, C, A, R, ensemble_vars),
        method='Nelder-Mead'
    )
    print(f'Optimal at s={result.x[0]}')
    return result.x[0]
'''


def optimize_smoothing_param(cov_matrix, y, m0, s0, C, A, R, ensemble_vars):
    guess = compute_initial_guess(y, ensemble_vars)

    # Define a callback function to update xatol during optimization
    def callback(xk):
        # Update xatol based on the current solution xk
        xatol = np.log(xk) * 0.01

        # Update the options dictionary with the new xatol value
        options['xatol'] = xatol

    # Initialize options with initial xatol
    options = {'xatol': np.log(guess)}

    result = minimize(
        return_nll_only,
        x0=guess,  # initial smooth param guess
        args=(cov_matrix, y, m0, s0, C, A, R, ensemble_vars),
        method='Nelder-Mead',
        options=options,
        callback=callback  # Pass the callback function
    )
    print(f'Optimal at s={result.x[0]}')
    return result.x[0]


# Function to compute ensemble mean, temporal differences, and standard deviation
def compute_initial_guess(y, ensemble_vars):
    # Compute ensemble mean
    ensemble_mean = np.mean(ensemble_vars, axis=0)

    # Initialize list to store temporal differences
    temporal_diffs_list = []

    # Iterate over each time step
    for i in range(1, len(ensemble_mean)):
        # Compute temporal difference for current time step
        temporal_diff = ensemble_mean - ensemble_vars[i]
        temporal_diffs_list.append(temporal_diff)

    # Compute standard deviation of temporal differences
    std_dev_guess = np.std(temporal_diffs_list)
    print(f'Initial guess: {std_dev_guess}')
    return std_dev_guess


# Combines filtering_pass, smoothing, and computing nll
def filter_smooth_nll(cov_matrix, smooth_param, y, m0, S0, C, A, R, ensemble_vars):
    # Adjust Q based on smooth_param and cov_matrix
    Q = smooth_param * cov_matrix
    # Run filtering and smoothing with the current smooth_param
    mf, Vf, S, innovs, innov_cov = forward_pass(y, m0, S0, C, R, A, Q, ensemble_vars)
    ms, Vs, CV = backward_pass(y, mf, Vf, S, A, Q, C)
    # Compute the negative log-likelihood based on innovations and their covariance
    nll, nll_values = compute_nll(innovs, innov_cov)
    return ms, Vs, nll, nll_values


# filter_smooth_nll version for iterative calls from optimize_smoothing_param
def return_nll_only(cov_matrix, smooth_param, y, m0, S0, C, A, R, ensemble_vars):
    # Adjust Q based on smooth_param and cov_matrix
    Q = smooth_param * cov_matrix
    smooth_param = smooth_param[0]
    # Run filtering and smoothing with the current smooth_param
    mf, Vf, S, innovs, innov_cov = forward_pass(y, m0, S0, C, R, A, Q, ensemble_vars)
    ms, Vs, CV = backward_pass(y, mf, Vf, S, A, Q, C)
    # Compute the negative log-likelihood based on innovations and their covariance
    nll, nll_values = compute_nll(innovs, innov_cov)
    return nll


def compute_nll(innovations, innovation_covs, epsilon=1e-6):
    T = innovations.shape[0]
    n_keypoints = innovations.shape[1]
    nll = 0
    nll_values = []
    k = np.log(2 * np.pi) * n_keypoints  # The Gaussian normalization constant part
    for t in range(T):
        # Regularize the innovation covariance matrix by adding epsilon to the diagonal
        reg_innovation_cov = innovation_covs[t] + epsilon * np.eye(n_keypoints)

        # Compute the log determinant of the regularized covariance matrix
        log_det_S = np.log(np.linalg.det(reg_innovation_cov) + epsilon)
        solved_term = np.linalg.solve(reg_innovation_cov, innovations[t])
        quadratic_term = np.dot(innovations[t], solved_term)

        # Compute the NLL increment for time step t
        nll_increment = 0.5 * (log_det_S + quadratic_term + k)
        nll_values.append(nll_increment)
        nll += nll_increment
    return nll, nll_values


# Alternative implementation of NLL

def compute_nll_2(y, mf, S, C, epsilon=1e-6, lower_bound=0, upper_bound=0):
    T, n_keypoints = y.shape
    nll = 0
    nll_values = []
    k = np.log(2 * np.pi) * n_keypoints

    for t in range(T):
        # Compute the innovation for time t
        innovation = y[t, :] - np.dot(C, mf[t, :])

        # Compute the log determinant and the quadratic term
        A = np.dot(C, S[t])

        # Add epsilon to the diagonal elements of A and S[t]
        A += np.eye(A.shape[0]) + epsilon
        S[t] += np.eye(S[t].shape[0]) + epsilon

        log_det_S = np.log(np.linalg.det(A))
        quadratic_term = np.dot(innovation.T, np.linalg.solve(S[t], innovation))
        nll_increment = 0.5 * (log_det_S + quadratic_term + k)
        nll_values.append(nll_increment)
        nll += nll_increment
    return nll, nll_values
