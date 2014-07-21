from corpus import CorpusReader
from c_nc import C_NC_TermExtractor
from concept_former import conceptFormer as ConceptFormer
import hearst_patterns as RelationExtractor
from pprint import pprint
import utils

#c = CorpusReader("corpora/snakes.corp")
#text = c.get_corpus()
sentence1 = "The mouse eat the snake."
sentence2 = "Leon kills the mouse."
text = sentence1 + " " + sentence2

term_extractor = C_NC_TermExtractor(text)
terms = term_extractor.compute_cnc()

tripel1 = RelationExtractor.find_realation(sentence1)
tripel2 = RelationExtractor.find_realation(sentence2)
former = ConceptFormer()
former.form_concepts(terms)

tripels = []
tripels += list(tripel1)
tripels += list(tripel2)

former.find_hearst_concepts(tripels)
print "Taxonomy"
pprint(former.get_taxonomy())
print "\Taxonomy"

tripels = [tripel for concept in list(former.get_taxonomy())
           for tripel in concept.make_tripels()]

print "Concepts"
pprint(tripels)
utils.dot_to_image(utils.list_of_tripels_to_dot(tripels), 'snake')
#relations = RelationExtractor.find_realation(text)
#print relations
