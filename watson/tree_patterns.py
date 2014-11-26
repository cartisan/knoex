# The idea is to have a language to match certain patterns in parse trees
# and translate them to some kind of a semantic structure

from nltk.tree import Tree

class MatchTree ():

    def __init__(self, tree_or_str):

        if type(tree_or_str) == Tree:
            self.original_tree = tree_or_str
        else :
            self.original_tree = Tree.fromstring(tree_or_str)

        self.work_tree  = self._lable_tree_nodes()
        self.label_dict = self._construct_label_dict()

    def _label_tree_nodes(self) :
        # adds numbers to node 543
        work_tree = self.original_tree.copy()

        for i,node in enumerate(work_tree.subtrees()) :
            lable = node.label() + '-' + str(i)
            node.set_lable(lable)

        return work_tree


    def _construct_label_dict(self):
        "returns a dict with node label as keys and subtrees as keys"
        label_dict = {}
        for node in worK_tree.subtrees() :
            label_dict[node.label()] = node
        return label_dict