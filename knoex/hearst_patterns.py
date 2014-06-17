import corpus
import string
import re
import tree_combinations as tc
from stat_parser import parser 


# primitve method : replace by something from NLTK !
def split_into_sentences(text):
    text = text.replace('!','.')
    text = text.replace('?','.')
    text = text.replace(':','.')
    sentences = text.split('.')
    nos = len(sentences) # number of sentences

    # remove useless blankspace and newline
    for i in range(nos) :
        sentences[i] = sentences[i].strip()
        print sentences[i]

    # remove 'empty' sentences
    if not sentences[-1]:
        del sentences[-1]
        nos-=1

    return sentences


# HEARST PATTERNS
hp1 = 'NP\d+ such as ((NP\d+,? )+(and |or ))?NP\d+'

def m2r_1(match,tree):
    NPs = re.findall(r'NP\d+', match)
    NPs = [string.join(tc.get_terminals(NP,tree)) for NP in NPs]
    return [(NP,'hyponym',NPs[0]) for NP in NPs[1:]]

hp2 = 'NN\d+ such as ((NN\d+,? )+(and |or ))?NN\d+'

def m2r_2(match,tree):
    NNs = re.findall(r'NN\d+', match)
    NNs = [string.join(tc.get_terminals(NN,tree)) for NN in NNs]
    return [(NN,'hyponym',NNs[0]) for NN in NNs[1:]]

hp3 = 'NP\d+ is NP\d+'

def m2r_3(match,tree):
    NNs = re.findall(r'NP\d+', match)
    NNs = [string.join(tc.get_terminals(NN,tree)) for NN in NNs]
    return [(NN,'hyponym',NNs[0]) for NN in NNs[1:]]


m2r = [ m2r_1, m2r_2, m2r_3  ] # functions to map matches on relations
pattern_list = [hp1,hp2,hp3]


# create list of sentences
text = 'Snakes, such as pythons, cobras and vipers are poisonous reptiles'
text = 'A tiger is a cat'
sentences = split_into_sentences(text)


# The next part is rather unclean, but it's hopefully gonna work
# Produces a string where every noun phrase is preplaced by NP1,... to NPn
# Then a regex search for hearst patterns is applied to find hyponym relations

P = parser.Parser()
hyponyms = []
for s in sentences:
    tree  = P.parse(s)
    print tree
    tc.numerate_non_terminals(tree) 
    print tree
    print
    combi = tc.all_parsing_combinations(tree)
    combi = [string.join(c) for c in combi]
    #for c in combi : print c
    for i, pattern in enumerate(pattern_list) :
        pattern = re.compile(pattern)
        for c in combi :
            print c
            match = re.match(pattern,c)
            if match :
                match = match.group()
                if match :
                    hyponyms.extend(m2r[i](match,tree))

print hyponyms

# \{TERM\d+\} such as ((\{TERM\d+\},)+(and|or))? \{TERM\d+\}