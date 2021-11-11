import spacy
import tensorflow_hub as hub
from typing import List, Tuple
import numpy as np
from spacy.tokens import Doc, Token, Span
from spacy.language import Language

# Could put this URL in a configuration file, or load from environment variables
MODEL_URL = "https://tfhub.dev/google/universal-sentence-encoder/4"

EMBEDDER = hub.load(MODEL_URL)


class TokenArrayCorrelator:
    """Aides in labeling entities in a document that reach a certain similarity
    threshold when embedded against a group of keywords

    Example: 
        correlator = TokenArrayCorrelator(kwds, 0.5, "CLIMATE")

    Args:
        keywords (str): A list of keywords in a subject area
        threshold (float): Embedding-similarity threshold to tag entity
        entity_tag (str): A name given to a section that will appear in Displacy
    """

    def __init__(self, keywords: List[str], threshold: float,
                 entity_tag: str) -> None:
        self.threshold = threshold
        self.entity_tag = entity_tag
        self.correlator = KeywordCorrelator(keywords)

    def __call__(self, doc: Doc, tokens: List[Token]):
        """Correlates and tags a section of a document with the loaded keywords

        This function will embed the entire set of tokens (no need to be consecutive) 
        as one string and find the similarity the list of embedded keywords. If 
        the similarity is higher than a certain threshold, the subset starting from the
        index of the first token to the index of the last token will be added to the 
        document entities if it does not overlap with an existing entity. This 
        entitly will be labeled with the self.entity_tag variable

        This is especially useful if performing preprocessing on a document
        where some tokens out of a given subset may be thrown out as
        members of a list of stopwords, unwanted characters, or other reasons

        Example: 
            phrase_in_question = [doc[49], doc[53], doc[59]]
            correlator(doc, phrase_in_question)
            displacy.render(doc, style='ent')
        
        Args:
            doc (Doc): The current working spacy document
            tokens (List[Token]): A subset of tokens from the doc
        """
        start = tokens[0].i
        end = tokens[-1].i
        text = [" ".join([str(t) for t in tokens])]

        if self.correlator(text)[0] > self.threshold:
            try:
                doc.ents = list(
                    doc.ents) + [Span(doc, start, end, self.entity_tag)]
            except:
                pass


class SpanCorrelator:
    """A correlator that will mark relevant spans with a tag

    This class aides in labeling spans if they are similar
    enough to a list of keywords which are embedded on instatiation
    of this class.

    Example: 
        correlator = SpanCorrelator(kwds, 0.5, "CLIMATE")

    Args:
        keywords (List[str]): list of subject keywords
        threshold (float): correlation threshold for a span to be labeled
        entity_tag (str): label for the span, will appear in displacy plot  
    """

    def __init__(self, keywords: List[str], threshold: float, entity_tag: str):
        self.threshold = threshold
        self.entity_tag = entity_tag
        self.correlator = KeywordCorrelator(keywords)

    def __call__(self, doc: Doc, spans: List[Span]):
        """Tags a span if over correlation thresh to initialized set of keywords

        This method will embed a span against a set of initialized keywords,
        and tag the span with a label if it meets a certain correlation threshold

        Example:
            correlator(doc, doc[49:54])

        Args:
            doc (Doc): A spacy document that is being analyzed
            span (Span): A consecutive subset of the document
        
        """
        text = [span.text for span in spans]
        correlated = self.correlator(text)

        for span, score in zip(spans, correlated):
            if score > self.threshold:
                try:
                    doc.ents = list(doc.ents) + [
                        Span(doc, span.start, span.end, self.entity_tag)
                    ]
                except:
                    pass


def entity_correlation_tagger(doc, spans: List, threshold, corr_attr_key,
                              entity_tag):
    spans = [s for s in spans if s._.get(corr_attr_key) > threshold]

    for s in spans:
        try:
            doc.ents = list(
                doc.ents) + [Span(doc, s.start, s.end, label=entity_tag)]
        except:  # This case is hit if there are overlapping entities, there can only be one entity attached to each token at a time.
            pass


class KeywordCorrelator:
    """
    A helper class to correlate strings with a given set of keywords

    This class is initialized with a set of keywords which are embedded
    in a tensorflow model loaded from the URL defined by MODEL_URL

    Repeated calls can be made to the instance that embed a list of 
    strings and return corresponding correlation coefficients

    Example: 
        climate_correlator = KeywordCorrelator(climate_kwds)

    Args:
        keywords (List[str]): list of keyword phrases to embed
    """

    def __init__(self, keywords: List[str]) -> None:
        self.embed = EMBEDDER
        self.keywords = keywords
        self.keyword_embeddings = self.embed(self.keywords)

    @classmethod
    def add_span_subject_correlator(cls, tag_name: str, keywords: List[str]):
        """Special method to add a keyword correlator feature to any 
        span selected from a document.

        Once the span-subject-correlator is added to a spacy pipeline,
        a subset of the document will have a method:

        doc[x:y]._.<tag_name>

        Which will return the correlation of the span to the list of 
        embedded keywords provided to this function

        Example:
            KeywordCorrelator.add_span_subject_correlator("climate_corr", climate_kwds)

        Args:
            tag_name (str): desired name of callable extension
            keywords (List[str]): List of keywords to correlate on extension
        
        """
        correlator = KeywordCorrelator(keywords)
        correlator_getter = lambda span: correlator([span.text])[0]
        Span.set_extension(tag_name, getter=correlator_getter, force=True)

    def __call__(self, span: List[str]) -> List[float]:
        """Computes correlations of phrases to initialized set of keywords

        This method will embed a list of phrases against a list of keywords
        that were embedded on instantiation of this class

        Args:
            span (List[str]): A list of phrases to correlate against 
                the already-initialized list of embedded keywords.

        Return:
            correlation_1d (List[float]): List of correlation coefficients
                corresponding positionwise to each phrase that was passed
                to this function on call
        
        """
        input_embeddings = self.embed(span)
        correlation_2d = np.inner(self.keyword_embeddings, input_embeddings)
        correlation_1d = np.max(correlation_2d, axis=0)

        return correlation_1d


@Language.factory("kwd_correlate_factory")
class KeywordCorrelateSpacy:
    """A class to assist in finding related terms to a set of keywords

    This can be added to a spacy pipeline by running:
    nlp.add_pipe("kwd_correlate_factory",
                 config={
                        "tf_model": "https://tfhub.dev/google/universal-sentence-encoder/4",
                        "keywords": climate_change_keywords,
                        "correlation_tag": "climate_change_corr"
                        }
                )

    After running the pipeline, i.e. doc = nlp("some long ..... text document")
    for each item in doc, there will be a custom extensio that contains the relevance
    of the term to the list of keywords provided to this pipeline

    ex: doc[3]._.climate_change_corr will return the correlation of the fourth word
    in the document to the list of climate change keywords

    Args:
        tf_model: url to a tensorflow model that embeds sentences
        keywords: a list of keywords to relate to
    """

    def __init__(self, nlp: Language, name: str, tf_model: str,
                 keywords: List[str], correlation_tag: str):
        self.keywords = keywords
        self.embed = hub.load(tf_model)
        self.keyword_embeddings = self.embed(self.keywords)
        self.correlation_tag = correlation_tag
        Token.set_extension(correlation_tag, default=None)

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
            t._.set(self.correlation_tag, correlated[i])

        return doc


if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe(
        "kwd_correlate_factory",
        config={
            "tf_model": "https://tfhub.dev/google/universal-sentence-encoder/4",
            "keywords": [
                "resilliance", "sustainability", "mother nature",
                "green thought"
            ],
            "correlation_tag": "climate_change_corr"
        })

    doc = nlp("The earth will die if global warming continues")
    for i in range(len(doc)):
        print(f"{doc[i]} {doc[i]._.climate_change_corr}")
