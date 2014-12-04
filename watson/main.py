import os
from time import sleep
from itertools import chain
from random import choice

from nltk.parse.stanford import StanfordParser
from nltk.tree import Tree

import dot_interface
#import tree_patterns
import configurations as conf
from tree_patterns import TreePatternMatcher, MatchTree, load_pattern_list
from utils_2 import lemma, ner, stem


speech = False

if speech : from utils import text_to_speech

silent = True
max_answer_number = 5

speaker = 'google'

def answer_question(sent) :

    parser = StanfordParser(conf.stanford_parser,conf.stanford_models)

    print "parsing sentence ..."
    trees = parser.raw_parse_sents(sent)

    pattern_list, semantic_translations = load_pattern_list()

    for i,tree in enumerate(trees) :
        tree = tree[0] # cut root node

        png_path = 'temp_tree_' + str(i) + '.png'
        if True : #not silent : #not os.path.exists(png_path) :
            print 'saving parse tree as .png ...'
            dot_code = dot_interface.nltk_tree_to_dot(tree)
            dot_interface.dot_to_image(dot_code, 'temp_tree_' + str(i))
            os.popen(conf.image_viewer + ' ' + png_path)

        matcher = TreePatternMatcher()

        match_tree = MatchTree(tree)

        print 'matching patterns ...'
        all_matches = matcher.match_all(match_tree)
        
        for i,matches in enumerate(all_matches) :
            if silent :
                break
            if matches == [] :
        		print 'No matches for', pattern_list[i], '!!'
            for match in matches :
        		print 'Match for',[str(node.label()) for node in match],'->',\
        		 [str(' '.join(MatchTree.get_terminals(node))) for node in match]


        if not reduce(lambda x,y : x or y,all_matches) :
            no_match = "Could not match any patterns."
            print no_match
            if speech : text_to_speech(no_match,speaker)
            return

        answers = matcher.semantics_all(all_matches)

        answers = list(chain(*answers))

        print

        if len(answers) == 0:
            sorry = "Sorry but I can't find any answers!"
            print sorry
            if speech : text_to_speech(sorry,speaker)
            return

        print answers[0]
        sleep(1)
        for c in answers[0].split(';') :
            if speech : text_to_speech(c,speaker)

        for i,a in enumerate(answers[1:]) :
            if i+1 == max_answer_number :
                break
            sleep(1)
            if speech : text_to_speech('or','espeak')
            print a
            sleep(1)
            for c in a.split(';') :
                if speech : text_to_speech(c,speaker)


def qa_loop():

    while True :
        sent = raw_input('>> ')
        sent = sent.strip()
        if sent == 'exit':
            break
        elif sent.startswith('lemma ') :
            for word in [lemma(word) for word in sent.split()[1:]] :
                print word
        elif sent.startswith('ner ') :
            sent = sent[4:]
            print ner(sent)
        elif sent.startswith('stem ') :
            for word in [stem(word) for word in sent.split()[1:]] :
                print word
        elif sent.startswith('parse ') :
            #sent = [sent[6:]]
            #answer_question(sent)
            pass
        elif sent.startswith('q ') :
            sent = [sent[2:]]
            answer_question(sent)
        else :
            'Well, ... I dont know what to do !'
    bye_phrase = choice(['Good bye!','auf wiedersehn.','good night','bye bye','it was nice meeting you.','see you soon.','thank you for using knoex.','au revoir'])
    print bye_phrase
    if speech : text_to_speech(bye_phrase)


if __name__ == '__main__':
    qa_loop()




#pattern = load_pattern(some_filename)

