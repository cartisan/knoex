import preprocessor as pp
import corpus
import string
import re


# primitve method : replace by something from NLTK !
def split_into_sentences(text):
	text = text.replace('!','.')
	text = text.replace('?','.')
	text = text.replace(':','.')
	return text.split('.')


text = corpus.CorpusReader().get_corpus((1.3,4.0,2.0))

# create list of sentences
sentences = split_into_sentences(text)
nos = len(sentences) # number of sentences
for i in range(nos) :
	sentences[i] = sentences[i].strip()
	print sentences[i]

if not sentences[-1]:
	del sentences[-1]
	nos-=1

# pos tag each sentence
tagged_sentences = [None]*nos
for i in range(nos):
	tagged_sentences[i] = pp.pos_tag(sentences[i])

print

# print sentences and pos tags
for i in range(nos):
	for j in range(len(tagged_sentences[i])):
		print tagged_sentences[i][j][1] + '\t',
	print
	for j in range(len(tagged_sentences[i])):
		print tagged_sentences[i][j][0] + '\t',
	print
	print
print

# The next part is rather unclean, but it's hopefully gonna work
# Produces a string where every noun phrase is preplaced by NP1,... to NPn
# Then a regex search for hearst patterns is applied to find hyponym relations

# HEARST PATTERNS
hearst_patterns = []
p1 = r'\{TERM\d+\} such as ((\{TERM\d+\},)+(and|or))? \{TERM\d+\}'
p2 = r''

for s in tagged_sentences:

	noun_dict = {}
	word_list=[None]*len(s)
	nn_count = 0
	for i in range(len(s)):
		if s[i][1] in ['NN','JJ','NNS']:
			word_list[i]='{TERM'+str(nn_count)+'}'
			noun_dict[nn_count] = s[i][0]
			nn_count+=1
		else :
			word_list[i]=s[i][0]

	manipulated_s = string.join(word_list)

	print manipulated_s
	print noun_dict
	print
