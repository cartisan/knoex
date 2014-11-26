from os import popen

from nltk.parse.stanford import StanfordParser
from nltk.tree import Tree

import dot_interface
#import tree_patterns
import configurations as conf


sent = ["My name is Johannes.", "I come from Bayern."]

parser = StanfordParser(conf.stanford_parser,conf.stanford_models)
trees = parser.raw_parse_sents(sent)

a = str(trees[0][0])
print a
Tree.fromstring(a)

for i,tree in enumerate(trees) :
    tree = tree[0]
    dot_code = dot_interface.nltk_tree_to_dot(tree)
    dot_interface.dot_to_image(dot_code, 'temp_tree_' + str(i))
    popen(conf.image_viewer + ' temp_tree_' + str(i) + '.png')




#pattern = load_pattern(some_filename)

