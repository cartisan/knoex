from os.path import abspath, dirname

watson_path = dirname(abspath(__file__))
stanford_path = abspath(watson_path + '/../' + 'stanford-parser-full-2014-08-27')
stanford_parser = stanford_path + '/' + 'stanford-parser.jar'
stanford_models = stanford_path + '/' + 'stanford-parser-3.4.1-models.jar'

stanford_ner_path = abspath(watson_path + '/../' + 'stanford-ner-2014-08-27')
stanford_ner_classifier = stanford_ner_path + '/classifiers/' + 'english.all.3class.distsim.crf.ser.gz'
stanford_ner = stanford_ner_path + '/' + 'stanford-ner.jar'


tree_patterns_path =  watson_path + '/' + 'pattern_list'

pattern_semantic_separator = '->'

image_viewer = 'gnome-open'

del abspath, dirname
