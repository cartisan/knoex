from nltk.tag.stanford import NERTagger
import configurations as conf
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer


def named_entity_recognition(sent) :
    st = NERTagger(conf.stanford_ner_classifier, conf.stanford_ner)
    return st.tag(sent.split())


def lemmatize(word):
	lmtzr = WordNetLemmatizer()
	return lmtzr.lemmatize(word)


def stem(word) :
	stemmer = PorterStemmer()
	return stemmer.stem(word)


ner = named_entity_recognition
lemma = lemmatize