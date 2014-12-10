from os import popen
from string import punctuation

import nltk
from nltk.parse.stanford import StanfordParser
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag.stanford import NERTagger, POSTagger


import configurations as conf

parser = StanfordParser(conf.stanford_parser,conf.stanford_models)
stanford_postagger = POSTagger(conf.stanford_pos_model, path_to_jar=conf.stanford_postagger, encoding='UTF-8')
ner_tagger = NERTagger(conf.stanford_ner_classifier, conf.stanford_ner)

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


def pos_tag(sent, tagger='stanford'):
    if tagger == 'nltk' :
        tokens = nltk.word_tokenize(sent)
        return nltk.pos_tag(tokens)
    elif tagger == 'stanford' :
        tokens = tokenize(sent)
        return stanford_postagger.tag(tokens)
    else :
        raise ValueError('No such tagger: ' + tagger)


def named_entity_recognition(sent, silent=True) :
    if type(sent) in [str,unicode]:
        sent = nltk.word_tokenize(sent)
    tagged = ner_tagger.tag(sent)
    if not silent :
        print 'ner-tags:',tagged
    return tagged

def normalize(text) :
    tokens = tokenize(text)
    # 3) convert numbers
    # 4) remove none ascii characters
    # 5) text canonicalization
    # 6) remove stop words (to common words)

#def remove_brackets

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


def tokenize(arg):

    if not hasattr(arg, '__iter__') :
        arg = nltk.sent_tokenize(arg)

    list_of_wordlists = [nltk.word_tokenize(sent) for sent in arg]

    return list_of_wordlists


def untokenize(tokens) :
    if tokens and hasattr(tokens[0], '__iter__') :
        return [untokenize(t) for t in tokens]
    return "".join([" "+i if not i.startswith("'") and i not in punctuation else i for i in tokens]).strip()


def canonicalize(words):

    if type(words) in [str, unicode] :
        words = words.strip().split()
        was_string = True
    else :
        was_string = False

    for i,word in enumerate(words) :
        if word in _transform_dict :
            words[i] = _transform_dict[word]
            print word
        elif word in _abbreviations :
            words[i] = _abbreviations[word]
            print word
    #flatten list : [item for sublist in l for item in sublist]
    if was_string :
        return untokenize(words)
    else :
        return words

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

_abbreviations = {
    'U.S.A.' : 'USA'
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

"""def flatten(nested_list):
    for i,item in enumerate(nested_list):
        if hasattr(item, '__iter__') :
            flatten"""