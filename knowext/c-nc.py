import nltk

# download nltk resources for tokenization
nltk.data.load('tokenizers/punkt/english.pickle')
nltk.data.load('taggers/maxent_treebank_pos_tagger/english.pickle')

# read text and pos-tag it
f = open('corpora/easy', 'r')
text = f.read()
f.close()

tokens = [token for sen in nltk.tokenize.sent_tokenize(text)
          for token in nltk.word_tokenize(sen)]

pos_tags = nltk.pos_tag(tokens)

# pos-tag
# linguistic filter
# c-vaues
# nc-values
