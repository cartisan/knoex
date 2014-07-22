from corpus import CorpusReader
from c_nc import C_NC_TermExtractor
from concept_former import conceptFormer as ConceptFormer
import hearst_patterns as RelationExtractor
from pprint import pprint
import utils


def small_text():
    sentence1 = "The poisonous green snake lies on the ground."
    sentence2 = "An elephant killes the snake."
    text = sentence1 + " " + sentence2

    term_extractor = C_NC_TermExtractor(text)
    terms = term_extractor.compute_cnc()
    former = ConceptFormer()
    former.form_concepts(terms)

    tripels = list(RelationExtractor.find_realation(text))
    former.find_hearst_concepts(tripels)

    print "Taxonomy: "
    pprint(former.get_taxonomy())

    concepts, relations = [], []
    for concept in list(former.get_taxonomy()):
        concepts.append(" ".join(concept.name))
        relations += concept.make_tripels()

    print "no con.: " + str(len(concepts))
    print "no rel.: " + str(len(relations))

    utils.dot_to_image(utils.taxonomy_to_dot(concepts, relations), 'snake')


def long_text():
    c = CorpusReader("corpora/snakes.corp")
    text = c.get_corpus()

    term_extractor = C_NC_TermExtractor(text)
    terms = term_extractor.compute_cnc()

    former = ConceptFormer()
    former.form_concepts(terms)

    print "Taxonomy: "
    pprint(former.get_taxonomy())

    concepts, relations = [], []
    for concept in list(former.get_taxonomy()):
        concepts.append(" ".join(concept.name))
        relations += concept.make_tripels()

    print "no con.: " + str(len(concepts))
    print "no rel.: " + str(len(relations))

    utils.dot_to_image(utils.taxonomy_to_dot(concepts, relations), 'snake')
