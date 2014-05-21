from math import log
import nltk
from preprocessor import pos_tag
from nltk.util import ngrams


MULTI_TERM_PARSER = nltk.RegexpParser('CHUNK: {<N|ADJ>*<N>}')


def find_multi_word_terms(pos_tags):
    def _candidate_words(pos_tags):
        tree = MULTI_TERM_PARSER.parse(pos_tags)
        return [subtree.leaves() for subtree in tree.subtrees()
                if subtree.node == "CHUNK"]

    # find all maximal multi word terms
    candidates = _candidate_words(pos_tags)

    # check weather candidates contain sub words
    sub_words = []
    for mult_word in candidates:
        # create all ngrams with size n-1..1
        for n in range(len(mult_word)-1, 0, -1):
            # extract candidates from each ngram
            for ngram in ngrams(mult_word, n):
                sub_words += _candidate_words(list(ngram))

    return candidates+sub_words


def c_value(ngram, corpus, max_n):
    if len(ngram) == max_n:
        # zip(*ngram)[0] returns a tuple with words from a (word,tag) list
        return log(max_n, 2) * corpus.lower().count(" ".join(zip(*ngram)[0]))

    # TODO: fill in!
    return 0


def compute_c_nc():
    f = open('corpora/easy', 'r')
    text = f.read()
    f.close()

    pos_tags = pos_tag(text, True)

    # linguistic filter
    # find all n-grams of the form (Noun|Adjective)*(Noun)
    # (according to Frantzi_97)
    candidates = find_multi_word_terms(pos_tags)

    # c-vaues
    max_len = max([len(ngram) for ngram in candidates])
    c_values = [c_value(ngram, text, max_len) for ngram in candidates]

    # nc-values
    pass
