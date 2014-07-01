import utils
import preprocessor as pp
from tree_combinations import numerate_non_terminals

file_name = 'plants'
s = 'Plants are organisms.'

file_name = '/home/momo/Dropbox/parse_trees/' + file_name


"""
tree = pp.parse_sentence(s,'stat')
#numerate_non_terminals(tree)
dot_code = utils.nltk_tree_to_dot(tree)
print dot_code
utils.dot_to_image(dot_code, file_name + '_stat')
print"""

tree = pp.parse_sentence(s,'stanford')
#numerate_non_terminals(tree)
dot_code = utils.nltk_tree_to_dot(tree)
print dot_code
utils.dot_to_image(dot_code, file_name + '_stanford')
print


