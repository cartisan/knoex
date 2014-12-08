import os

from nltk.tree import Tree
from utils import parse

import configurations as conf

def nltk_tree_to_dot(tree) :
    
    dot_code = 'digraph graphname {\n'
    dot_code += str(0) + ' [label="' + tree.label() + '"];\n'

    def get_subtrees(tree,node_number=0,terminals = '{ rank=same; '):
        dot_code = ""

        father_node_number = node_number


        for child in tree:

            node_number+=1

            if type(child) in [str,unicode] :
                dot_code += str(node_number) + ' [label="' + child + '" shape=box];\n'
                dot_code += str(father_node_number) + ' -> ' + str(node_number) + '\n'
                terminals += str(node_number) + '; '
            else :
                dot_code += str(node_number) + ' [label="' + child.label() + '"];\n'
                dot_code += str(father_node_number) + ' -> ' + str(node_number) + '\n'
                new_code, node_number, terminals = get_subtrees(child,node_number,terminals)
                dot_code += new_code

        return dot_code, node_number, terminals

    new_code, _, terminals = get_subtrees(tree)
    dot_code += terminals + '}\n'
    dot_code += new_code + '}'

    return dot_code


def build_triple_code(tripel_list):
    dot_code = ""
    for tripel in tripel_list:
        dot_code += '"' + tripel[0] + '" -> "' + tripel[2] + '" [label="'+ tripel[1] + '"]\n'
    return dot_code


def list_of_tripels_to_dot(tripel_list):
    dot_code = 'digraph graphname {\n'
    dot_code += build_triple_code(tripel_list)
    return dot_code + '}'


def list_of_tripels_to_dot_fancy(tripel_list):
    dot_code = 'digraph graphname {\n'
    dot_code += 'rankdir=LR\n'
    dot_code += 'node [shape=box]\n'

    node_shape_list = []
    for i,tripel in enumerate(tripel_list) :
        if tripel[1] == 'to_verb' :
            node_shape_list.append(tripel[2] + ' [shape=diamond]')
            tripel_list[i] = (tripel[0],'',tripel[2])
        elif tripel[1] == 'from_verb' :
            node_shape_list.append(tripel[0] + ' [shape=diamond]')
            tripel_list[i] = (tripel[0],'',tripel[2])
        elif tripel[1] == 'property_of' :
            node_shape_list.append(tripel[0] + ' [shape=egg]')
    
    for s in set(node_shape_list) :
        dot_code += s+'\n'

    dot_code += build_triple_code(tripel_list)

    return dot_code + '}'


def taxonomy_to_dot(concepts, relations):
    dot_code = 'digraph graphname {\n'
    for concept in concepts:
        dot_code += '"' + concept + '"\n'

    dot_code += build_triple_code(relations)
    return dot_code + '}'


def dot_to_image(dot_code, name) :
    tmp_file = 'temp.dot'
    f = open(tmp_file, 'w')
    f.write(dot_code)
    f.close()
    os.popen('dot temp.dot -Tpng -o' + name + '.png')
    os.remove('temp.dot')


# parses a sentence and draws a tree / accepts also directly accepts parsetrees
def draw_parsetree(arg, cut_root_node=True):
    
    if isinstance(arg,(str,unicode)):
        arg = parse(arg)
    if isinstance(arg, Tree):
        arg = [arg]
    
    for i,tree in enumerate(arg) :
        if cut_root_node : tree = tree[0]
        png_path = 'temp_tree_' + str(i) + '.png'
        dot_code = nltk_tree_to_dot(tree)
        dot_to_image(dot_code, 'temp_tree_' + str(i))
        os.popen(conf.image_viewer + ' ' + png_path)

