import os
import string
from time import sleep
from itertools import chain
from random import choice

import nltk
from nltk.parse.stanford import StanfordParser
from nltk.tree import Tree
from numpy import array

import dot_interface
#import tree_patterns
import configurations as conf
from recources import get_wikipedia_text
from tree_patterns import TreePatternMatcher, MatchTree, load_pattern_list
from utils import text_to_speech, lemma, ner, stem, canonicalize, tokenize, ner_tagger


speech = False
silent = True
max_answer_number = 1
speaker = 'google'
whole_sentence = False

def answer_question(sent) :

    parser = StanfordParser(conf.stanford_parser,conf.stanford_models)

    print "parsing sentence ..."
    trees = parser.raw_parse_sents(sent)

    pattern_list, semantic_translations = load_pattern_list()

    for i,tree in enumerate(trees) :
        tree = tree[0] # cut root node

        png_path = 'temp_tree_' + str(i) + '.png'
        if not silent : #not os.path.exists(png_path) :
            print 'saving parse tree as .png ...'
            dot_code = dot_interface.nltk_tree_to_dot(tree)
            dot_interface.dot_to_image(dot_code, 'temp_tree_' + str(i))
            os.popen(conf.image_viewer + ' ' + png_path)

        matcher = TreePatternMatcher()

        match_tree = MatchTree(tree)

        print 'matching patterns ...'
        all_matches = matcher.match_all(match_tree, whole_sentence)
        
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
        for c in answers[0].split(';') :
            if speech : text_to_speech(c,speaker)

        for i,a in enumerate(answers[1:]) :
            if i+1 == max_answer_number :
                break
            sleep(1)
            if speech : text_to_speech('or',speaker)
            print a
            sleep(1)
            for c in a.split(';') :
                if speech : text_to_speech(c,speaker)


def find_answer(topic, filter_words, ner_types):
    print 'get articles from wikipedia'
    articles = get_wikipedia_text(topic,lang='en',summary=False)
    articles += get_wikipedia_text(topic,lang='simple',summary=False)

    # merge to one string
    articles = unicode('\n'.join(articles))

    # filter non ascii
    articles = filter(lambda x: x in string.printable, articles)

    print 'len articles:',len(articles)

    # split in paragraphs
    paragraphs = articles.split('\n')

    print 'tokenize into words'
    paragraphs = [nltk.word_tokenize(p) for p in paragraphs]

    print 'translate abbreviations and slang ...'
    paragraphs = [canonicalize(p) for p in paragraphs]

    print 'check each paragraph if it contains a keyword'
    good_paragraphs = []
    for p in paragraphs :
        for fw in filter_words :
            if fw.lower() in [lp.lower() for lp in p] :
                good_paragraphs += [p]
                break

    print 'len good_paragraphs', len(good_paragraphs)
    good_paragraphs = [item for sublist in good_paragraphs for item in sublist]
    good_sentences = tokenize(" ".join(good_paragraphs))

    print 'perform a named entity recognition'
    tagged_sentences = ner_tagger.tag_sents(good_sentences)

    tagged_text = [item for sublist in tagged_sentences for item in sublist]
    print set(zip(*tagged_text)[1])
    solutions = {}
    for word, tag in tagged_text:
        if tag not in ner_types :
            continue
        if tag in solutions :
            solutions[tag] += [word]
        else :
            solutions[tag] = [word]

    return solutions.items()




def qa_loop():

    global speech
    global silent
    global speaker
    global max_answer_number
    global whole_sentence


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
        elif sent.strip() == 'speech' :
            speech = not speech
            print 'speech toggled', 'on' if speech else 'off'
        elif sent.strip() == 'speaker' :
            speaker = 'google' if speaker=='espeak' else 'espeak'
            print 'speaker toggled to', speaker
        elif sent.strip() == 'silent' :
            silent = not silent
            print 'silent toggled', 'on' if silent else 'off'
        elif sent.startswith('max') :
            try :
                i = int(sent.split()[1])
                max_answer_number = i
                print 'max_answer_number set to', i 
            except :
                print 'wrong max usage!'
        elif sent == 'whole' :
            whole_sentence = not whole_sentence
            print 'whole_sentence toggled', 'on' if whole_sentence else 'off'
        else :
            print 'Well, ... I dont know what to do !'
    bye_phrase = choice(['Good bye!','auf wiedersehn.','good night','bye bye','it was nice meeting you.','see you soon.','thank you for using knoex.','au revoir'])
    print bye_phrase
    if speech : text_to_speech(bye_phrase, speaker)


if __name__ == '__main__':
    qa_loop()
