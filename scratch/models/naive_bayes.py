# AUTOGENERATED! DO NOT EDIT! File to edit: 02_naive_bayes.ipynb (unless otherwise specified).

__all__ = ['NaiveBayes']

# Cell
import pandas as pd
import numpy as np
from collections import defaultdict, Counter

# Cell
class NaiveBayes:
    """Naive Bayes Algorithm for Binary Classification"""

    def __init__(self):
        self.class1_term_cf = defaultdict(int) #term frequency in class 1
        self.class2_term_cf = defaultdict(int) #term frequency in class 2
        self.classes = []

    def fit(self, X, y):
        """ Train Naive Bayes.

        Args:

            X (nested list): nested list of tokenized samples.
            y (list): list of corresponding lables.
        """

        self._get_priors(y)
        self._get_term_class_freq(X, y)
        self._get_vocab_length()

    def _get_priors(self, y_train):
        """Calculate the priors for both classes"""

        self.priors = Counter(y_train)
        self.classes = list(self.priors.keys())
        total = sum(self.priors.values())
        for class_name in self.priors.keys():
            self.priors[class_name] /= total

    def _get_term_class_freq(self, x_train, y_train):
        """Calculate term frequency in each class"""

        for index , sample in enumerate(x_train):
            for term in sample:
                if   y_train[index] == self.classes[0]:
                    self.class1_term_cf[term] += 1
                elif y_train[index] == self.classes[1]:
                    self.class2_term_cf[term]  += 1

        self.class1_cf = sum(self.class1_term_cf.values())
        self.class2_cf = sum(self.class2_term_cf.values())

    def _get_vocab_length(self):
        self.vocab_length = len(set(list(self.class1_term_cf.keys()) + \
                                    list(self.class2_term_cf.keys())))

    def predict(self, X):
        """ Predict the labels for samples.

        Args:

            X(nested list): nested list of tokenized samples.

        Returns:

            list of predicted label.
        """

        predictions = []
        for sample in X:
            predictions.append(self._predict_label(sample))
        return predictions

    def _predict_label(self, sample):
        """predict label for one sample / instance"""

        summation_class1 = np.sum([np.log(self._prob_term_given_label(term , label = self.classes[0]))\
                                 for term in sample])
        summation_class2 = np.sum([np.log(self._prob_term_given_label(term , label = self.classes[1]))\
                                 for term in sample])
        prob_class1  = np.log(self.priors[self.classes[0]]) + summation_class1
        prob_class2  = np.log(self.priors[self.classes[1]]) + summation_class2

        prediction = self.classes[0] if prob_class1 > prob_class2 else self.classes[1]
        return prediction

    def _prob_term_given_label(self, term , label):
        """calculate probability of term given some label / class ,laplace smoothing applied"""

        if   label == self.classes[0]:
            return (self.class1_term_cf[term] + 1) / (self.class1_cf + self.vocab_length)
        elif label == self.classes[1]:
            return (self.class2_term_cf[term] + 1)  / (self.class2_cf + self.vocab_length)