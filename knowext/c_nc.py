import pdb
from math import log
from collections import defaultdict
import operator
import nltk
from preprocessor import pos_tag
from nltk.util import ngrams


MULTI_TERM_PARSER = nltk.RegexpParser('CHUNK: {<N|ADJ>*<N>}')
CONTEXT_TYPES = ["V", "N", "ADJ"]


class C_NC_TermExtractor(object):

    def __init__(self, text):
        self.corpus = text.lower()
        self.pos_tags = pos_tag(text, True)
        self.c_values = []
        self.candidate_cache = []

        # maps from ("token", "pos-tag") to
        # (freq. as context word, no. of ngrams it appears with):
        self.context_words = defaultdict(lambda: [0, 0])
        self.weights = defaultdict(int)

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
        # get all ngrams with maximal c_value
        max_value, max_ngrams = self.c_values[0]
        max_ngrams = [max_ngrams]
        for i in range(1, len(self.c_values)):
            if self.c_values[i][0] < max_value:
                break
            max_ngrams.append(self.c_values[i][1])

        # compute context of max_ngrams
        self.conc_index = nltk.ConcordanceIndex(self.pos_tags)
        for ngram in max_ngrams:
            self.extract_context(ngram)

        no_terms = float(len(max_ngrams))
        for token, counts in self.context_words.items():
            pdb.set_trace() ############################## Breakpoint ##############################
            corpus_count = self.corpus.count(
                self.text_from_tagged_ngram(token))
            self.weights[token] = 0.5 * (counts[1]/no_terms +
                                         counts[0]/corpus_count)
        # nc-values
        pass

    def extract_context(self, ngram):
        """ Takes an ngram and retrieves the context for all
        it's occurrances. The context is a window of size 1.
        Only nouns, verbs and adjectives (CONTEXT_TYPES) are
        kept as context, others are ignored.
        For each context word numer of occurance is computed and
        stored as value in self.context.

        Param:
            ngram: list of tuples of form ("token", "pos-tag")

        Result:
            self.context is filled with "ngram" -> count entries

        TODO: Maybe take context as first CONTEXT_TYPE to the left
              and right, instead of just window of size 1?
        """
        # for each term create a list with it's offsets,
        # find sequences of consequetive offsets in all this lists
        len_ngram = len(ngram)
        list_of_offset_lists = []
        for token in ngram:
            list_of_offset_lists.append(self.conc_index.offsets(token))

        offsets = self.flatten_list(list_of_offset_lists)
        subsequences = self.conseq_sequences(offsets, len_ngram)

        # check that offset-order is same as word order in ngram
        offsets = []
        for seq in subsequences:
            ok = True
            for i in range(len_ngram):
                if not seq[i] in list_of_offset_lists[i]:
                    ok = False
                    break
            if ok:
                offsets.append(seq)

        # find  nouns, verbs and adjectives in context of ngram
        # offset has form [[1,2,3], [5,6] ...], each sub-list
        # holding the offsets of an occurance of ngram.
        # The n-th entry of a sub-list is the
        # offset of the  n-th word of the ngram
        context = []
        for occurrance in offsets:
            if (occurrance[0] - 1 >= 0 and
            occurrance[-1] + 1 <= len(self.pos_tags)):
                pre = self.pos_tags[occurrance[0]-1]
                post = self.pos_tags[occurrance[-1]+1]
                for token in [pre, post]:
                    if token[1] in CONTEXT_TYPES:
                        context.append(token)
                        # increment frequency as context word
                        self.context_words[token][0] += 1

        # increment number of ngrams the context appeared in
        for token in set(context):
            self.context_words[token][1] += 1

    def conseq_sequences(self, li, length):
        """ Takes a list and a length. Returns all sub-sequences in li that
        are successice (e.g. [1,2,3] or [5,6,7,8]) and of the right length.

        E.g.  >>> conseq_sequences([1,6,7,8,9,8,9]], length=3)
              [[6,7,8], [7,8,9]]
        """
        return [li[n:n+length]
                for n in range(len(li)-length+1)
                if li[n:n+length] == range(li[n], li[n]+length)]

    def flatten_list(self, l):
        """ Takes a list of lists and returns the flattened version"""

        return reduce(operator.add, l)

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
        if type(ngram) == tuple:
            return ngram[0]
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

        self.c_values.append((c_value, ngram))


f = open('corpora/easy', 'r')
#f = open('corpora/snakes', 'r')
text = f.read()
f.close()
extractor = C_NC_TermExtractor(text)
extractor.compute_cnc()
import pprint
pprint.pprint(extractor.__dict__)
