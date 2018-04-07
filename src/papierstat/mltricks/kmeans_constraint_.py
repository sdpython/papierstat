# -*- coding: utf-8 -*-
"""
@file
@brief Implémente la classe @see cl ConstraintKMeans.
"""
from pandas import DataFrame
import numpy
import scipy.sparse
from sklearn.cluster.k_means_ import _labels_inertia
from sklearn.cluster._k_means import _centers_sparse, _centers_dense
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.utils.extmath import row_norms


def linearize_matrix(mat, *adds):
    """
    Linearizes a matrix into a new one
    with 3 columns value, row, column.
    The output format is similar to
    :epkg:`csr_matrix` but null values are kept.

    @param      mat     matrix
    @param      adds    additional square matrices
    @return             new matrix

    *adds* defines additional matrices, it adds
    columns on the right side and fill them with
    the corresponding value taken into the additional
    matrices.
    """
    if scipy.sparse.issparse(mat):
        if isinstance(mat, scipy.sparse.csr_matrix):
            max_row = mat.shape[0]
            res = numpy.empty((len(mat.data), 3 + len(adds)), dtype=mat.dtype)
            row = 0
            for i, v in enumerate(mat.data):
                while row < max_row and i >= mat.indptr[row]:
                    row += 1
                res[i, 0] = v
                a, b = row - 1, mat.indices[i]
                res[i, 1] = a
                res[i, 2] = b
                for k, am in enumerate(adds):
                    res[i, k + 3] = am[a, b]
            return res
        else:
            raise NotImplementedError(
                "This kind of sparse matrix is not handled: {0}".format(type(mat)))
    else:
        n = mat.shape[0]
        c = mat.shape[1]
        ic = numpy.arange(mat.shape[1])
        res = numpy.empty((n * c, 3 + len(adds)), dtype=mat.dtype)
        for i in range(0, n):
            a = i * c
            b = (i + 1) * c
            res[a:b, 1] = i
            res[a:b, 2] = ic
        res[:, 0] = mat.ravel()
        for k, am in enumerate(adds):
            res[:, 3 + k] = am.ravel()
        return res


def constraint_kmeans(X, labels, centers, inertia, precompute_distances, iter, max_iter,
                      sortby='distance', verbose=0, fLOG=None):
    """
    Completes the constraint *k-means*.

    @param      X                       features
    @param      labels                  initialized labels (unsued)
    @param      centers                 initialized centers
    @param      inertia                 initialized inertia (unsued)
    @param      precompute_distances    precompute distances (used in
                                        `_label_inertia <https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/cluster/k_means_.py#L547>`_)
    @param      iter                    number of iteration already done
    @param      max_iter                maximum of number of iteration
    @param      sortby                  strategy used to sort observations before
                                        mapping them to clusters
    @param      verbose                 verbose
    @param      fLOG                    logging function (needs to be specified otherwise
                                        verbose has no effects)
    @return                             tuple (best_labels, best_centers, best_inertia, iter)
    """
    if isinstance(X, DataFrame):
        X = X.as_matrix()
    x_squared_norms = row_norms(X, squared=True)
    counters = numpy.empty((centers.shape[0],), dtype=numpy.int32)
    limit = X.shape[0] // centers.shape[0]
    leftover = X.shape[0] - limit * centers.shape[0]
    leftclose = numpy.empty((X.shape[0],), dtype=numpy.int32)
    n_clusters = centers.shape[0]
    distances_close = numpy.empty((X.shape[0],), dtype=X.dtype)
    best_inertia = None
    prev_labels = None

    while iter < max_iter:

        # association
        _constraint_association(leftover, counters, labels, leftclose, distances_close,
                                centers, X, x_squared_norms, limit, sortby)

        # compute new clusters
        if scipy.sparse.issparse(X):
            centers = _centers_sparse(X, labels, n_clusters, distances_close)
        else:
            centers = _centers_dense(X, labels, n_clusters, distances_close)

        # inertia
        _, inertia = _labels_inertia(X, x_squared_norms, centers,
                                     precompute_distances=precompute_distances,
                                     distances=distances_close)

        iter += 1
        if verbose and fLOG:
            fLOG("CKMeans %d/%d inertia=%f" % (iter, max_iter, inertia))

        # best option so far?
        if best_inertia is None or inertia < best_inertia:
            best_inertia = inertia
            best_centers = centers.copy()
            best_labels = labels.copy()

        # early stop
        if prev_labels is not None and numpy.array_equal(prev_labels, labels):
            break
        prev_labels = labels.copy()

    return best_labels, best_centers, best_inertia, iter


def _constraint_association(leftover, counters, labels, leftclose, distances_close,
                            centers, X, x_squared_norms, limit, sortby):
    """
    Completes the constraint *k-means*.

    @param      X               features
    @param      labels          initialized labels (unsued)
    @param      centers         initialized centers
    @param      x_squared_norms norm of *X*
    @param      limit           number of point to associate per cluster
    @param      leftover        number of points to associate at the end
    @param      counters        allocated array
    @param      leftclose       allocated array
    @param      labels          allocated array
    @param      distances_close allocated array
    @param      sortby          strategy used to sort point before
                                mapping them to a cluster
    """
    # initialisation
    counters[:] = 0
    labels[:] = -1
    leftclose[:] = -1
    distances_close[:] = numpy.nan

    # distances
    distances = euclidean_distances(
        centers, X, Y_norm_squared=x_squared_norms, squared=True)
    distances = distances.T
    sortby_coef = _compute_sortby_coefficient(distances, sortby)
    distance_linear = linearize_matrix(distances, sortby_coef)
    sorted_distances = distance_linear[distance_linear[:, 3].argsort()]

    nover = leftover
    for i in range(0, sorted_distances.shape[0]):
        ind = int(sorted_distances[i, 1])
        if labels[ind] >= 0:
            continue
        c = int(sorted_distances[i, 2])
        if counters[c] < limit:
            # The cluster still accepts new points.
            counters[c] += 1
            labels[ind] = c
            distances_close[ind] = sorted_distances[i, 0]
        elif nover > 0 and leftclose[ind] == -1:
            # The cluster may accept one point if the number
            # of clusters does not divide the number of points in X.
            counters[c] += 1
            labels[ind] = c
            nover -= 1
            leftclose[ind] = 0
            distances_close[ind] = sorted_distances[i, 0]
    return distances


def constraint_predictions(X, centers, sortby):
    """
    Computes the predictions but tries
    to associates the same numbers of points
    in each cluster.

    @param      X           features
    @param      centers     centers of each clusters
    @param      sortby      strategy used to sort point before
                            mapping them to a cluster
    @return                 labels, distances, distances_close
    """
    if isinstance(X, DataFrame):
        X = X.as_matrix()
    x_squared_norms = row_norms(X, squared=True)
    counters = numpy.empty((centers.shape[0],), dtype=numpy.int32)
    limit = X.shape[0] // centers.shape[0]
    leftover = X.shape[0] - limit * centers.shape[0]
    leftclose = numpy.empty((X.shape[0],), dtype=numpy.int32)
    distances_close = numpy.empty((X.shape[0],), dtype=X.dtype)
    labels = numpy.empty((X.shape[0],), dtype=int)

    distances = _constraint_association(leftover, counters, labels, leftclose,
                                        distances_close, centers, X, x_squared_norms,
                                        limit, sortby)

    return labels, distances, distances_close


def _compute_sortby_coefficient(distances, sortby):
    """
    Creates a matrix
    """
    if sortby == 'distance':
        return distances
    elif sortby == '-distance':
        return distances
    elif sortby == 'ratio':
        inv = numpy.reciprocal(distances)
        mini = numpy.amin(distances, axis=1)
        return mini[:, numpy.newaxis] * inv
    elif sortby == '-ratio':
        mini = numpy.reciprocal(numpy.amin(distances, axis=1))
        return mini[:, numpy.newaxis] * distances
    else:
        raise ValueError("Strategy '{0}' does not exist.".format(sortby))
