#graphing/visualization packages:
from typing import Dict
import matplotlib.pyplot as plt

plt.style.use('ggplot')


def calculate_topic_frequency_subset(document_frequency: Dict[str, int],
                                     topic_to_keywords: Dict[str, list[str]],
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
