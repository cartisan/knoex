from utils import setup_nltk_resources
from nltk.corpus import wordnet as wn
import concept 

setup_nltk_resources(['wordnet'])

class conceptFormer(object):

	def __init__(self):
		pass	


	def lookUp(self,term,pofs=wn.NOUN):
		# takes a term and a part of speech tag 
		# and looks up the synsets in Wordnet
		# if no pos is specified term is expected to be noun		
		synsets = wn.synsets(term,pos=pofs)
		if len(synsets)>0:
			return synsets
		else:
			print 'No concept found'



	def form_concepts(self,terms):
		sets = []

		for term in terms: 
			sets.append(self.lookUp(term))

		easies = self.get_easies(sets)
		rest = [x for x in sets if not x in easies]
		concepts = self.compare_easies(easies)
		concepts = self.compare_concepts(concepts,rest)

		return concepts	


	def compare_concepts(self,concepts, rest):

		for synsets in rest:
			similarities = []
			for possib in synsets:
				similarity = 0
				for con in concepts:
					similarity = similarity + possib.path_similarity(con)
				similarities.append(similarity)
			concepts.append(synsets[similarities.index(max(similarities))])	

		result = []	
		for conc in concepts:
			c = concept.Concept(conc)
			result.append(c)

		return result	



	def get_easies(self,sets):

		count = self.count_synsets(sets)
		indices = [x for x in count if x <=3]
		easies = []
		for index in indices:
			easies.append(sets[index])
		if not easies:
			easies.append(sets[count.index(min(count))])
		return easies

	def compare_easies(self,easies):


		similarities = []
		for possib in easies:
			tmp = [x for x in easies if x!=possib] #get rest list
			flatten = [item for sublist in tmp for item in sublist] #flatten rest list
 			sim = []
			for synset in possib:
				similarity = 0
				for elem in flatten:	
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
		for synset in easies:
			concepts.append(synset[indices[i]])
			i = i+1


		return concepts	

	def count_synsets(self,sets):
		count = []
		for possib in sets:
			count.append(len(possib))

		return count	


former = conceptFormer()
text1 = ['River','fish','bank','Party']
text2 = ['city','traffic','bank','Sky','teller','money']

onto1 = former.form_concepts(text1)
onto2 = former.form_concepts(text2)

print "First Context"
for concept1 in onto1:
	print concept1.synset

print ""
print "Second Context"
for concept2 in onto2:
	print concept2.synset	

print "First meaning of Bank:"
print onto1[2].synset.examples

print "Second meaning of Bank"
print onto2[4].synset.examples	