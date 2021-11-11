import spacy
from spacy.tokens import Span, Doc
# Can attach a special getter to a general span that will calculate the correlation to a group of keywords
# Later on can make span groups based on the value of the correlation values.
from correlation import SpanCorrelator


class NGramCorrelateSpacy:

    def __init__(self, keywords, threshold, tag) -> None:
        self.correlator = SpanCorrelator(keywords, threshold, tag)

    def correlate_spans(self, doc: Doc, n_gram_size):
        n_gram_tuples = self.get_n_gram_tuples(n_gram_size, len(doc))
        span_candidates = [doc[t[0]:t[1]] for t in n_gram_tuples]
        self.correlator(doc, span_candidates[::4])

    def get_n_gram_tuples(self, size, doc_len):
        return [(i, i + size) for i in range(doc_len - size + 1)]