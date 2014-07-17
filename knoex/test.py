import concept_former as cf
import term

former = cf.conceptFormer()

print "Disambiguate 'bank': "

text1 = [term.Term([('River','N')]),term.Term([('run','V')]),term.Term([('bank','N')]),term.Term([('Party','N')])]
text2 = [term.Term([('bank','N')]),term.Term([('city','N')]),term.Term([('stock','N')]),term.Term([('dangerous','ADJ'),('Neighbourhood','N')]),term.Term([('Money','N')])]

onto1 = former.form_concepts(text1)
onto2 = former.form_concepts(text2)
print''
print 'First context: '
for concept1 in onto1:
	print concept1.synset

print''
print 'Second context: '
for concept2 in onto2:
	print concept2.synset	

print''
print 'Example sentence first meaning: '
print onto1[0].synset.examples

print''
print 'Example sentence second meaning: '
print onto2[3].synset.examples
