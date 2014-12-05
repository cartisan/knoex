from os import popen

import nltk
from nltk.tag.stanford import NERTagger
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

import configurations as conf


def text_to_speech(text, engine='google'):
    if engine == 'google' :

        text = text.replace('(',' ')
        text = text.replace(')',' ')
        text = text.replace('`','')
        text = text.replace("'",'')
        text = text.replace("-",' ')
        popen('./speech.sh ' + text)
    elif engine == 'espeak' :
        popen('espeak ' + '"' + text + '"')
    else :
        print 'No such tos engine:', engine
        print text 


def pos_tag(sent):
    tokens = nltk.word_tokenize(sent)
    return nltk.pos_tag(tokens)


def named_entity_recognition(sent) :
    st = NERTagger(conf.stanford_ner_classifier, conf.stanford_ner)
    return st.tag(sent.split())


def lemmatize(word):
    #if type(word) in [str,unicode] :
    #    word = word.split()
    lmtzr = WordNetLemmatizer()
    #return [lmtzr.lemmatize(w) for w in word]
    return lmtzr.lemmatize(word)


def stem(word) :
    if type(word) in [str,unicode] :
        word = word.split()
    stemmer = PorterStemmer()
    return [stemmer.stem(w) for w in word]


ner = named_entity_recognition
lemma = lemmatize

