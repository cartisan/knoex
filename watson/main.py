from os import popen

from nltk.parse.stanford import StanfordParser
from nltk.tree import Tree

import dot_interface
#import tree_patterns
import configurations as conf
from tree_patterns import TreePatternMatcher


sent = ["My name is Johannes."]

parser = StanfordParser(conf.stanford_parser,conf.stanford_models)
trees = parser.raw_parse_sents(sent)

for i,tree in enumerate(trees) :
    tree = tree[0]
    dot_code = dot_interface.nltk_tree_to_dot(tree)
    dot_interface.dot_to_image(dot_code, 'temp_tree_' + str(i))
    popen(conf.image_viewer + ' temp_tree_' + str(i) + '.png')

    matcher = TreePatternMatcher('NP VP')



#pattern = load_pattern(some_filename)

