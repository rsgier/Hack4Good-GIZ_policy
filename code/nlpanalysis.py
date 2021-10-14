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


def graph_word_freq_ndc(frequencies: dict[str, int],
                        topic: str,
                        doc_name: str,
                        output_folder: str,
                        save=False):
    """Graphs keyword frequencies found in an individual document
    Input: The word frequencies (word_scores) for the NDC words associated 
    with a topic (words) for graphing, including the associated NDC topic (ndc_name) and 
    document name (doc_name) to include in graph and file name for output to the output_folder. 
    Output: Bar graph in the output folder of word frequencies for the NDC words associated 
    with a topic/theme.

    Args:
        frequencies: a keyword to frequency mapping
        topic: the 
    """
    #input data
    x = words
    y = word_scores
    x_pos = [i for i, _ in enumerate(x)]

    #set plot parameters
    plt.rcParams["figure.figsize"] = ((len(words) / 3), 4)
    plt.bar(x, y, color='mediumseagreen')
    plt.xlabel(f"NDC words: {ndc_name}")
    plt.ylabel("Frequency")
    title = (f"{ndc_name} NDC words in: {doc_name}")
    plt.title(title)
    plt.xticks(x_pos, x, rotation=90)
    if save:
        plt.savefig((output_folder + 'bar_chart_%s.pdf' % (title)),
                    bbox_inches='tight')
    plt.show()