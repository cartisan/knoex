import corpus
import nltk
from stat_parser import Parser
from nltk import word_tokenize
from preprocessor import pos_tag

print 'go'
print

#text = corpus.CorpusReader('corpora/snakes.corp').get_corpus((1.0))
text = corpus.CorpusReader('corpora/simple.corp').get_corpus((1.0))

sent = text.split('.')[0]

print sent
print

# --------------------------- STAT_PARSER ---------------------------- #

parser = Parser()

tree = parser.parse(sent)

print tree

nltk.draw.tree.TreeView(tree)
raw_input()


# --------------------------- OWN CFG -------------------------------- #

#sent = word_tokenize(sent)

tags = pos_tag(sent,1)
print tags
raw_input()


own_grammar = nltk.parse_cfg("""
S -> NP VP
PP -> P NP
NP -> Det N | Det N PP
VP -> V NP | VP PP
NP -> 'NP'
VP -> 'VP'
PP -> 'P'
""")

rd_parser = nltk.RecursiveDescentParser(own_grammar)

for p in rd_parser.nbest_parse(sent):
    print p
    nltk.draw.tree.TreeView(p)
    raw_input()


