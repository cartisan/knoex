import itertools   


# get all combinations of a parsetree
# unsuprisingly awefull runtime complexity
def all_parsing_combinations(tree):

    # if terminal then return
    if type(tree) == str :
        return [[tree]]
    
    # get all parsing combinations of subnodes
    combis = []
    for t in tree :
        a = all_parsing_combinations(t)
        combis.append(a)

    # cross all combination of subnodes
    combis = itertools.product(*combis)
    combis = list(combis)
    for i,e in enumerate(combis) :
        e = list(itertools.chain.from_iterable(e))
        combis[i]=e

    # add current node
    combis.append([tree.node])

    return combis

# Numerates same named non-terminals in parse tress
def numerate_non_terminals(tree, num_dict={}):

    if tree.node in num_dict :
        num_dict[tree.node]+=1
    else :
        num_dict[tree.node]=0

    tree.node += str(num_dict[tree.node])

    for child in tree :

        if type(child)==str :
            pass
            #if child in num_dict :
            #    num_dict[child]+=1
            #else :
            #    num_dict[child]=0
        else :
            numerate_tags(child, num_dict)

# returns terminals of a subtree identified by a node
def get_terminals(tree,node):

    if type(tree) == str :
        return None

    if tree.node == node :
        return tree.leaves()

    for subtree in tree :
        terminals = get_terminals(subtree,node)
        if terminals != None :
            return terminals


if __name__ == '__main__':

    from nltk import Tree  
    import string
    from stat_parser import parser

    tree = Tree('A',[Tree('A',['A','A']),'A'])
    tree = parser.Parser().parse('All animals are organisms')
    print 'Tree:', tree
    print

    numerate_tags(tree)
    print 'Num_Tree:', tree
    print

    print 'NP0:', get_terminals(tree,'NP0')
    print 'NP1:', get_terminals(tree,'NP1') 
    print 'NP2:', get_terminals(tree,'NP2')
    print 'NP3:', get_terminals(tree,'NP3')
    print 'NP4:', get_terminals(tree,'NP4')
    print

    combis = all_parsing_combinations(tree)
    
    for i,x in enumerate(combis):
        print string.join(x)
        if i >= 20 :
            print '...'
            break;
    print
    print 'Total number of combinations: ', len(combis)