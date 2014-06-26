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

    def get_subtrees(tree):
        dot_relations = ""

        for child in tree:
            if type(child) == str :
                dot_relations += '"' + tree.node + '"' + ' -> ' + '"' + child + '"' + '\n'
            else :
                dot_relations += '"' + tree.node + '"' + ' -> ' + '"' + child.node + '"' + '\n'
                dot_relations += get_subtrees(child)

        return dot_relations

    dot_code += get_subtrees(tree) + '}'

    return dot_code


def dot_to_image(dot_code, name) :
    os.popen("echo '" + dot_code + "' > ~/temp.dot")
    os.popen('dot ~/temp.dot -Tpng -o' + name + '.png')
