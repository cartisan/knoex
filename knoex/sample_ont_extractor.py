from corpus import CorpusReader
from c_nc import C_NC_TermExtractor
from concept_former import conceptFormer as ConceptFormer
import hearst_patterns as RelationExtractor
from pprint import pprint
import utils

#c = CorpusReader("corpora/snakes.corp")
#text = c.get_corpus()
sentence1 = "The mouse eats the snake."
sentence2 = "Leon kills the mouse."
text = sentence1 + " " + sentence2

term_extractor = C_NC_TermExtractor(text)
terms = term_extractor.compute_cnc()
former = ConceptFormer()
former.form_concepts(terms)

tripel1 = RelationExtractor.find_realation(sentence1)
tripel2 = RelationExtractor.find_realation(sentence2)
tripels = []
tripels += list(tripel1)
tripels += list(tripel2)

former.find_hearst_concepts(tripels)
print "Taxonomy"
pprint(former.get_taxonomy())

concepts, relations = [], []
for concept in list(former.get_taxonomy()):
    concepts.append(" ".join(concept.name))
    relations += concept.make_tripels()

print "Relations"
pprint(tripels)
utils.dot_to_image(utils.taxonomy_to_dot(concepts, relations), 'snake')
#relations = RelationExtractor.find_realation(text)
#print relations
