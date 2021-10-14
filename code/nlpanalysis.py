#graphing/visualization packages:
import matplotlib.pyplot as plt

plt.style.use('ggplot')


def topic_frequency_subset(document_frequency: dict[str, int],
                           topic_to_keywords: dict[str, list[str]],
                           topic: str) -> dict[str, int]:
    """Returns a frequency table of keywords from a topic area

    Formerly calculate_word_freq_ndc(dict, dict, str) -> list, list

    Args:
        document_frequency: a mapping of all words in a document to their frequency
        topic_to_keywords: a mapping of all topics to their relevant keywords
        topic: the topic for which to find keyword frequencies

    Returns:
        A dictionary mapping topic-defined keywords to their respective frequencies

    """
    word_frequencies = {
        word: document_frequency[word] for word in topic_to_keywords[topic]
    }

    return word_frequencies


def graph_word_freq_ndc(topic_term_frequencies: dict[str, int],
                        topic: str,
                        doc_name: str,
                        output_folder: str,
                        save=False):
    """Graphs keyword frequencies found in an individual document

    Args:
        frequencies: a keyword to frequency mapping
        topic: topic containing keyword subset to plot 
        doc_name: document on which frequency analysis has been made
        output_folder: folder path to output a pdf of the plot
        save: boolean to enable saving of a plot pdf (default False)
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