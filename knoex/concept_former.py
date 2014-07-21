from utils import setup_nltk_resources
from nltk.corpus import wordnet as wn
import concept
from term import Term
import preprocessor
import itertools

setup_nltk_resources(['wordnet'])


class conceptFormer(object):
    def __init__(self):
        self.multi_concepts = set([])
        self.single_concepts = set([])

    def get_taxonomy(self):
        if self.multi_concepts and self.single_concepts:
            return self.multi_concepts.union(self.single_concepts)
        if self.multi_concepts:
            return self.multi_concepts
        if self.single_concepts:
            return self.single_concepts
        return set([])

    def lookUp(self, term, pos):
        # takes a term and a part of speech tag
        # and looks up the synsets in Wordnet

        pos = self.pos_tag(pos)

        synsets = wn.synsets(term, pos=pos)
        if len(synsets) > 0:
            return (synsets, term)
        else:
            print\
                'Concept Former: No concept found for "{}"'.format(term)


    def form_concepts(self, terms):
        """
        Takes a list of term objects and returns
        a list of concepts after applying disambiguation via
        comparing possible candidates.
        """
        nouns = [t for t in terms if t.get_head()[1]=='N']
        #verbs = [t for t in terms if t.get_head()[1]=='V']
        #adjectives = [t for t in terms if t.get_head()[1]=='ADJ']

        #concepts = []
        #if nouns:
        #   concepts += 
        self.form(nouns)
        #if verbs:
        #    concepts += self.form(verbs)
        #if adjectives:
        #    concepts += self.form(adjectives)

        #return set(concepts)

    def form(self, terms):
        #actual formation
        sets = []
        multiwords = []

        #look for multiword terms, for concepts of them and then go on with the disambiguation only
        #with the head-term
        for term in terms:
            if len(term.get_terms()) > 1:
                multiwords.append(concept.Concept(name=term.get_terms(), term=term.get_head()[0]))
            synsets = self.lookUp(term.get_head()[0], term.get_head()[1])
            if synsets:
                sets.append(synsets)

        if sets:
            easies = self.get_easies(sets)
            rest = [x for x in sets if not x in easies]
            concepts = self.compare_easies(easies)
            concepts = self.compare_concepts(concepts, rest)

            for (mult, con) in itertools.product(multiwords, concepts):
                    if str(con.get_term()) == str(mult.get_term()):
                        mult.add_hypernym(con)
                        con.add_hyponym(mult)

            self.single_concepts = set(concepts)
        self.multi_concepts = set(multiwords)

    def compare_concepts(self, concepts, rest):
        #Compares already found concepts to possible synsts for each term
        #in order to find most probable one
        conNoTerm = [x[0] for x in concepts]
        restNoTerm = [y[0] for y in rest]

        for synsets in restNoTerm:
            similarities = []
            for possib in synsets:
                similarity = 0
                for con in conNoTerm:
                    similarity = similarity + possib.path_similarity(con)
                similarities.append(similarity)
            concepts.append((synsets[similarities.index(max(similarities))],rest[restNoTerm.index(synsets)][1]))

        result = []
        for conc in concepts:
            c = concept.Concept(synset=conc[0], term=conc[1], name=conc[1])
            result.append(c)

        return result

    def get_easies(self, sets):
        #Finds the Concepts with the fewest possible interpretations
        #Tries to find those with less than 3, if not takes just the one with 
        #the smallest list

        synsets = [x[0] for x in sets]
        counts = self.count_synsets(synsets)
        indices = [index for index, count in
                   enumerate(counts) if count <= 3]

        easies = []
        for index in indices:
            easies.append(sets[index])
        if not easies:
            easies.append(sets[counts.index(min(counts))])
        return easies

    def count_synsets(self, sets):
        #count numbers of possible synsets for a list of terms
        #returns list of counts

        count = []
        for possib in sets:
            count.append(len(possib))

        return count

    def compare_easies(self,easies):
        #Takes a list of ([synsets],pos-tag) tuples for 'easy' terms
        #and computes the similarites between all possible interpretations of a term
        #returns list of (synset,pos-tag) tuples with the highes similarity

        easysets = [x[0] for x in easies]
        similarities = []
        for possib in easysets: #get one list of possible synsets
            tmp = [x for x in easysets if x!=possib] #get rest list
            flatten = [item for sublist in tmp for item in sublist] #flatten rest list
            sim = []
            for synset in possib: #get one possible synset
                similarity = 0
                for elem in flatten:    #compare it to all other synsets
                    similarity = similarity + synset.path_similarity(elem)
                sim.append(similarity)
            similarities.append(sim)
        
        indices = []
        for (measure,i) in [(measure,i) for measure in similarities for i in range(len(measure))]:
            if measure[i] == max(measure):
                    indices.append(i)

        concepts = []
        i = 0
        #append found concepts + respective terms
        for synset in easysets:
            concepts.append((synset[indices[i]], easies[i][1]))
            i = i+1

        return concepts

    def find_hearst_concepts(self, triples):
        s_concepts = []
        m_concepts = []
        for (t1, rel, t2) in triples:
            term1 = Term(preprocessor.pos_tag(t1, True))
            term2 = Term(preprocessor.pos_tag(t2, True))

            synsets1 = wn.synsets(term1.get_head()[0], self.pos_tag(term1.get_head()[1]))
            synsets2 = wn.synsets(term2.get_head()[0], self.pos_tag(term2.get_head()[1]))
            (best1, best2) = self.comp(synsets1, synsets2)

            con1 = concept.Concept(synset=best1, term=term1.get_head()[0])
            con2 = concept.Concept(synset=best2, term=term2.get_head()[0])

            conChild1 = None
            conChild2 = None
            if len(term1.get_terms()) > 1:
                conChild1 = concept.Concept(name=term1.get_terms(), term=term1.get_head()[0])
                con1.add_hyponym(conChild1)
                conChild1.add_hypernym(con1)
                #m_concepts.append(conChild1)
            if len(term2.get_terms()) > 1:
                conChild2 = concept.Concept(name=term2.get_terms(), term=term2.get_head()[0])
                con2.add_hyponym(conChild2)
                conChild2.add_hypernym(con2)
                #m_concepts.append(conChild2)

            if conChild1:
                if conChild2:
                    conChild1.add_relation(conChild2, rel)
                else:
                    conChild1.add_relation(con2, rel)
                m_concepts.append(conChild1)
            else:
                if conChild2:
                    con1.add_relation(conChild2, rel)
                    m_concepts.append(conChild2)
                else:
                    con1.add_relation(con2, rel)

            s_concepts.append(con1)
            s_concepts.append(con2)

        self.single_concepts = self.single_concepts.union(set(s_concepts))
        self.multi_concepts = self.multi_concepts.union(set(m_concepts))

    def comp(self, synsets1, synsets2):
        similarity = 0
        for (try1,try2) in [(try1,try2) for try1 in synsets1 for try2 in synsets2]:
            newsimilarity = try1.path_similarity(try2)
            if newsimilarity > similarity:
                similarity = newsimilarity
                best1 = try1
                best2 = try2

        return (best1, best2)

    def pos_tag(self, pos):
        if pos == 'N':
            pos = wn.NOUN
        elif pos == 'V':
            pos = wn.VERB
        elif pos == 'ADJ':
            pos = wn.ADJ
        else:
            print 'No regular Part of speech'

        return pos
