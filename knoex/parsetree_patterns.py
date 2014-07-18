from nltk.tree import Tree
from copy import copy
from string import join

class ParseTree:

	def __init__(self, tree_or_str):

		if type(tree_or_str) == Tree:
			self.tree = tree_or_str
		else :
			self.tree = Tree(tree_or_str)

		nt_dict={}
		nodepaths=[]
		pos=()

		def subroutine(tree, pos, node_list) :

			node_list+=[pos]

			if type(tree) == str :
				if tree in nt_dict :
					nt_dict[tree]+=[pos]
				else :
					nt_dict[tree]=[pos]
			else :
				if tree.node in nt_dict :
					nt_dict[tree.node]+=[pos]
				else :
					nt_dict[tree.node]=[pos]

				for i,child in enumerate(tree) :
					subroutine(child, pos+(i,), node_list)

		subroutine(self.tree, pos, nodepaths)

		self.nt_dict = nt_dict
		self.nodepaths = nodepaths


	# returns a list of nodes that can be next to the argument node
	def next_to(self, nodepath='start'):
		# find next anchestrial sibling

		if nodepath == 'start' :
			asib = []
		else:
			asib = list(copy(nodepath))
			while len(asib)>0 :
				asib[-1]+=1
				if tuple(asib) in self.nodepaths :
					break
				asib = asib[:-1]

			if len(asib) == 0 :
				return []

		next_to_list = []

		while tuple(asib) in self.nodepaths :
			next_to_list += [tuple(asib)]
			asib += [0]

		return next_to_list


	def get_subtree(self, nodepath):
		ac_node = self.tree
		for i in nodepath :
			ac_node = ac_node[i]
		return ac_node


	def get_node(self, nodepath):
		sub = self.get_subtree(nodepath)
		if type(sub)==Tree:
			return sub.node
		else :
			return sub

	def get_terminals(self, nodepath):
		sub = self.get_subtree(nodepath)
		if type(sub)==Tree:
			return sub.leaves()
		else :
			return [sub]


def match(pattern, parsetree):

	def match_(pattern, nodepath, parsetree):

		if len(pattern) == 0 :
			print 'matched', nodepath
			return [[]]

		token_matches = parsetree.nt_dict[pattern[0]]
		next_to = parsetree.next_to(nodepath)

		matches = []
		for next_nodepath in intersect(token_matches, next_to) :
			submatches = match_(pattern[1:], next_nodepath, parsetree)
			for submatch in submatches :
				matches.append([next_nodepath]+submatch)

		return matches

	return match_(pattern, 'start', parsetree)


def match_to_terminals(match, parsetree):
	list_ = []
	for path in match :
		list_.append(parsetree.get_terminals(path))
	return list_

def match_to_joined_terminals(match, parsetree):
	list_ = []
	for path in match :
		list_.append(join(parsetree.get_terminals(path)))
	return list_
		

def intersect(l1,l2):
	s = set(l1).intersection(set(l2))
	return list(s)


if __name__=="__main__":
	import preprocessor as pp
	tree = pp.parse_sentence('The python hits Kai.')
	tree = tree[0]
	pt = ParseTree(tree)
	print
	for item in pt.nt_dict.items() :
		print item
	print
	for path in pt.nodepaths :
		print path
	print

	print 'test get_subtree'
	print pt.get_subtree((1,))
	print 'test get_node'
	print pt.get_node((1,))
	print 'test get_terminals'
	print pt.get_terminals((1,))

	print 'test next_to ()'
	print pt.next_to(())
	print 'test next_to (0,)'
	print pt.next_to((0,))
	print 'test next_to start'
	print pt.next_to('start')
	print
	print 'text match'

	pattern = ['NP','VBZ','NP']
	matches = match(pattern, pt)

	for match in matches :
		print match_to_joined_terminals(match, pt)
	

