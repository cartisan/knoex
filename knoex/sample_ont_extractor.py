from corpus import CorpusReader
from c_nc import C_NC_TermExtractor

c = CorpusReader("corpora/snakes.corp")
text = c.get_corpus()

term_extractor = C_NC_TermExtractor(text)
term_extractor.compute_cnc()
terms = term_extractor.multi_word_terms()
