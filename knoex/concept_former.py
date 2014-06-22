from utils import setup_nltk_resources
from nltk.corpus import wordnet as wn
import concept 
import term

setup_nltk_resources(['wordnet'])

class conceptFormer(object):
	
	def __init__(self):
		pass	
	

	def lookUp(self,term,pos):
		# takes a term and a part of speech tag 
		# and looks up the synsets in Wordnet

		if pos=='N':
			pos = wn.NOUN
		elif pos =='V':
			pos = wn.VERB
		elif pos =='ADJ':
			pos = wn.ADJ
		else:
			print 'No regular Part of speech'		

		synsets = wn.synsets(term,pos=pos)
		if len(synsets)>0:
			return (synsets,term)
		else:
			print 'No concept found'

	def form_concepts(self,terms):
		"""
		Takes a list of term objects and returns 
		a list of concepts after applying disambiguation via 
		comparing possible candidates.
		"""
		nouns = [t for t in terms if t.get_head()[1]=='N']
		verbs = [t for t in terms if t.get_head()[1]=='V']
		adjectives = [t for t in terms if t.get_head()[1]=='ADJ']

		concepts = []
		if nouns:
			concepts.append(self.form(nouns))
		if verbs:
			concepts.append(self.form(verbs))
		if adjectives:
			concepts.append(self.form(adjectives))

		concepts = [item for sublist in concepts for item in sublist]	
		return concepts			

	def form(self,terms):
		#actual formation 

		sets = []
		multiwords = []

		#look for multiword terms, for concepts of them and then go on with the disambiguation only
		#with the head-term
		for term in terms: 
			if len(term.get_terms()) > 1:
				multiwords.append(concept.Concept(name=term.get_terms(),term=term.get_head()[0]))
			sets.append(self.lookUp(term.get_head()[0],term.get_head()[1]))
		
		easies = self.get_easies(sets)
		rest = [x for x in sets if not x in easies]
		concepts = self.compare_easies(easies)
		concepts = self.compare_concepts(concepts,rest)

		for mult in multiwords:
			for con in concepts:
				if str(con.get_term()) == str(mult.get_term()):
					mult.add_relation(con,'hypernym')
					con.add_relation(mult,'hyponym')

		return concepts	

	def compare_concepts(self,concepts,rest):
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
			concepts.append((synsets[similarities.index(max(similarities))],rest[restNoTerm.index(synsets)][0]))

		result = []	
		for conc in concepts:
			c = concept.Concept(synset=conc[0],term=conc[1])
			result.append(c)

		return result	

	def get_easies(self,sets):
		#Finds the Concepts with the fewest possible interpretations
		#Tries to find those with less than 3, if not takes just the one with 
		#the smallest list

		synsets = [x[0] for x in sets] 
		count = self.count_synsets(synsets)
		indices = [x for x in count if x <=3]
		easies = []
		for index in indices:
			easies.append(sets[index])
		if not easies:
			easies.append(sets[count.index(min(count))])
		return easies
			
	def count_synsets(self,sets):	
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
				for elem in flatten:	#compare it to all other synsets
					similarity = similarity + synset.path_similarity(elem)
				sim.append(similarity)
			similarities.append(sim)
		
		indices = []
		for measure in similarities:
			for i in range(len(measure)):
				if measure[i] == max(measure):
					indices.append(i)

		concepts = []
		i = 0
		#append found concepts + respective terms
		for synset in easysets:
			concepts.append((synset[indices[i]],easies[i][1]))
			i = i+1

		return concepts	

