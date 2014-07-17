import utils
import preprocessor as pp
from tree_combinations import numerate_non_terminals

file_name = 'LeonHitsKai'
s = "Leon hits Kai."

file_name = '/home/momo/Dropbox/parse_trees/' + file_name
#file_name = "./"+file_name

"""
try:
    tree = pp.parse_sentence(s,'stat')
    #numerate_non_terminals(tree)
    dot_code = utils.nltk_tree_to_dot(tree)
    print dot_code
    utils.dot_to_image(dot_code, file_name + '_stat')
    print
except :
    print 'cannot parse with stat'
"""


try :
    tree = pp.parse_sentence(s,'stanford')
    #numerate_non_terminals(tree)
    dot_code = utils.nltk_tree_to_dot(tree)
    utils.dot_to_image(dot_code, file_name + '_stanford')
    print "stanford done"
except :
    print 'cannot parse with stanford'


"""
try :
    tree = pp.parse_sentence(s,'berkeley')
    #numerate_non_terminals(tree)
    dot_code = utils.nltk_tree_to_dot(tree)
    utils.dot_to_image(dot_code, file_name + '_berkeley')
    print "berkeley done"
except :
    print 'cannot parse with berkeley'
"""
