import re
import string
import wikipedia as wiki


class CorpusReader(dict) :
    """ class to access text of the .corp data files, accessible like a dict"""

    def __init__(self,path='corpora/simple.corp'):
        data = open(path).read() + "\n"
        d = self.__get_dict(data)
        super(CorpusReader, self).__init__(d)
        self.__dict__=self

    def __get_dict(self,data):
        data = re.sub( r'#.*?\n' ,"" ,data) #remove comments
        matches = re.findall(r'\$(\d+\.\d+)([^\$]*)',data) # constructs a list of tuples of text between $-symboles and its corresponding number 
        matches = dict(matches)
        matches = { float(k):v.strip() for k, v in matches.iteritems()}
        return matches

    def get_corpus(self,paragraphs='*'):
        if paragraphs == '*':
            paragraphs = self.keys()
        elif type(paragraphs) in [float,int]:
            paragraphs = [paragraphs]
        
        l = [self[x] for x in paragraphs if self[x]!=''] # <<< exception handling ?
        l = string.join(l,'\n')
        return l


# get text from any wikipedia article (default: summary of random simple english wikipedia article)
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


if __name__=='__main__':
    cr = CorpusReader()
    print cr.get_corpus((1.0,2.0,2.1))
