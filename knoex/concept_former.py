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
		if len(synsets)==1:
			#if only one synset is found it can be returned
			return synsets
		elif len(synsets)>1:
			#if more than one concept is found we still have to
			#think of a clever way to find the best one 
			return synsets[0]
		else:
			print 'No concept found'

	

	def form_concepts(self,terms):
		concepts =[]

		for pair in terms: 
			term = pair
			conc = concept.concept(self.lookUp(term))
			#tag = pair[1]
			concepts.append(conc)
		return concepts	


former = conceptFormer()
sets = former.form_concepts([('dog'),('house'),('fish')])
for concept in sets:
	print concept.synset

print sets[1].get_hypernyms()
print sets[0].get_hyponyms()	