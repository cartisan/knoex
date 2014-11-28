# The idea is to have a language to match certain patterns in parse trees
# and translate them to some kind of a semantic structure

from nltk.tree import Tree, ParentedTree


class TreePatternMatcher :

    def __init__(self, pattern_list):

        if type(pattern_list) in [str,unicode] :
            pattern_list = pattern_list.split('\n')

        pattern_list = [p.strip().split() for p in pattern_list]

        self.pattern_list = pattern_list


    def match_all_patterns(self, match_tree):
        pass

    # matching has the find first 
    def match_pattern(self, pattern, match_tree):

        pattern = self._transform_pattern(pattern)
        match_tree = self._transform_match_tree(match_tree)
        starters = match_tree.follower_candidates()

    def _transform_pattern(self, pattern):

        if type(pattern) == int :
            pattern = self.pattern_list[pattern]
        elif type(pattern) in [str,unicode]:
            pattern = pattern.strip().split()
        else :
            pattern = list(pattern)

        return pattern


    def _transform_match_tree(self, match_tree):

        if type(match_tree) in [str,unicode,Tree] :
            match_tree = MatchTree(match_tree)
        elif type(match_tree) != MatchTree :
            raise Exception('Type: ' + type(match_tree) + \
                ' not convertable to MatchTree !')

        return match_tree


    

class MatchTree : # ???? maybe inheret from ParentedTree

    def __init__(self, tree_or_str):

        if type(tree_or_str) == Tree:
            self.original_tree = tree_or_str
        else :
            self.original_tree = Tree.fromstring(tree_or_str)

        self._construct_work_tree()
        self._construct_label_dict()
        self._construct_follower_dict()

    def _construct_work_tree(self, add_label_numbers=False) :
        # adds numbers to node 543
        work_tree = ParentedTree.convert(self.original_tree)

        # wrap leaves
        def wrap_leaves(node):
            for i,child in enumerate(node) :
                if isinstance(child, Tree):
                    wrap_leaves(child)
                else :
                    node[i] = ParentedTree(child,[])

        wrap_leaves(work_tree)

        if add_label_numbers :
            for i,node in enumerate(work_tree.subtrees()) :
                label = node.label() + '-' + str(i)
                node.set_label(label)

        self.work_tree = work_tree

    def _construct_label_dict(self):
        "returns a dict with node label as keys and subtrees as keys"
        label_dict = {}
        for node in self.work_tree.subtrees() :
            label_dict[node.label()] = node
        self.label_dict = label_dict

    def _construct_follower_dict(self):
        follower_dict = {}
        follower_dict[None] = self._get_followers(None)
        follower_dict[self.work_tree.label()] = []
        for node in self.work_tree.subtrees() :
            print node.label()
            follower_dict[node.label()] = self._get_followers(node)
        self.follower_dict = follower_dict

    def _get_followers(self, node):

        if node == None :
            tmp_node = self.work_tree
        else :
            # find next right sibling,uncle,great uncle ...
            tmp_node = node
            while tmp_node.right_sibling() == None :
                tmp_node = tmp_node.parent()
                if tmp_node == None :
                    return []
            tmp_node = tmp_node.right_sibling()

        # get line of first children
        followers = []
        while list(tmp_node) !=  []:
            followers.append(tmp_node)
            tmp_node = tmp_node[0]

        return followers

    def find_all(self, label_pattern):

        match_labeles = []
        match_nodes = []

        for label in label_dict :
            # matching is rudimentary for now
            # TODO: extend to regex
            if label_pattern == label :
                match_labeles.append(label)
                match_nodes.append(label_dict[label])

        return match_labeles, match_nodes

    