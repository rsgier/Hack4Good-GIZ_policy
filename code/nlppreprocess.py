#NLP related helper functions
#used these resources:
#https://www.geeksforgeeks.org/nlp-expand-contractions-in-text-processing/)
#https://realpython.com/natural-language-processing-spacy-python/#how-to-download-models-and-data

import codecs
import contractions
import spacy
from collections import OrderedDict
from typing import List, Dict, Tuple


# for multi-language: spacy.load('xx_ent_wiki_sm')
nlp = spacy.load(
    'en_core_web_sm')

def fix_contractions(document: str) -> str:
    """Expands text, such that potentially important words
     are not removed with punctuation removal (e.g. can't is expanded to cannot).

     Args:
        document (str): input policy document to be analysed

     Returns (str):
        text with expanded contractions
    """

    # read original contracted text
    with codecs.open(document, errors="ignore", encoding="utf8") as f:
        text = f.read()

    # create empty list
    expanded_words = []
    for word in text.split():
        # use contractions.fix to expand the shortened words
        expanded_words.append(contractions.fix(word))

    expanded_text = ' '.join(expanded_words)
    return expanded_text

def is_token_allowed(token: object) -> bool:
    """ Checks whether token in not a stop word or punctuation symbol.

    Args:
        token (object): input spacy token object

    Returns (bool)
        True if token is not stop word or punctuation symbol, False otherwise
    """

    if (not token or not token.text.strip() or token.is_stop or token.is_punct):
        return False
    return True


def preprocess_token(token: object) -> str:
    """ Computes the lowercase lemma form of the input token.

    Args:
        token (object): input spacy token opject

    Returns (str):
        lowercase lemma form of the input token
    """
    return token.lemma_.strip().lower()

def preprocess_token_no_lemma(token: object) -> str:
    """ Computes the lowercase, stripped form of the input token.

    Args:
        token (object): input spacy token opject

    Returns (str):
        lowercase lemma form of the input token
    """
    return token.text.strip().lower()


def preprocess_doc(doc_path: str) -> Tuple[object, List[object], List[object]]:
    """Applies NLP framework to a document.

    Args:
        doc_path (str): path to the input document

    Returns:
        tokens (object): word tokens
        token_list (List[object]): list of the word tokens
        sentences (List[object]): sentence tokens
    """

    # TODO: check functionality and output of spacy (nlp) and potentially condense functions

    # remove contracted words and tokenize the document
    tokens = nlp(fix_contractions(doc_path))
    token_list = [token for token in tokens]

    # sentence tokens
    sentences = list(tokens.sents)
    return tokens, token_list, sentences


def filter_modify_tokens(tokens: List[object]) -> List[object]:
    """ This function takes a collection of tokens from the nlp() function applied to text
    and generates a list of filtered tokens that we then convert into a filtered text and
    collection of filtered tokens.

    Args:
        tokens (List[object]): list of input tokens

    Returns (List[object]):
        list of filtered tokens
    """

    # TODO: still need to filter out super weird non words and may want to filter numbers and
    # may want to find some important accronyms too (so maybe modify this function later)

    # filter tokens, and make lowercase and lemmatize:
    filtered_text_list = [
        preprocess_token(token) for token in tokens if is_token_allowed(token)
    ]

    filtered_text = ' '.join(filtered_text_list)
    filtered_tokens = nlp(filtered_text)
    return filtered_tokens

def filter_tokens(tokens: List[object]) -> List[object]:
    """ This function takes a collection of tokens from the nlp() function applied to text
    and generates a list of filtered tokens that we then convert into a filtered text and
    collection of filtered tokens. (But without lemmatization.)

    Args:
        tokens (List[object]): list of input tokens

    Returns (List[object]):
        list of filtered tokens
    """

    # TODO: still need to filter out super weird non words and may want to filter numbers and
    # may want to find some important accronyms too (so maybe modify this function later)

    # filter tokens, and make lowercase and lemmatize:
    filtered_text_list = [
        preprocess_token_no_lemma(token) for token in tokens if is_token_allowed(token)
    ]

    filtered_text = ' '.join(filtered_text_list)
    filtered_tokens = nlp(filtered_text)
    return filtered_tokens


def make_filtered_tokens_from_ndc(ndc_dict: Dict) -> Dict[str, List[str]]:
    """Takes an NDC dictionary and processes the topics and keywords for searching within the documents,
    assuming we are searching for individual words and to process the words in the same way are processing
    the document text to have the best chance of finding keywords in the documents.

    Args:
        ndc_dict (dict): input NDC dictionary including topics and keywords

    Returns (dict):
        dictionary of the processed words of the NDC dictionary
    """

    ndc_dict_processed = dict()

    for i in range(0, len(list(ndc_dict.keys()))):
        topic = list(ndc_dict.keys())[i]
        keywords = list(ndc_dict.values())[i]

        # add keywords from topic (key) to list of values and tokenize those values
        keywords.append(topic)
        keywords_tokens = nlp(' '.join(keywords))

        # generate a filtered list of keywords
        # using the same token preprocessing we use in the documents
        keywords_tokens_list = [
            str(token) for token in filter_modify_tokens(keywords_tokens)
        ]
        # filter non-unique words generated by splitting terms
        # with shared words (e.g. two types of 'plan')
        unique_keywords = list(OrderedDict.fromkeys(keywords_tokens_list))
        ndc_dict_processed[topic] = unique_keywords

    return ndc_dict_processed

def make_ndc_keyword_df_from_dict(ndc_dict: Dict[str, List[str]],
                                  topic: str,
                                  col_topic_name: str,
                                  ) -> pd.DataFrame:
    """Takes a NDC dictionary of the processed words, the name of the topic and the title for the
    topic-column and creates a pandas dataframe.

    Args:
        ndc_dict (Dict[str, List[str]]): NDC dictionary of the processed words
        topic (str): topic associated with the NDC keywords
        col_topic_name (str): name of the column containing the topics

    Returns:
        ndc_df (pd.DataFrame): A pd.DataFrame with one column with the keywords
        and one column with the associated topic
    """

    ndc_df = pd.DataFrame({'keyword': ndc_dict[topic],
                           col_topic_name: topic})

    return ndc_df


def stack_ndc_keyword_dfs(ndc_dict: Dict[str, List[str]],
                          col_topic_name: str) -> pd.DataFrame:
    """Takes a NDC dictionary of the processed words, the title for the
    topic-column and creates a pandas dataframe by concatenating dataframes
    for all topics in the NDC dictionary.

    Args:
        ndc_dict (Dict[str, List[str]]): NDC dictionary of the processed words
        col_topic_name (str): name of the column containing the topics

    Returns:
        ndc_df (pd.DataFrame): A pd.DataFrame with one column with the keywords
        and one column with the associated topics
    """

    ndc_df = pd.DataFrame()

    for topic in ndc_dict.keys():
        ndc_df_add = make_ndc_keyword_df_from_dict(ndc_dict, topic, col_topic_name)
        ndc_df = pd.concat([ndc_df, ndc_df_add], axis=0)

    return ndc_df

def make_ndc_idx_df(ndc_dict: Dict[str, List[str]],
                    col_topic_name: str,
                    tokens: List[object]) -> pd.DataFrame:
    """Takes a NDC dictionary of the processed words, a collection of tokens from the nlp() function,
    the title for the topic-column and creates a pandas dataframe containing the indices for each token
    by concatenating dataframes for all topics in the NDC dictionary.

    Args:
        ndc_dict (Dict[str, List[str]]): NDC dictionary of the processed words
        col_topic_name (str): name of the column containing the topics
        tokens (List[object]): list of input tokens

    Returns:
        ndc_df (pd.DataFrame): A pd.DataFrame with one column with the topics
        and one column with the word index for each token
    """

    ndc_idx_df = pd.DataFrame()

    for topic in ndc_dict.keys():
        ndc_idx_df_to_add = pd.DataFrame({col_topic_name: topic,
                                          'word_index': [token.idx for token in tokens if token.text in ndc_dict[topic]]})
        ndc_idx_df = pd.concat([ndc_idx_df, ndc_idx_df_to_add], axis=0)

    return ndc_idx_df