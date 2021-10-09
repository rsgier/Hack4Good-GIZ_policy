from typing import Text
import textutils
from textutils.importer import TextImporter
import nltk
nltk.download('punkt')
print(TextImporter('texts/AnnualReport2017-2018.txt').tokenize_text())