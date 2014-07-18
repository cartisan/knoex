import concept_former as cf
import term
import hearst_patterns as hp 

former = cf.conceptFormer()

text = 'The monkey bites the snake.'
pattern = hp.find_realation(text)

result = former.find_hearst_concepts(pattern)
print result

for concept in list(result):
	print str(concept) + ' ' + str(concept.get_relations())