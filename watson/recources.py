from nltk.corpus import wordnet as wn
from rdflib import Graph, URIRef
import wikipedia as wiki
import httplib


def get_wordnet_definition(word):
    synsets = wn.synsets(word)
    return [syn.definition() for syn in synsets]


def get_dbpedia(topics, subject_object) :
    g = Graph()
    for topic in topics :
        g.parse('http://dbpedia.org/resource/' + topic)

    results = g.subject_objects(URIRef('http://dbpedia.org/ontology/' +  subject_object))

    return [str(r[1]) for r in results]


def dbpedia_wrapper(topics, subject_object):
    #print 'called dbpedia with', topics, subject_object
    if type(topics) not in [list,tuple] :
        topics = [topics]
    results = get_dbpedia(topics, subject_object)
    #print 'results', results
    return ['The ' + subject_object + ' of ' + ', '.join(topics).replace('_',' ') + ' is ' + r for r in results]


def get_wikipedia_text(keywords=None, lang='simple', summary=True, silent=False):
    wiki.set_lang(lang)
    if type(keywords) in [str,unicode]:
        keywords = [keywords]
    articles = []
    for name in keywords :
        try :
            if not name :
                name = wiki.random()
                if not silent :
                    print name
            if summary :
                t = wiki.summary(name)
            else :
                t = wiki.page(name).content
        except Exception, e:
            t = ''
            if not silent :
                print e
        articles += [t]
    return articles
