import spacy
from spacy.tokens import Span, Doc
# Can attach a special getter to a general span that will calculate the correlation to a group of keywords
# Later on can make span groups based on the value of the correlation values.
from correlation import KeywordCorrelator


class NGramCorrelateSpacy:

    def __init__(self, model_url, keywords, n_gram_length, threshold) -> None:
        self.correlator = KeywordCorrelator(model_url, keywords)
        self.n_gram_length = n_gram_length
        self.threshold = threshold

    def correlate_spans(self, doc: Doc, n_gram_size):
        span_correlate = lambda span: self.correlator(span.text)
        n_gram_tuples = self.get_n_gram_tuples(n_gram_size, len(doc))
        span_candidates = [doc[t[0]:t[1]] for t in n_gram_tuples]
        relevance_coefficients = self.correlator(span_candidates)

        span_candidates = [
            s for s, c in zip(span_candidates, relevance_coefficients)
            if c > self.threshold
        ]

    def get_n_gram_tuples(self, size, doc_len):
        return [(i, i + size) for i in range(doc_len - size + 1)]