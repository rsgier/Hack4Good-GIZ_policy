#graphing/visualization packages:
import matplotlib.pyplot as plt

plt.style.use('ggplot')


def calculate_word_freq_ndc(word_freq: dict[str, int],
                            ndc_dict: dict[str, list[str]], key: str):
    """
    Input: The word frequencies calculated by the Counter for the whole document (word_freq), 
    the dictionary of ndc key words organized by topic (ndc_dict), and the ndc topic (key).
    Output: Pull out the word frequencies (word_scores) for each of the NDC words associated 
    with a topic (words) for graphing.
    """
    words = ndc_dict[key]
    word_scores = []
    for word in words:
        word_scores.append(word_freq[word])
    print((
        "This document has the following number of words related to %s NDCs: " %
        (key)), sum(word_scores), '\n')
    return words, word_scores


def graph_word_freq_ndc(words,
                        word_scores,
                        ndc_name,
                        doc_name,
                        output_folder,
                        save=False):
    """
    Input: The word frequencies (word_scores) for the NDC words associated 
    with a topic (words) for graphing, including the associated NDC topic (ndc_name) and 
    document name (doc_name) to include in graph and file name for output to the output_folder. 
    Output: Bar graph in the output folder of word frequencies for the NDC words associated 
    with a topic/theme.
    """
    #input data
    x = words
    y = word_scores
    x_pos = [i for i, _ in enumerate(x)]

    #set plot parameters
    plt.rcParams["figure.figsize"] = ((len(words) / 3), 4)
    plt.bar(x, y, color='mediumseagreen')
    plt.xlabel("NDC words: %s" % (ndc_name))
    plt.ylabel("Frequency")
    title = ("%s NDC words in: %s" % (ndc_name, doc_name))
    plt.title(title)
    plt.xticks(x_pos, x, rotation=90)
    if save:
        plt.savefig((output_folder + 'bar_chart_%s.pdf' % (title)),
                    bbox_inches='tight')
    plt.show()