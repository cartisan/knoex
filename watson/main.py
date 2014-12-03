from os import popen

from nltk.parse.stanford import StanfordParser
from nltk.tree import Tree

import dot_interface
#import tree_patterns
import configurations as conf
from tree_patterns import TreePatternMatcher, MatchTree


sent = ["I am 27."]

parser = StanfordParser(conf.stanford_parser,conf.stanford_models)

print "parsing sentence ..."
trees = parser.raw_parse_sents(sent)

for i,tree in enumerate(trees) :
    tree = tree[0]
    print 'saving as .png ...'
    dot_code = dot_interface.nltk_tree_to_dot(tree)
    dot_interface.dot_to_image(dot_code, 'temp_tree_' + str(i))
    popen(conf.image_viewer + ' temp_tree_' + str(i) + '.png')

    matcher = TreePatternMatcher()

    match_tree = MatchTree(tree)

    print 'matching patterns ...'
    all_matches = matcher.match_all(match_tree)
    	
    for i,matches in enumerate(all_matches) :
    	if matches == [] :
    		print 'No matches for', pattern_list[i], '!!'
    	for match in matches :
    		print [node.label() for node in match],\
    		 [MatchTree.get_terminals(node) for node in match]





#pattern = load_pattern(some_filename)

