# AUTOGENERATED! DO NOT EDIT! File to edit: 01_count_vectorizer.ipynb (unless otherwise specified).

__all__ = ['CountVectorizer']

# Cell
from collections import Counter, defaultdict
from scipy.sparse import coo_matrix
import numpy as np

# Cell
class CountVectorizer:
    """Implementation of Bag of Word Model. Assign zero to terms that don't occur in vocabulary"""

    def __init__(self, store_class_vocab = False):
        """
        Args:
            store_class_vocab (bool): store vocabulary for individual classes ?
        """

        if store_class_vocab:
            self.store_class_vocab = {}

    def _calculate_stats(self, y_train):
        """Calculates basic stats: labels , labels frequency, and distrubution of labels/class"""
        self.labels, self.labels_freq = np.unique(y_train, return_counts= True)
        total_freq = np.sum(self.labels_freq)
        self.distribution = self.labels_freq / total_freq

    def _get_vocab(self,  x_train, y_train):
        """Build vocabulary  and store corresponding frequency of word types"""

        vocab = Counter()
        for label in self.labels:
            vocab += self._word_to_count_map(x_train, y_train , label)

        self.vocab, self.vocab_freq = zip(*vocab.items())

    def _word_to_count_map(self, x_train, y_train , label):
        """A dictionary that maps from word types in a class to its frequency"""

        word_to_count = defaultdict(int)
        for index , sample in enumerate(x_train):
            if y_train[index] == label:
                for term in sample:
                    word_to_count[term] += 1

        try: # can be used to store vocab of individual classes
            self.store_class_vocab[label] = word_to_count
        finally:
            return Counter(word_to_count)

    def fit(self, x_train, y_train):
        """Calcultes neccesary stats to build Bag of Words model"

        Args:
            x_train (nested list): list of list containing samples.
            y_train (list): labels for training samples.
        """

        self._calculate_stats(y_train)
        self._get_vocab(x_train, y_train)

    def transform(self, X):
        """Make Bag of Words vector.

        Args:
            X (nested list): list of list containing tokenized samples.

        Returns:
            sparse coordinate matrix of shape(len(X), len(vocab))
        """
        rows = []
        columns = []
        data = []

        for sample_index, sample in enumerate(X):
            sample = Counter(sample)
            for term, term_freq in sample.items():
                if term in self.vocab:
                    vocab_index = self.vocab.index(term)
                else:  #assign zero to some new term in test set which is not present in train.
                    continue
                columns.append(vocab_index)
                rows.append(sample_index)
                data.append(term_freq)

        return coo_matrix((data,(rows, columns)), shape=(len(X), len(self.vocab)))
