import nltk
from nltk.util import ngrams
from nltk.tag.simplify import simplify_wsj_tag
# download nltk resources for tokenization
nltk.data.load('tokenizers/punkt/english.pickle')
nltk.data.load('taggers/maxent_treebank_pos_tagger/english.pickle')

# read and tokenize text
f = open('corpora/easy', 'r')
text = f.read()
f.close()

tokens = [token for sen in nltk.tokenize.sent_tokenize(text)
          for token in nltk.word_tokenize(sen)]

# generate pos-tags
pos_tags = nltk.pos_tag(tokens)

# linguistic filter
# find all sequences of the form (Noun|Adjective)+(Noun)
# (according to Frantzi_97)
pos_tags = [(word, simplify_wsj_tag(tag)) for word, tag in pos_tags]
multi_term_parser = nltk.RegexpParser('CHUNK: {<N|ADJ>+<N>}')
tree = multi_term_parser.parse(pos_tags)
multi_terms = [subtree.leaves() for subtree in tree.subtrees()
               if subtree.node == "CHUNK"]


# c-vaues
# nc-values
