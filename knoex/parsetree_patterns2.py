from nltk import Tree
import utils

#pattern_dict = {}

#pattern_dict['S']  = [[['NP','VP','.'],[(0,None,1)],1]]
#pattern_dict['VP'] = [[['VBZ','NP'],[(0,None,1)],0]]

#print pattern_dict

def load_pattern_list():
    path = utils.get_knoex_path()
    lines = open(path + 'pattern_list2').readlines()
    pattern_dict = {}
    for line in lines :

        if line.strip() == '' :
            continue

        head, pat, sems, out = line.split('|')
        head = head.strip()
        pat = [p for p in pat.split() if p!='']
        
        sems = sems.split(';')
        for j,sem in enumerate(sems):
            sem = sem.split(',')
            for i in range(len(sem)):
                sem[i] = sem[i].strip()
                if sem[i] == '' :
                    sem[i]=None
                else :
                    if sem[i].isdigit() :
                        sem[i]=int(sem[i])
            sem = tuple(sem)
            sems[j] = sem
        sem = sems
        out = int(out.strip())

        if head in pattern_dict :
            pattern_dict[head]+=[[pat,sem,out]]
        else :
            pattern_dict[head]=[[pat,sem,out]]
    return pattern_dict



def match_tree(tree, pattern_dict):

    #print 'pos', 1, tree
    #raw_input()

    if type(tree) != Tree :
        return [], tree

    #print 'pos', 2

    # if pattern does not match
    if tree.node not in pattern_dict :
        print 'not in', tree.node, tree.leaves()
        o = '_'.join(tree.leaves())
        return [],o

    #print 'pos', 3

    pattern_list  = [item[0] for item in pattern_dict[tree.node]]
    semantic_list = [item[1] for item in pattern_dict[tree.node]]
    outnodes_list = [item[2] for item in pattern_dict[tree.node]]

    #print 'pos', 4
    #print 'pattern_list',  pattern_list
    #print 'semantic_list', semantic_list
    #print 'outnodes_list', outnodes_list
    #print 'pos', 5
    for i, pattern in enumerate(pattern_list):

        # make list of children nodes
        children_list = []
        for subtree in tree:
            if type(subtree) == Tree :
                node = subtree.node
            else :
                node = subtree
            children_list += [node]

        #print 'pos', 6, children_list

        # find a match to childrens list
        index = -1
        for i,pattern in enumerate(pattern_list):
            if pattern == children_list :
                print 'match', pattern
                index = i
                break

        # if pattern does not match 
        if index == -1 :
            print 'no match'
            o = '_'.join(tree.leaves())
            return [],o

        # create interpretations
        #print 'pos', 7, semantic_list
        relations = []
        for sem in semantic_list[index] :
            rel = ['','','']
            for i in range(len(sem)):
                if type(sem[i]) == int:
                    rel[i] = tree[sem[i]]
                elif type(sem[i]) == str: 
                    rel[i] = sem[i]
                print 'reli', rel[i], rel
            relations += [rel]
        
        # replace subtrees
        sub_relations = []
        for rel in relations :
            for i in range(len(rel)) :
                new_relations, outnode = match_tree(rel[i],pattern_dict)
                rel[i] = outnode
                sub_relations += new_relations
                if i == outnodes_list[index] :
                    global_outnode = outnode
        relations += sub_relations

        return relations, global_outnode
                

if __name__ == '__main__':

    import preprocessor as pp
    import os

    pattern_dict = load_pattern_list()

    for i in pattern_dict.items() :
        print i
    raw_input()

    #s = "The Anaconda, or Water Boa, is one the world's largest snakes, when born they can be 3 feet (1m) long."
    s = "I am awesome."
    tree, dep = pp.parse_sentence(s,'stanford',None,True)
    tree = tree[0]
    #tree = Tree('S', [Tree('NP', [Tree('NNP', ['Leon'])]), Tree('VP', [Tree('VBZ', ['hits']), Tree('NP', [Tree('NNP', ['Kai'])])]), Tree('.', ['.'])])
    
    path = utils.get_knoex_path()
    dot_code = utils.nltk_tree_to_dot(tree)
    utils.dot_to_image(dot_code, 'temptree_stanford')
    os.popen('gnome-open ' + 'temptree_stanford.png')

    graph,_ = match_tree(tree, pattern_dict)
    print graph
    
    dot_code = utils.list_of_tripels_to_dot(graph)
    utils.dot_to_image(dot_code, 'tempgraph_stanford')

    os.popen('gnome-open ' + 'tempgraph_stanford.png')


