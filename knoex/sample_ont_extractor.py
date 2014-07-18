from corpus import CorpusReader
from c_nc import C_NC_TermExtractor
from concept_former import conceptFormer as ConceptFormer
import hearst_patterns as RelationExtractor
from term import Term

c = CorpusReader("knoex/corpora/snakes.corp")
text = c.get_corpus()

#term_extractor = C_NC_TermExtractor(text)
#terms = term_extractor.compute_cnc()

#terms = [#Term([("snake", "N")]),
         #Term([("snake", "N")]),
terms = [Term([("cake", "N")]),
         Term([("green", "ADJ"), ("snake", "N")])]
taxonomy = ConceptFormer().form_concepts(terms)
print taxonomy

#relations = RelationExtractor.find_realation(text)
#print relations
