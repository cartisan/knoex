import utils
import preprocessor as pp
from tree_combinations import numerate_non_terminals
import hearst_patterns
file_name = 'LeonHitsKai'
text = 'Leon hits Kai.'

print 'get relations by applying hearst patterns'
relations = hearst_patterns.find_realation(text)
print relations
print
print 'generate dot code'
dot_code = utils.list_of_tripels_to_dot(relations)
print dot_code
print
print 'convert dot code to image'
utils.dot_to_image(dot_code, file_name + '_relations')




