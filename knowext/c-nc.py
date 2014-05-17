import pdb
from math import log
import nltk
from nltk.tag.simplify import simplify_wsj_tag
from nltk.util import ngrams

multi_term_parser = nltk.RegexpParser('CHUNK: {<N|ADJ>*<N>}')


def c_value(token, max_len):
    pass


def find_multi_word_terms(pos_tags):
    # find all multi word terms
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


def _candidate_words(pos_tags):
    tree = multi_term_parser.parse(pos_tags)
    return [subtree.leaves() for subtree in tree.subtrees()
            if subtree.node == "CHUNK"]


# download nltk resources for tokenization
nltk.data.load('tokenizers/punkt/english.pickle')
nltk.data.load('taggers/maxent_treebank_pos_tagger/english.pickle')

# read and tokenize text
f = open('corpora/easy', 'r')
text = f.read()
f.close()

tokens = [token.lower() for sen in nltk.tokenize.sent_tokenize(text)
          for token in nltk.word_tokenize(sen)]

# generate pos-tags
pos_tags = nltk.pos_tag(tokens)

# linguistic filter
# find all n-grams of the form (Noun|Adjective)*(Noun)
# (according to Frantzi_97)
pos_tags = [(word, simplify_wsj_tag(tag)) for word, tag in pos_tags]
candidates = find_multi_word_terms(pos_tags)

# c-vaues
max_len = max([len(ngram) for ngram in candidates])
c_values = [log(len(ngram), 2) for ngram in candidates]

# nc-values
