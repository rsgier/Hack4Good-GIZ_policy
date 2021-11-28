#graphing/visualization packages:
from typing import Dict, List
import matplotlib.pyplot as plt
from typing import List, Tuple
import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
from spacy import displacy
import pandas as pd


nlp = spacy.load(
    'en_core_web_sm')

plt.style.use('ggplot')

def calculate_topic_frequency_subset(document_frequency: Dict[str, int],
                                     topic_to_keywords: Dict[str, List[str]],
                                     topic: str) -> Dict[str, int]:
    """Returns a frequency table of keywords from a topic area.

    Args:
        document_frequency (Dict[str, int]): a mapping of all words in a document to their frequency
        topic_to_keywords (Dict[str, list[str]]): a  mapping of all topics to their relevant keywords
        topic (str): the topic for which to find keyword frequencies

    Returns:
        word_frequencies (Dict[str, int]): A dictionary mapping topic-defined keywords to their
            respective frequencies

    """
    word_frequencies = {
        word: document_frequency[word] for word in topic_to_keywords[topic]
    }

    return word_frequencies


def plot_word_freq_barchart_ndc(topic_term_frequencies: Dict[str, int],
                                topic: str,
                                doc_name: str,
                                output_folder: str,
                                save=False):
    """Graphs keyword frequencies found in an individual document

    Args:
        frequencies (Dict[str, int]): a keyword to frequency mapping
        topic (str): topic containing keyword subset to plot
        doc_name (str): document on which frequency analysis has been made
        output_folder (str): folder path to output a pdf of the plot
        save (bool): to enable saving of a plot pdf (default False)
    """
    #input data
    keywords = topic_term_frequencies.keys()
    frequencies = topic_term_frequencies.values()
    kwd_pos = list(range(len(keywords)))

    #set plot parameters
    plt.rcParams["figure.figsize"] = ((len(keywords) / 3), 4)
    plt.bar(keywords, frequencies, color='mediumseagreen')
    plt.xlabel(f"NDC words: {topic}")
    plt.ylabel("Frequency")
    title = (f"{topic} NDC words in: {doc_name}")
    plt.title(title)
    plt.xticks(kwd_pos, keywords, rotation=90)
    if save:
        plt.savefig((output_folder + 'bar_chart_%s.pdf' % (title)),
                    bbox_inches='tight')
    plt.show()

def filter_idx_for_overlap(idxs: List[int],
                           min_dist: int) -> List[int]:
    """Takes a list with word indices and returns another list
     only with word indices separated by at least a minimum distance.

    Args:
        idxs (List[int]): list with word indices
        min_dist (int): minimum distance between word indices

    Returns:
        filtered_idxs (List[int]): list with word indices separated by at least min_dist
    """

    distance_btwn_idxs = [(idxs[i + 1] - idxs[i]) for i in range(0, len(idxs) - 1)]

    filtered_idxs = []
    for index, distance in enumerate(distance_btwn_idxs):
        if distance >= min_dist:
            filtered_idxs.append(idxs[index])
        else:
            pass

    print("Total number of word indices: {}".format(len(idxs)), "\n",
          "Number of word indices seperated by at least min_dist={}: {}"
          .format(min_dist, len(filtered_idxs)))

    return filtered_idxs


def make_window_text(tokens: List[object],
                     max_length: int) -> List[object]:
    """Takes a collection of tokens from the nlp() function and removes
    tokens with equal or more than max_length characters.

    Args:
        tokens (List[object]): list of input tokens
        max_length: (int): max. allowed no. of characters for the tokens

    Returns:
        tokens (List[object]): list of tokens with less than max_length characters
    """
    filtered_for_length = [token.text.lower() for token in tokens if len(token) < max_length]
    text_for_windows = ' '.join(filtered_for_length)
    window_tokens = nlp(text_for_windows)

    return window_tokens

def return_window(ndc_word_index: int,
                  tokens: List[object],
                  size: int) -> Tuple[int, int, List[object]]:
    """Gives the tokens within a window of user-specific size around a given word index

    Args:
        ndc_word_index (index): word index around which the window is defined
        tokens: (List[object]): list of input tokens which are checked if inside the window
        size: size of the token window around the word index (ndc_word_index +/- size)

    Returns:
        lower limit (int): lower limit index of the token window
        upper limit (int): upper limit index of the token window
        window_tokens (List[object]): list of tokens inside the token window
    """

    lower_limit = ndc_word_index - size
    upper_limit = ndc_word_index + size
    token_idxs = [token.idx for token in tokens]
    window_token_list = []

    for index, idx in enumerate(token_idxs):
        if (idx >= lower_limit) and (idx <= upper_limit):
            window_token_list.append(tokens[index])
        else:
            pass
    text_for_windows = ' '.join(list(token.text for token in window_token_list))
    window_tokens = nlp(text_for_windows)

    return lower_limit, upper_limit, window_tokens

def label_ndc_sdg_spans_in_windows(keyword_df: pd.DataFrame,
                                   doc: List[object],
                                   topic_column: str) -> Tuple[List[str], List[object]]:
    """Takes a nlp-processes window text and labels the keywords from a pandas dataframe

    Args:
        keyword_df (pd.DataFrame): dataframe containing the SDG keywords to be labelled
        doc: (List[object]): nlp-processed window text to be labelled
        topic_column (str): topic name for the column

    Returns:
        entity_labels (List[str]): List containing the SDG names for the labels
        doc (List[object]): Labelled nlp-processed window text
    """

    matcher = PhraseMatcher(nlp.vocab)

    # iterate through NDC keys in NDC dictionary
    # to create separate label categories for the matching
    entity_labels = []
    topics = list(keyword_df[topic_column].value_counts().index)
    for topic in topics:
        entity_labels.append(topic)
        keywords = list(keyword_df[keyword_df[topic_column]==topic]['keyword'])
        patterns = [nlp(i) for i in keywords]
        matcher.add(topic, None, *patterns)

    matches = matcher(doc)
    for match_id, start, end in matches:
        try:
            span = Span(doc, start, end, label=match_id)
            doc.ents = list(doc.ents) + [span]  # add span to doc.ents
        except:
            pass

    return entity_labels, doc