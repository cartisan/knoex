from corpus import CorpusReader
from c_nc import C_NC_TermExtractor
from concept_former import conceptFormer as ConceptFormer
import hearst_patterns as RelationExtractor

c = CorpusReader("knoex/corpora/snakes.corp")
text = c.get_corpus()

term_extractor = C_NC_TermExtractor(text)
terms = term_extractor.compute_cnc()

taxonomy = ConceptFormer().form_concepts(terms)
relations = RelationExtractor.find_realation(text)

print relations
