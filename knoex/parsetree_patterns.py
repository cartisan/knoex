from nltk.tree import Tree
from copy import copy

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
			asib = ()
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
		ac_node = self
		for i in nodepath :
			ac_node = ac_node[i]
		return ac_node


	def get_node(self, nodepath):
		sub = self.get_subtree(nodepath)
		if type(sub)==Tree:
			return sub.node
		else :
			return sub


"""def match(pattern, parsetree):
	d = parsetree.nt_dict

	phrase_matches = []

	for phrase in pattern :
		if phrase not in d :
			print 'out here'
			return []
		else :
			phrase_matches.append(d[phrase])


	def match_(phrase_matches, node, path, pattern_matches):

		if len(phrase_matches) == 0:
			pass

		nodes = parsetree.next_to(node)

		matches = intersect(phrase_matches[0], nodes)

		for m in matches :
			match_(phrase_matches[1:], m)"""



	print phrase_matches


def intersect(l1,l2):
	s = set(l1).intersection(set(l2))
	return list(s)


if __name__=="__main__":
	import preprocessor as pp
	tree = pp.parse_sentence('Leon hits Kai.')
	
	




