from nltk.data import find
from nltk import download
import os

def setup_nltk_resources(resource_urls):
    """ Checks weather reasources like tokenizers are
    installed and installs them if not.

    Param:
        resource_urls: list of strings, containing
                       NLTK Resource URLs like:
                            'tokenizers/punkt.zip'
    """

    if not list == type(resource_urls):
        raise ValueError("resource_urls must contain a list.")

    for res in resource_urls:
        download(res)


def nltk_tree_to_dot(tree) :
    
    dot_code = 'digraph graphname {\n'
    dot_code += str(0) + ' [label="' + tree.node + '"];\n'    

    def get_subtrees(tree,node_number=0):
        dot_code = ""

        father_node_number = node_number

        for child in tree:

            node_number+=1

            if type(child) == str :
                dot_code += str(node_number) + ' [label="' + child + '"];\n'
                dot_code += str(father_node_number) + ' -> ' + str(node_number) + '\n'
            else :
                dot_code += str(node_number) + ' [label="' + child.node + '"];\n'
                dot_code += str(father_node_number) + ' -> ' + str(node_number) + '\n'
                new_code, node_number = get_subtrees(child,node_number)
                dot_code += new_code

        return dot_code, node_number

    new_code, _ = get_subtrees(tree)
    dot_code += new_code + '}'

    return dot_code


def dot_to_image(dot_code, name) :
    os.popen("echo '" + dot_code + "' > ~/temp.dot")
    os.popen('dot ~/temp.dot -Tpng -o' + name + '.png')
