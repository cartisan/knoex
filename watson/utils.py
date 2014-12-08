from os import popen
from string import punctuation

import nltk
from nltk.parse.stanford import StanfordParser
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag.stanford import NERTagger


import configurations as conf

parser = StanfordParser(conf.stanford_parser,conf.stanford_models)

def parse(text, normalize=True) :
    """Parses string, iterable of strings or nested iterables of strings"""
    if hasattr(text, '__iter__') :
        return [parse(t) for t in text]
    else :
        if normalize : text = resolve_abb(text)
        trees = parser.raw_parse(text)
    return trees

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

def tokenize(arg, prune=True):
    if not hasattr(arg, '__iter__') :
        arg = nltk.sent_tokenize(arg)
    list_of_wordlists = [nltk.word_tokenize(sent) for sent in arg]
    if prune and len(list_of_wordlists) == 1:
        list_of_wordlists = list_of_wordlists[0]
    return list_of_wordlists

def untokenize(tokens) :
    if tokens and hasattr(tokens[0], '__iter__') :
        return [untokenize(t) for t in tokens]
    return "".join([" "+i if not i.startswith("'") and i not in punctuation else i for i in tokens]).strip()

def resolve_abb(text):

    words = text.strip().split()

    for i,word in enumerate(words) :
        if word in _transform_dict :
            words[i] = _transform_dict[word]
    #flatten list : [item for sublist in l for item in sublist]
    return untokenize(words)

_transform_dict = {
    
    "I'm" : "I am",
    "he's" : "he is",
    "He's" : "He is",
    "she's" : "she is",
    "She's" : "She is",
    "it's" : "it is",
    "It's" : "It is",
    "that's" : "that is",
    "That's" : "That is",
    "there's" : "there is",
    "There's" : "There is",
    "What's" : "what is",
    "what's" : "what is",
    "Whats" : "What is",
    "whats" : "what is",
    "Where's" : "where is",
    "where's" : "where is",
    "I'll" : "I will",
    "Ill" : "I will",
    "you'll" : "you will",
    "You'll" : "You will", 
    "they're" : "they are",
    "They're" : "they are",
    "you're" : "you are",
    "You're" : "you are",
    "we're" : "we are",
    "We're" : "we are",
    "has't" : "has not",
    "doesn't" : "does not",
    "won't" : "will not",
    "was't" : "was not",
    "is't" : "is not",
    "don't" : "do not",
    "can't" : "can not",
    "cannot" : "can not",
    "could't" : "could not",
    "would't" : "would not",
    "wanna" : "want to",
    "gonna" : "going to"

}


# needs some improvement
def transform_arithmetics(expr):
    
    def is_number(num) :
        try :
            float(num)
            return True
        except :
            return False

    tokens = tokenize(expr)
    for i,token in enumerate(tokens) :
        if token in _arithmetic_dict :
            tokens[i] = _arithmetic_dict[token]
        elif is_number(token) :
            tokens[i] = token
        else :
            return False
    return " ".join(tokens)

_arithmetic_dict = {
    'zero' : '0',
    'one' : '1',
    'two' : '2',
    'three' : '3',
    'four' : '4',
    'five' : '5',
    'six' : '6',
    'seven' : '7',
    'eight' : '8',
    'nine' : '9',
    'ten' : '10',
    'eleven' : '11',
    'twelve' : '12',
    'and' : '+',
    'minus' : '-',
    'plus' : '+',
    'times' : '*',
    '**' : '**',
    '-' : '-',
    '+' : '+',
    '*' : '*',
    '^' : '**',
    '/' : '/' 
}

ner = named_entity_recognition
lemma = lemmatize