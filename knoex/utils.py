from nltk import download
import os
from os.path import expanduser

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

    def get_subtrees(tree,node_number=0,terminals = '{ rank=same; '):
        dot_code = ""

        father_node_number = node_number


        for child in tree:

            node_number+=1

            if type(child) == str :
                dot_code += str(node_number) + ' [label="' + child + '" shape=box];\n'
                dot_code += str(father_node_number) + ' -> ' + str(node_number) + '\n'
                terminals += str(node_number) + '; '
            else :
                dot_code += str(node_number) + ' [label="' + child.node + '"];\n'
                dot_code += str(father_node_number) + ' -> ' + str(node_number) + '\n'
                new_code, node_number, terminals = get_subtrees(child,node_number,terminals)
                dot_code += new_code

        return dot_code, node_number, terminals

    new_code, _, terminals = get_subtrees(tree)
    dot_code += terminals + '}\n'
    dot_code += new_code + '}'

    return dot_code


def list_of_tripels_to_dot(tripel_list):
    dot_code = 'digraph graphname {\n'
    for tripel in tripel_list :
        dot_code += '"' + tripel[0] + '" -> "' + tripel[2] + '" [label="'+ tripel[1] + '"]\n'
    return dot_code + '}'


def dot_to_image(dot_code, name) :
    os.popen("echo '" + dot_code + "' > ~/temp.dot")
    os.popen('dot ~/temp.dot -Tpng -o' + name + '.png')
    home = expanduser("~")
    os.remove(home + '/temp.dot')


def which(program):
    """ Checks if a string corresponds to a shell command and returns its location. """
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None
