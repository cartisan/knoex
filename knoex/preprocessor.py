import re
import os
import sys
import ctypes
from nltk import Tree
from nltk.tag.simplify import simplify_wsj_tag
from stat_parser import parser as s_parser
from os.path import expanduser
from random import randint
from subprocess import Popen, STDOUT, PIPE
from textblob import TextBlob


def pos_tag(text, simple=False):
    """ Tokenizes a given text and determines the pos-tags. Lowercases
        the text.

     Params:
        text: string to be tokenized
        simple: boolean indicating weather to simplify the pos tags

    Returns:
        list of tuples of form (token, pos-tag)
    """

    blob = TextBlob(text.lower())
    pos = blob.tags

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

    #print 'module_path', module_path

    # get the current process_id to run parser in multiple processes
    try :
        tid = ctypes.CDLL('libc.so.6').syscall(186)
    except :
        tid = randint(0,1000000)

    if parser == 'stanford':

        if path_to_parser == None :
            if sys.platform == 'win32':
                path_to_parser = module_path + '\stanford_parser'
            else:
                path_to_parser = module_path + '/stanford_parser'
        elif path_to_parser[-1] == '/':
            path_to_parser = path_to_parser[:-1]

        # saves the sentence in a temporary file
        #tmp_file = '~/stanfordtemp_' + str(tid)
        if sys.platform == 'win32':
            tmp_file = module_path + '\\stanfordtemp_' + str(tid)
        else:
            tmp_file = module_path + '/stanfordtemp_' + str(tid)   
        f = open(tmp_file, 'w')
        f.write(sentence)
        f.close()
        #os.popen("echo '" + sentence + "' > " + tmp_file)

        # calles the stanford parser and outputs string representation of parse tree
        if sys.platform == 'win32':
            cmd = path_to_parser + "\lexparser.bat " + tmp_file
            sub = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=path_to_parser)
            parser_out = sub.stdout.read()

        else:
            cmd = path_to_parser + "/lexparser.sh " + tmp_file
            parser_out = "\n".join(os.popen(cmd).readlines())

        os.remove(tmp_file)

        # transform the stanford parse tree representation into nltk parse tree representation
#        if sys.platform == 'win32':
        regex = re.compile("\(ROOT.*\)\)", re.DOTALL)
        parse_trees_text = regex.findall(parser_out)
        parse_trees_text.append("We doesn't extract second tree yet")

        # neglect parse_trees_text[1] at this point
        #print 'tree', tree
        parse_tree = Tree(parse_trees_text[0])
        print
        print 'PT0', parse_trees_text[0]
    
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
