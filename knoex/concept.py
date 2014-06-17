from nltk.corpus import wordnet as wn



class Concept(object):

	def __init__(self,synset=None,name=None,term=None):
		self.synset = synset
		self.name = name
		self.term = term
		if synset:
			self.hypernyms = synset.hypernyms()
			self.hyponyms = synset.hyponyms()
		self.relations =[]


	def add_relation(self,concept,relation):
		self.relations.add((concept,relation))
				
	def get_term(self):
		return self.term

	def get_hypernyms(self):
		return self.hypernyms

	def get_hyponyms(self):
		return self.hyponyms	


		
