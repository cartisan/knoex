from nltk.corpus import wordnet as wn
from rdflib import Graph, URIRef
import wikipedia as wiki

def get_wordnet_definition(word):
    synsets = wn.synsets(word)
    return [syn.definition() for syn in synsets]


def get_dbpedia(topics, subject_object) :
    g = Graph()
    for topic in topics :
        g.parse('http://dbpedia.org/resource/' + topic)

    results = g.subject_objects(URIRef('http://dbpedia.org/ontology/' +  subject_object))

    return [str(r[1]) for r in results]


def get_wiki_text(name=None, lang='simple', summary=True, silent=False):
    wiki.set_lang(lang)
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
    return t

if __name__ == '__main__' :
    pass