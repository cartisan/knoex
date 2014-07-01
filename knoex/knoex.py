import corpus
import hearst_patterns as hp
import utils

file_name = 'simple'

text = corpus.CorpusReader().get_corpus()
relations = hp.find_realation(text)

print
for r in relations :
    print r

if utils.which('dot') :
    dot_code = utils.list_of_tripels_to_dot(relations)
    utils.dot_to_image(dot_code, file_name + '_relations')