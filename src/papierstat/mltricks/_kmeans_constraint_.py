"""
@file
@brief This file uses the code in scikit-learn *0.22*.
"""
# Source: https://github.com/scikit-learn/scikit-learn/blob/95d4f0841d57e8b5f6b2a570312e9d832e69debc/sklearn/cluster/_k_means_fast.pyx
import numpy as np
from sklearn.utils.sparsefuncs_fast import assign_rows_csr  # pylint: disable=W0611,E0611


def _centers_dense(X, sample_weight, labels, n_clusters, distances):
    """
    M step of the K-means EM algorithm
    Computation of cluster centers / means.
    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
    sample_weight : array-like, shape (n_samples,)
        The weights for each observation in X.
    labels : array of integers, shape (n_samples)
        Current label assignment
    n_clusters : int
        Number of desired clusters
    distances : array-like, shape (n_samples)
        Distance to closest cluster for each sample.
    Returns
    -------
    centers : array, shape (n_clusters, n_features)
        The resulting centers
    """
    n_samples = X.shape[0]
    n_features = X.shape[1]

    dtype = X.dtype
    centers = np.zeros((n_clusters, n_features), dtype=dtype)
    weight_in_cluster = np.zeros((n_clusters,), dtype=dtype)

    for i in range(n_samples):
        c = labels[i]
        weight_in_cluster[c] += sample_weight[i]
    empty_clusters = np.where(weight_in_cluster == 0)[0]
    # maybe also relocate small clusters?

    if len(empty_clusters):
        # find points to reassign empty clusters to
        far_from_centers = distances.argsort()[::-1]

        for i, cluster_id in enumerate(empty_clusters):
            far_index = far_from_centers[i]
            new_center = X[far_index] * sample_weight[far_index]
            centers[cluster_id] = new_center
            weight_in_cluster[cluster_id] = sample_weight[far_index]

    for i in range(n_samples):
        for j in range(n_features):
            centers[labels[i], j] += X[i, j] * sample_weight[i]

    centers /= weight_in_cluster[:, np.newaxis]

    return centers


def _centers_sparse(X, sample_weight, labels, n_clusters, distances):
    """
    M step of the K-means EM algorithm
    Computation of cluster centers / means.
    Parameters
    ----------
    X : scipy.sparse.csr_matrix, shape (n_samples, n_features)
    sample_weight : array-like, shape (n_samples,)
        The weights for each observation in X.
    labels : array of integers, shape (n_samples)
        Current label assignment
    n_clusters : int
        Number of desired clusters
    distances : array-like, shape (n_samples)
        Distance to closest cluster for each sample.
    Returns
    -------
    centers : array, shape (n_clusters, n_features)
        The resulting centers
    """
    n_samples = X.shape[0]
    n_features = X.shape[1]

    data = X.data
    indices = X.indices
    indptr = X.indptr

    dtype = X.dtype
    centers = np.zeros((n_clusters, n_features), dtype=dtype)
    weight_in_cluster = np.zeros((n_clusters,), dtype=dtype)
    for i in range(n_samples):
        c = labels[i]
        weight_in_cluster[c] += sample_weight[i]
    empty_clusters = np.where(weight_in_cluster == 0)[0]
    n_empty_clusters = empty_clusters.shape[0]

    # maybe also relocate small clusters?

    if n_empty_clusters > 0:
        # find points to reassign empty clusters to
        far_from_centers = distances.argsort()[::-1][:n_empty_clusters]
        assign_rows_csr(X, far_from_centers, empty_clusters, centers)

        for i in range(n_empty_clusters):
            weight_in_cluster[empty_clusters[i]] = 1

    for i in range(labels.shape[0]):
        curr_label = labels[i]
        for ind in range(indptr[i], indptr[i + 1]):
            j = indices[ind]
            centers[curr_label, j] += data[ind] * sample_weight[i]

    centers /= weight_in_cluster[:, np.newaxis]

    return centers
