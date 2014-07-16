from nltk import download
from utils import setup_nltk_resources
from nltk import word_tokenize, Tree
from nltk import pos_tag as nltk_pos_tag
from nltk.tag.simplify import simplify_wsj_tag
from nltk.tokenize import sent_tokenize
from stat_parser import parser as s_parser
import ctypes
import os
from os.path import expanduser


def pos_tag(text, simple=False):
    """ Tokenizes a given text and determines the pos-tags. Lowercases
        the text.

     Params:
        text: string to be tokenized
        simple: boolean indicating weather to simplify the pos tags

    Returns:
        list of tuples of form (token, pos-tag)
    """

    # tokenize to sentences, then to tokens
    try:
        tokens = [token.lower() for sen in sent_tokenize(text)
                  for token in word_tokenize(sen)]
    except LookupError:
        download("punkt")
        tokens = [token.lower() for sen in sent_tokenize(text)
                  for token in word_tokenize(sen)]

    # generate pos-tags
    try:
        pos = nltk_pos_tag(tokens)
    except LookupError:
        download('maxent_treebank_pos_tagger')
        pos = nltk_pos_tag(tokens)

    # simplify tags if requested
    if simple:
        simple_pos = []
        for word, tag in pos:
            new_tag = simplify_wsj_tag(tag)
            # simplification removes some tags
            # not allowed to use empty tag so use initial one
            if not new_tag:
                new_tag = tag
            simple_pos.append((word, new_tag))
        pos = simple_pos

    return pos


def parse_sentence(sentence, parser='stanford', path_to_parser=None):

    abs_path = os.path.abspath(__file__)
    module_path = os.path.dirname(abs_path)
    
    print 'module_path', module_path

    # get the current process_id to run parser in multiple processes
    tid = ctypes.CDLL('libc.so.6').syscall(186)

    if parser == 'stanford':

        if path_to_parser == None :
            path_to_parser = module_path + '/stanford_parser'
        elif path_to_parser[-1] == '/' :
            path_to_parser = path_to_parser[:-1]

        # saves the sentence in a temporary file
        tmp_file = '~/stanfordtemp_' + str(tid)
        os.popen("echo '" + sentence + "' > " + tmp_file)

        # calles the stanford parser and outputs string representation of parse tree
        parser_out = os.popen(path_to_parser + "/lexparser.sh " + tmp_file).readlines()
        home = expanduser("~")
        os.remove(home + tmp_file[1:])

        print parser_out

        # transform the stanford parse tree representation into nltk parse tree representation
        parse_trees_text=[]
        tree = ""
        for line in parser_out:
            if line.isspace():
                parse_trees_text.append(tree)
                tree = ""
            elif "(. ...))" in line:
                #print "YES"
                tree = tree + ')'
                parse_trees_text.append(tree)
                tree = ""
            else:
                tree = tree + line

        # neglect parse_trees_text[1] at this point
        print 'tree', tree
        parse_tree = Tree(parse_trees_text[0])
        print
        print 'PT0', parse_trees_text[0]
        print
        print 'PT1', parse_trees_text[1]


    elif parser == 'berkeley' :
        
        if path_to_parser == None :
            path_to_parser = module_path + '/berkeley_parser/'
        elif path_to_parser[-1] != '/' :
            path_to_parser += '/'

        grammar = path_to_parser + 'eng_sm6.gr'
        path_to_parser += 'BerkeleyParser.jar'


        # saves the sentence in a temporary file
        tmp_file = '~/berkeleytemp_' + str(tid)
        os.popen("echo '" + sentence + "' > " + tmp_file)

        # calles the berkeley parser and outputs string representation of parse tree

        parser_out = os.popen('java -jar ' + path_to_parser + ' -gr ' + grammar + ' -inputFile ' + tmp_file).readlines()
        home = expanduser("~")
        os.remove(home + tmp_file[1:])

        parse_tree = Tree(parser_out[0])

    elif parser in ['s_parser','stat','stat_parser']:
        sp = s_parser.Parser()
        parse_tree = sp.parse(sentence)

    else :
        print 'No such parser:', parser
        parse_tree = None

    return parse_tree   
