# AUTOGENERATED! DO NOT EDIT! File to edit: 03_KNN.ipynb (unless otherwise specified).

__all__ = ['KNearestNeighbors', 'euclidean_distance', 'distance_weights']

# Cell
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
from collections import defaultdict, Counter

from sklearn.model_selection import train_test_split
from sklearn import datasets

# Cell
class KNearestNeighbors:
    """K Nearest Neighbour Algorithm , Standard and Weighted KNN"""

    def __init__(self, k, distance_metric = 'standard'):
        """
        Args:

            k(int): Take K nearest neighbours into account

            distance_metric(str): "weighted KNN" | "standard"
        """
        self.k = k
        self.distance_metric = distance_metric

    def fit(self, X, y):
        """Train KNN"""
        self.X = X
        self.y = y
        self.labels = list(Counter(y).keys())

    def predict(self, X):
        """ Prediction for samples.

        Args:

            X: Numpy array of shape(m, n)

        Returns:

            array of shape (m,)
        """
        predictions = np.array([])

        for test_sample in X:
            distance = np.array([])

            for train_sample in self.X:
                distance = np.append(distance , euclidean_distance(train_sample, test_sample))

            # get indexes for k closest points
            k_min_distance_indexes = distance.argsort()[:self.k]
            # get gold predictions using indexes.
            prediction_pool = self.y[k_min_distance_indexes]
            # get unique predictions and their counts.
            k_min_values , k_min_counts = np.unique(prediction_pool, return_counts=True)

            #weighted KNN
            if self.distance_metric == "weighted KNN":
                pool = zip(prediction_pool, np.sort(distance)[:self.k])
                pred = distance_weights(pool, self.labels)
                predictions = np.append(predictions, pred)

            else:
                max_count_index = np.argmax(k_min_counts)
                predictions = np.append(predictions, k_min_values[max_count_index])

        return predictions

def euclidean_distance(x1, x2):
    """Euclidean distance between numpy arrays"""

    return np.sqrt(np.sum((x1 - x2)*(x1 - x2)))

def distance_weights(pool, labels):
    """Calculate weights based on distance"""

    weights = [0 for _ in range(len(labels))]

    for i in pool:
        for label in labels:
            pool_label = i[0]
            distance   = i[1]
            if pool_label == label:
                weights[label] += 1 / distance

    return weights.index(max(weights))