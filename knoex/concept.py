class Concept(object):
    def __init__(self, synset=None, name=None, term=None):
        self.synset = synset
        self.name = name
        self.term = term
        if synset:
            self.hypernyms = synset.hypernyms()
            self.hyponyms = synset.hyponyms()
        else:
            self.hypernyms = None
            self.hyponyms = None
        self.relations = []

    def __str__(self):
        if self.synset:
            name = "Concept({})".format(str(self.synset))
        else:
            name = "Concept({})".format(str(self.name))

        return name

    def __repr__(self):
        if self.synset:
            name = "Concept({})".format(str(self.synset))
        else:
            name = "Concept({})".format(str(self.name))

        return name

    def __eq__(self, other):
        if isinstance(other, Concept):
            return hash(self) == hash(other)
        else:
            return False

    def __hash__(self):
        if self.synset:
            return hash(str(self.synset))
        else:
            if type(self.name) == list:
                return hash(" ".join(self.name))

            return hash(self.name)

    def add_relation(self, concept, relation):
        self.relations.append((concept, relation))

    def get_term(self):
        return self.term

    def get_hypernyms(self):
        return self.hypernyms

    def get_hyponyms(self):
        return self.hyponyms
