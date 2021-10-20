from typing import List, Tuple
import numpy as np


class KeywordCorrelate:
    """A class to assist in finding related terms to a set of keywords

    Args:
        tf_model: a tensorflow model that embeds sentences
        keywords: a list of keywords to relate to
    """

    def __init__(self, tf_model, keywords):
        self.keywords = keywords
        self.embed = tf_model
        self.keyword_embeddings = self.embed(self.keywords)

    def __call__(self, tokens, to_sort=False) -> List[Tuple[float, str]]:
        """Initiates the correlation process on a new document

        Args:
            tokens: a set of tokens to determine correlation 
            to_sort (bool): a flag to determine if the output is sorted
        
        Returns: a list of tuples containing the correlation value [0:1),
            which may be optionally sorted, highest correlated terms first
        
        """
        list_to_correlate = list(tokens)
        input_embeddings = self.embed(list_to_correlate)
        correlation_2d = np.inner(self.keyword_embeddings, input_embeddings)
        correlation_1d = np.max(correlation_2d, axis=0)
        zipped_correlations = zip(correlation_1d, list_to_correlate)

        if to_sort:
            return sorted(zipped_correlations, key=lambda x: x[0], reverse=True)
        else:
            return zipped_correlations
