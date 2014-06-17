class Term(object):

    def __init__(self, ngram):
        if not type(ngram) == list:
            raise ValueError("Param should be list of ('token', 'pos-tag')")

        self.terms = []
        self.pos_tags = []

        for word, pos_tag in ngram:
            self.terms.append(word)
            self.pos_tags.append(pos_tag)

    def get_head(self):
        return (self.terms[-1], self.pos_tags[-1])    

    def get_terms(self):
        return self.terms    

    def __str__(self):
        return str(zip(self.terms, self.pos_tags))

    def __repr__(self):
        return str(zip(self.terms, self.pos_tags))

