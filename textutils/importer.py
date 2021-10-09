"""textutils.importer for GIZ-Policy"""

import codecs
import nltk


class TextImporter:
    """Assists in importing text files that may contain unknown characters

    Some files produced by OCR engines may contain invalid UTF-8 and ASCII
    characters that are not compatible with NLP libraries. This class will
    import a text file safely and provide methods for accessing the text.

        Typical usage example:

        report = TextImporter("annualreport.txt")
        tokens = report.tokenize_text()

    Parameters:
        text (str): raw text of imported file

    """

    def __init__(self, path) -> None:
        with codecs.open(path, errors="ignore", encoding="utf8") as f:
            self.text = f.read()

    def nltk_tokenize_text(self):
        """Tokenizes imported text with nltk library"""
        return nltk.word_tokenize(self.text)
