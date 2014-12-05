# The idea is to have a language to match certain patterns in parse trees
# and translate them to some kind of a semantic structure

from copy import copy

from nltk.tree import Tree, ParentedTree

from configurations import tree_patterns_path, pattern_semantic_separator
import recources as res


def load_pattern_list():

    with open(tree_patterns_path) as pattern_file:
        pattern_list = pattern_file.readlines()
    #maybe just use for instead of list_comprehentions
    pattern_list = [line.split(pattern_semantic_separator) for line in pattern_list]

    pattern_list = [[pair[0].strip().split(),pair[1].strip().split()] for pair in pattern_list]

    patterns, semantic_tranlations = zip(*pattern_list)

    return patterns, semantic_tranlations


class TreePatternMatcher :

    def __init__(self):
        pattern_list, semantic_tranlations = load_pattern_list()
        self.pattern_list = pattern_list
        self.semantic_tranlations = semantic_tranlations

        self.function_dict = {'dbpedia' : res.dbpedia_wrapper,
                        'wordnet' : res.get_wordnet_definition }

    def match_all(self, match_tree, whole_sentence):
        match_tree = self._transform_match_tree(match_tree)
        matches = []
        for pattern in self.pattern_list :
            #print pattern
            #print match_tree.work_tree.pprint().replace(' ','').replace('\n',' ')
            matches += [self.match_pattern(pattern, match_tree, whole_sentence)]
        return matches        

    # matching has the find first 
    def match_pattern(self, pattern, match_tree, whole_sentence=False):

        pattern = self._transform_pattern(pattern)

        if whole_sentence :
            starters = match_tree.follower_dict[None]
        else :
            starters = match_tree.get_all_nodes()

        current_match = [-1]*len(pattern)

        def _match(nodes, index):

            matches = []

            for node in nodes :
                # here is the actual comparison :
                if pattern[index] != node.label() :
                    continue

                current_match[index] = node

                followers = match_tree.follower_dict[node]

                if index+1==len(pattern) :
                    if whole_sentence and followers :
                        continue
                    matches += [copy(current_match)]

                elif followers:
                    matches += _match(followers, index+1)

            return matches

        matches = _match(starters, 0)

        return matches


    def semantics_all(self, all_matches,silent=True):

        answers = []

        for i,matches in enumerate(all_matches):
            s = self.semantic_tranlations[i]
            if s[0] in ['none','None'] :
                if not silent: print 'Empty semantic!'
                continue
            p = self.pattern_list[i]
            for m in matches :
                answers += self.match_to_semantics(p,m,s)
        return answers


    def match_to_semantics(self, pattern, match, semantic):

        output = []

        match_labels = [m.label() for m in match]
        match_terminals = [" ".join(MatchTree.get_terminals(m)) for m in match]
        #print
        #print 'match_labels', match_labels
        #print 'match_terminals', match_terminals
        #print semantic
        sem_func, sem_args = zip(*[s.split(':') for s in semantic])
        sem_args = [a.split(',') for a in sem_args]
        
        #print 'sem_func', sem_func
        #print 'sem_args', sem_args

        for func,args in zip(sem_func,sem_args) :
            arg_terminals = []
            for a in args :
                if a in match_labels :
                    arg = match_terminals[match_labels.index(a)]
                else :
                    arg = a
                arg_terminals.append(arg)
            
            #print 'arg_terminals', arg_terminals
            output += [self.function_dict[func](*arg_terminals)]

        return output


    def _transform_pattern(self, pattern):

        if type(pattern) == int :
            pattern = self.pattern_list[pattern]
        elif type(pattern) in [str,unicode]:
            pattern = pattern.strip().split()
        else :
            pattern = list(pattern)

        return pattern


    def _transform_match_tree(self, match_tree):

        if isinstance(match_tree, (str,unicode,Tree)) :
            match_tree = MatchTree(match_tree)
        elif not isinstance(match_tree, MatchTree) :
            raise Exception('Type: ' + str(type(match_tree)) + \
                ' not convertable to MatchTree !')

        return match_tree


    

class MatchTree :

    def __init__(self, tree_or_str):

        if type(tree_or_str) == Tree:
            self.original_tree = tree_or_str
        else :
            self.original_tree = Tree.fromstring(tree_or_str)

        self.work_tree = self._construct_work_tree()
        self.label_dict = self._construct_label_dict()
        self.follower_dict = self._construct_follower_dict()

    @classmethod
    def get_terminals(cls,node):

        if len(node) == 0 :
            return [node.label()]

        terminals = []
        for subnode in node.subtrees() :
            if len(subnode) == 0 :
                terminals.append(subnode.label())

        return terminals

    def get_all_nodes(self):
        return list(self.work_tree.subtrees()) + [self.work_tree]

    def _construct_work_tree(self) :
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

        # freeze worktree to use as key in dict
        return work_tree.freeze()

    def _construct_label_dict(self):
        label_dict = {}
        for node in self.work_tree.subtrees() :
            if node.label() in label_dict :
                label_dict[node.label()].append(node)
            else :
                label_dict[node.label()] = [node]
        return label_dict

    def _construct_follower_dict(self):
        follower_dict = {}
        follower_dict[None] = self._get_followers(None)
        follower_dict[self.work_tree] = []
        for node in self.work_tree.subtrees() :
            #print node.label()
            follower_dict[node] = self._get_followers(node)
        return follower_dict

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
        followers.append(tmp_node)

        return followers

    