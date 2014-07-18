from corpus import CorpusReader
from c_nc import C_NC_TermExtractor
from concept_former import conceptFormer as ConceptFormer
import hearst_patterns as RelationExtractor
from pprint import pprint
import utils

c = CorpusReader("corpora/snakes.corp")
text = c.get_corpus()

term_extractor = C_NC_TermExtractor(text)
terms = term_extractor.compute_cnc()

former = ConceptFormer()
former.form_concepts(terms)
#pprint(former.get_taxonomy())
tripels = [tripel for concept in list(former.get_taxonomy())
           for tripel in concept.make_tripels()]
pprint(tripels)
utils.dot_to_image(utils.list_of_tripels_to_dot(tripels), 'snake')
#relations = RelationExtractor.find_realation(text)
#print relations
