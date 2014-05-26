import corpus
import nltk
from stat_parser import Parser

print 'go'
print

text = corpus.CorpusReader('corpora/snakes.corp').get_corpus((6.0))
#text = corpus.CorpusReader('corpora/simple.corp').get_corpus((1.0))

first_sentence = text.split('.')[0]

print first_sentence
print

parser = Parser()

tree = parser.parse(first_sentence)

print tree

nltk.draw.tree.TreeView(tree)