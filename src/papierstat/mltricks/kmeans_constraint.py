# -*- coding: utf-8 -*-
"""
@file
@brief Implémente la classe @see cl ConstraintKMeans.
"""
from sklearn.cluster import KMeans
from .kmeans_constraint_ import constraint_kmeans


class ConstraintKMeans(KMeans):
    """
    Defines a constraint :epkg:`k-means`.
    Clusters are modified to have an equal size.
    The algorithm is initialized with a regular :epkg:`k-means`
    and continues with a modified version of it.
    """

    def __init__(self, n_clusters=8, init='k-means++', n_init=10, max_iter=300,
                 tol=0.0001, precompute_distances='auto', verbose=0,
                 random_state=None, copy_x=True, n_jobs=1, algorithm='auto'):
        """
        @param      n_clusters              number of clusters
        @param      n_init                  used by :epkg:`k-means`
        @param      max_iter                used by :epkg:`k-means`
        @param      tol                     used by :epkg:`k-means`
        @param      precompute_distances    used by :epkg:`k-means`
        @param      verbose                 used by :epkg:`k-means`
        @param      random_state            used by :epkg:`k-means`
        @param      copy_x                  used by :epkg:`k-means`
        @param      n_jobs                  used by :epkg:`k-means`
        @param      algorithm               used by :epkg:`k-means`
        """
        KMeans.__init__(self, n_clusters=n_clusters, init=init, n_init=n_init,
                        max_iter=max_iter, tol=tol, precompute_distances=precompute_distances,
                        verbose=verbose, random_state=random_state, copy_x=copy_x,
                        n_jobs=n_jobs, algorithm=algorithm)

    def fit(self, X, y=None, fLOG=None):
        """
        Compute k-means clustering.

        Parameters
        ----------
        X : array-like or sparse matrix, shape=(n_samples, n_features)
            Training instances to cluster. It must be noted that the data
            will be converted to C ordering, which will cause a memory
            copy if the given data is not C-contiguous.

        y : Ignored

        fLOG: logging function
        """
        max_iter = self.max_iter
        self.max_iter //= 2
        KMeans.fit(self, X, y)
        self.max_iter = max_iter
        return self.constraint_kmeans(X, fLOG=fLOG)

    def constraint_kmeans(self, X, fLOG=None):
        """
        Completes the constraint k-means.

        @param      X   features
        """
        labels, centers, inertia, iter = constraint_kmeans(X, self.labels_, self.cluster_centers_,
                                                           self.inertia_, self.precompute_distances, self.n_iter_, self.max_iter,
                                                           verbose=self.verbose, fLOG=fLOG)
        self.labels_ = labels
        self.cluster_centers_ = centers
        self.inertia_ = inertia
        self.n_iter_ = iter
        return self
