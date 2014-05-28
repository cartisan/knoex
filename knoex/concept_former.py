from utils import setup_nltk_resources
from nltk.corpus import wordnet as wn

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
			return false

	

	def form_concepts(self,terms):

		for pair in terms: 
			term = pair[0]
			#tag = pair[1]
			lookUp(term)



print wn.synsets('dog')
