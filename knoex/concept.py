from nltk.corpus import wordnet as wn



class concept(object):

	def __init__(self,synset):
		self.synset = synset
		self.hypernyms = synset.hypernyms()
		self.hyponyms = synset.hyponyms()
		self.relations =[]


	def add_relation(self,concept,relation):

				

		

	
