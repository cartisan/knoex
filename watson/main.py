import os

from nltk.parse.stanford import StanfordParser
from nltk.tree import Tree

import dot_interface
#import tree_patterns
import configurations as conf
from tree_patterns import TreePatternMatcher, MatchTree, load_pattern_list


sent = ["What is water?"]

parser = StanfordParser(conf.stanford_parser,conf.stanford_models)

print "parsing sentence ..."
trees = parser.raw_parse_sents(sent)

pattern_list, semantic_translations = load_pattern_list()

for i,tree in enumerate(trees) :
    tree = tree[0] # cut root node
    png_path = 'temp_tree_' + str(i) + '.png'

    if True : #not os.path.exists(png_path) :
        print 'saving as .png ...'
        dot_code = dot_interface.nltk_tree_to_dot(tree)
        dot_interface.dot_to_image(dot_code, 'temp_tree_' + str(i))
        os.popen(conf.image_viewer + ' ' + png_path)

    matcher = TreePatternMatcher()

    match_tree = MatchTree(tree)

    print 'matching patterns ...'
    all_matches = matcher.match_all(match_tree)
    
    for i,matches in enumerate(all_matches) :
    	if matches == [] :
    		print 'No matches for', pattern_list[i], '!!'
    	for match in matches :
    		print 'Match for',[str(node.label()) for node in match],'->',\
    		 [str(' '.join(MatchTree.get_terminals(node))) for node in match]





#pattern = load_pattern(some_filename)

