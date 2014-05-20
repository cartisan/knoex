import re
import string
import wikipedia as wiki


class CorpusReader(dict) :
    """ class to access text of the .corp data files, accessible like a dict"""

    def __init__(self,path='corpora/simple.corp'):
        data = open(path).read() + "\n"
        d = self.get_dict(data)
        super(CorpusReader, self).__init__(d)
        self.__dict__=self

    def get_dict(self,data):
        data = re.sub( r'#.*?\n' ,"" ,data) #remove comments
        matches = re.findall(r'\$(\d+\.\d+)([^\$]*)',data) # constructs a list of tuples of text between $-symboles and its corresponding number 
        matches = dict(matches)
        matches = { float(k):v.strip() for k, v in matches.iteritems()}
        return matches

    def get_corpus(self,paragraphs='*'):
        if paragraphs == '*':
            paragraphs = self.keys()
        l = [self[x] for x in paragraphs if self[x]!='']
        l = string.join(l,'\n')
        return l


# get text from any wikipedia article (default: summary of random simple english wikipedia article)
def get_wiki_text(name=None, lang='simple', summary=True, silent=False):
    try :
        wiki.set_lang(lang)
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


if __name__=='__main__':
    cr = CorpusReader()
    print cr.get_corpus((1.0,2.0,2.1))
