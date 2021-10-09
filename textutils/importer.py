
import nltk, codecs

class TextImporter:

    def __init__(self, path) -> None:
        with codecs.open(path, errors='ignore', encoding="utf8") as f:
            self.text = f.read()

    def tokenize_text(self):
        return nltk.word_tokenize(self.text)