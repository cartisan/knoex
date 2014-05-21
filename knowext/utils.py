from nltk.data import load, find


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
        try:
            find(res)
        except LookupError:
            print "Package {} not found. Downloading.".format(res)
            load(res)
