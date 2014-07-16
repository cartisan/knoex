import corpus
import string
import re
import tree_combinations as tc
from preprocessor import parse_sentence
import nltk


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

def format_sentence(text):
    words = nltk.word_tokenize(text)
    return string.join(words)

def find_realation(text):

    # HEARST PATTERNS
    hp1 = 'NP\d+ such as ((NP\d+ ,d+ )+(and |or ))?NP\d+'

    def m2r_1(match,tree):
        NPs = re.findall(r'NP\d+', match)
        NPs = [string.join(tc.get_terminals(tree,NP)) for NP in NPs]
        return [(NP,'hyponym',NPs[0]) for NP in NPs[1:]]

    hp2 = 'NP0 VBZ0 NP1 \.0'

    def m2r_2(match,tree):
        subject = ' '.join(tc.get_terminals(tree,'NP0'))
        predicate = ' '.join(tc.get_terminals(tree,'VBZ0'))
        object_ = ' '.join(tc.get_terminals(tree,'NP1'))
        return [(subject,predicate,object_)]

    hp3 = 'NP\d+ is NP\d+'

    def m2r_3(match,tree):
        NNs = re.findall(r'NP\d+', match)
        NNs = [string.join(tc.get_terminals(tree,NN)) for NN in NNs]
        return [(NN,'hyponym',NNs[0]) for NN in NNs[1:]]


    #m2r = [ m2r_1, m2r_2, m2r_3  ] # functions to map matches on relations
    #pattern_list = [hp1,hp2,hp3]
    m2r = [ m2r_2 ] # functions to map matches on relations
    pattern_list = [hp2]

    sentences = split_into_sentences(text)


    # The next part is rather unclean, but it's hopefully gonna work
    # Produces a string where every noun phrase is preplaced by NP1,... to NPn
    # Then a regex search for hearst patterns is applied to find hyponym relations

    relations = []
    for s in sentences:
        s = format_sentence(s)
        s+=' .' # adding a fullstop in the end to satisfy the needs of stanford parser
        tree  = parse_sentence(s)

        tc.numerate_non_terminals(tree) 

        combi = tc.all_parsing_combinations(tree)

        combi = [string.join(c) for c in combi]

        #for c in combi :
        #    print c

        #for c in combi : print c
        for i, pattern in enumerate(pattern_list) :
            pattern = re.compile(pattern)
            #open('combi','w').write(str(combi).replace(',','\n'))
            for c in combi :
                match = re.match(pattern,c)
                if match :
                    print 'match : ', match.group(), ' --> ', c
                    match = match.group()
                    if match :
                        tmp = m2r[i](match,tree)
                        print type(tmp), ' -- ', tmp
                        relations.extend(tmp)
    print 'relations', relations
    return set(relations)

# \{TERM\d+\} such as ((\{TERM\d+\},)+(and|or))? \{TERM\d+\}

if __name__ == '__main__' :
    import sys

    if len(sys.argv) > 1 :
        text = sys.argv[1]
    else :
        # create list of sentences
        text = 'Snakes, such as pythons, cobras and vipers are poisonous reptiles.'
        #text = 'Snakes such as pythons are long reptiles'
        #text = 'A tiger is a cat'
        text = 'Leon hits Kai.'

    relations = find_realation(text)
    print
    for r in relations :
        print r