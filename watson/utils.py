from os import popen

def text_to_speech(text, engine='google'):
    if engine == 'google' :

        text = text.replace('(',' ')
        text = text.replace(')',' ')
        text = text.replace('`','')
        text = text.replace("'",'')
        text = text.replace("-",' ')
        popen('./speech.sh ' + text)
    elif engine == 'espeak' :
        popen('espeak ' + '"' + text + '"')
    else :
        print 'No such tos engine:', engine
        print text 

def replace_numbers(text):
    pass

