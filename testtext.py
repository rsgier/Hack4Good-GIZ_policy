'''
This module  a docstring now
'''
import nltk
from textutils.importer import TextImporter

nltk.download('punkt')

print(TextImporter('texts/AnnualReport2017-2018.txt').tokenize_text())
