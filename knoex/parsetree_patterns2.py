from nltk import Tree, sent_tokenize
from corpus import get_wiki_text
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

    #print 'pos', 2, tree.node

    # if pattern does not match
    if tree.node not in pattern_dict :
        #print 'not in', tree.node, tree.leaves()
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
                #print 'match', pattern
                index = i
                break

        # if pattern does not match 
        if index == -1 :
            print 'no match for' + str(children_list)
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
                #print 'reli', rel[i], rel
            relations += [rel]
        
        # replace subtrees
        sub_relations = []
        for rel in relations :
            for i in range(len(rel)) :
                new_relations, outnode = match_tree(rel[i],pattern_dict)
                rel[i] = outnode
                sub_relations += new_relations
                #if i == outnodes_list[index] :
                #    global_outnode = outnode
        relations += sub_relations

        # determine outnode
        i = outnodes_list[index]
        _, outnode = match_tree(tree[i],pattern_dict)

        return relations, outnode
                

if __name__ == '__main__':

    import preprocessor as pp
    import os
    import sys

    parser = 'stanford'
    graph = []
    count = 0
    s = raw_input('S [' + str(count) + ']: ')
    show = 2
    while s != 'end':
        if s == '':
            s = raw_input('S [' + str(count) + ']: ')
            continue
        if s == 'clear':
            graph = []
            print '>>> graph has been cleared <<<'
            s = raw_input('S [' + str(count) + ']: ')
            continue
        if s == 'switch':
            if parser == 'stanford' :
                parser = 'berkeley'
            elif parser == 'berkeley' :
                parser = 'stat'
            else :
                parser = 'stanford'
            print '>>> parser set to', parser,'<<<'
            s = raw_input('S [' + str(count) + ']: ')
            continue
        if s == 'show':
            if show == 2:
                print '>>> show off <<<'
                show = 0
            elif show == 0:
                print '>>> show only graph <<<'
                show = 1
            else :
                print '>>> show graph and parsetrees <<<'
                show = 2
            s = raw_input('S [' + str(count) + ']: ')
            continue
        if s == 'random':
            s = get_wiki_text()
        else :
            print "====================================================================="

        pattern_dict = load_pattern_list()

        #for i in pattern_dict.items() :
        #    print i
        #raw_input()

        #s = "The Anaconda, or Water Boa, is one the world's largest snakes, when born they can be 3 feet (1m) long."
        #s = ' '.join(sys.argv[1:])
        
        sentences = sent_tokenize(s)
        for s in sentences:
            count+=1
            tree = pp.parse_sentence(s,parser)
            tree = tree[0]
            #tree = Tree('S', [Tree('NP', [Tree('NNP', ['Leon'])]), Tree('VP', [Tree('VBZ', ['hits']), Tree('NP', [Tree('NNP', ['Kai'])])]), Tree('.', ['.'])])
            
            path = utils.get_knoex_path()
            dot_code = utils.nltk_tree_to_dot(tree)
            utils.dot_to_image(dot_code, 'temptree_'+str(count))
            if show == 2:
                os.popen('gnome-open ' + 'temptree_'+str(count)+'.png')

            g,_ = match_tree(tree, pattern_dict)
            graph += g

        while ['','',''] in graph:
            graph.remove(['','',''])
        print graph
        
        dot_code = utils.list_of_tripels_to_dot_fancy(graph)
        utils.dot_to_image(dot_code, 'tempgraph')

        if show :
            os.popen('gnome-open ' + 'tempgraph.png')
        s = raw_input('S [' + str(count) + ']: ')


