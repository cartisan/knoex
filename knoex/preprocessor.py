from utils import setup_nltk_resources

from nltk import word_tokenize
from nltk import pos_tag as nltk_pos_tag
from nltk.tag.simplify import simplify_wsj_tag
from nltk.tokenize import sent_tokenize


def pos_tag(text, simple=False):
    """ Tokenizes a given text and determines the pos-tags. Lowercases
        the text.

     Params:
        text: string to be tokenized
        simple: boolean indicating weather to simplify the pos tags

    Returns:
        list of tuples of form (token, pos-tag)
    """

    # check availability of nltk resources for pos-tagging
    resources = ['punkt',
                 'maxent_treebank_pos_tagger']
    setup_nltk_resources(resources)

    # tokenize to sentences, then to tokens
    tokens = [token.lower() for sen in sent_tokenize(text)
              for token in word_tokenize(sen)]

    # generate pos-tags
    pos = nltk_pos_tag(tokens)

    # simplify tags if requested
    if simple:
        pos = [(word, simplify_wsj_tag(tag)) for word, tag in pos]

    return pos
