"""
Tools for analyzing the frequency of tokens
within a document
"""

import nltk
from typing import List


class WordCount:
    """Wraps term counting functionality

    Args:
        tokens (list[str]): a list of tokens from a preprocessing step
    """

    def __init__(self, tokens: List[str]):
        self.tokens = tokens

    def get_total_token_count(self) -> int:
        """Returns the total token count"""
        return len(self.tokens)

    def get_frequency_table(self):
        """Converts tokens to a term frequency table

        Return:
            nltk.FreqDist dictionary mapping each word in a document
            to its frequency
        """
        return nltk.FreqDist(self.tokens)
