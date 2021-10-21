from typing import List, Tuple
import numpy as np
from spacy.tokens import Doc, Token


class KeywordCorrelateSpacy:
    """A class to assist in finding related terms to a set of keywords

    Args:
        tf_model: a tensorflow model that embeds sentences
        keywords: a list of keywords to relate to
    """

    def __init__(self, tf_model, keywords):
        self.keywords = keywords
        self.embed = tf_model
        self.keyword_embeddings = self.embed(self.keywords)
        Token.set_extension("kwd_correlate", default=None)

    def correlate_tokens(self, tokens) -> List[Tuple[float, str]]:
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

        return correlation_1d, list_to_correlate

    def sorted_correlate(self, tokens):
        correlation, list_out = self.correlate_tokens(tokens)
        zipped_correlations = zip(correlation, list_out)
        return sorted(zipped_correlations, key=lambda x: x[0], reverse=True)

    def __call__(self, doc: Doc):
        tokens = [str(t) for t in doc]
        correlated, _ = self.correlate_tokens(tokens)

        for i, t in enumerate(doc):
            t._.kwd_correlate = correlated[i]

        return doc
