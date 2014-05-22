from math import log
import nltk
from preprocessor import pos_tag
from nltk.util import ngrams


MULTI_TERM_PARSER = nltk.RegexpParser('CHUNK: {<N|ADJ>*<N>}')


class C_NC_TermExtractor(object):

    def __init__(self, text):
        self.corpus = text.lower()
        self.pos_tags = pos_tag(text, True)
        self.c_values = []
        self.candidate_cache = []

    def compute_cnc(self):
        # linguistic filter
        # find all n-grams of the form (Noun|Adjective)*(Noun)
        # (according to Frantzi_97)
        candidates = self.find_multi_word_terms()
        self.candidate_cache = [self.text_from_tagged_ngram(candidate) for
                                candidate in candidates]

        # compute c_value for each candidate
        max_len = max([len(ngram) for ngram in candidates])
        for ngram in candidates:
            self._compute_c_value(ngram, max_len)

        self.c_values.sort(key=lambda x: x[0], reverse=True)

        # compute weight
        max_value, max_ngrams = self.c_values[0]
        max_ngrams = [max_ngrams]
        for i in range(1, len(self.c_values)):
            if self.c_values[i][0] < max_value:
                break
            max_ngrams.append(self.c_values[i][1])

        # TODO: compute context of max_ngrams

        # nc-values
        pass

    def find_multi_word_terms(self):
        def _candidate_words(pos_tags):
            tree = MULTI_TERM_PARSER.parse(pos_tags)
            return [subtree.leaves() for subtree in tree.subtrees()
                    if subtree.node == "CHUNK"]

        # find all maximal multi word terms
        candidates = _candidate_words(self.pos_tags)

        # check weather candidates contain sub words
        sub_words = []
        for mult_word in candidates:
            # create all ngrams with size n-1..1
            for n in range(len(mult_word)-1, 0, -1):
                # extract candidates from each ngram
                for ngram in ngrams(mult_word, n):
                    sub_words += _candidate_words(list(ngram))

        return candidates+sub_words

    def text_from_tagged_ngram(self, ngram):
        """ Returns the text of an pos-tagged ngram.

        Param:
            ngram: list of tuples of form (word, pos-tag)
        Return:
            a string containing all words from the ngram seperated by spaces
        """

        # zip(*ngram)[0] returns a tuple with words from a (word,tag) list
        return " ".join(zip(*ngram)[0])

    def _compute_c_value(self, ngram, max_n):
        ngram_text = self.text_from_tagged_ngram(ngram)
        len_ngram = len(ngram)
        c_value = log(len_ngram, 2) * self.corpus.count(ngram_text)

        containing_ngrams = [candidate for candidate in self.candidate_cache
                             if ngram_text in candidate
                             and not ngram_text == candidate]
        if containing_ngrams:
            dependency_score = 0
            # find all candidates that contain the current one
            for container in containing_ngrams:
                dependency_score += self.corpus.count(container)

            c_value = c_value - float(1)/len(containing_ngrams)*dependency_score

        self.c_values.append((c_value, ngram_text))


f = open('corpora/easy', 'r')
#f = open('corpora/snakes', 'r')
text = f.read()
f.close()
extractor = C_NC_TermExtractor(text)
extractor.compute_cnc()
import pprint
pprint.pprint(extractor.c_values)
