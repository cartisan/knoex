knowext
=======
Ontology extraction from unstructured text.

## Dev Setup 
In order to have the same development environment for all developers we use vagrant, a headless virtual machine, that we can control from
the host using a python package called fabric.

### Installation
On your host:
1. Install vagrant: http://www.vagrantup.com/downloads
2. Install virtual box: https://www.virtualbox.org/wiki/Downloads
3. Install python 2.7 on your host: https://www.python.org/downloads/
4. Install fabric: http://www.fabfile.org/installing.html

Now you are all set! All dependencies, compilers and co. go to the VM. Let's get it over with:

1. Clone the repo: `git clone https://github.com/cartisan/knowext.git`
2. Start the virtual box, install all the needed gear and get the python dependencies:
```
vagrant up
fab vagrant install
fab vagrant deploy
```
3. To power off the VM run `vagrant halt`

### Control from host
Start the VM using `vagrant up`. You can now ssh onto it using `vagrant ssh` (close session using Ctrl + D). To execute fabric
tasks from the host you can use `fab vagrant task-name` where *task-name* is the name of the task defined in *fabfile.py*.

(t.b.c)


### Stanford Parser:
1. Download Stanford Parser : http://nlp.stanford.edu/software/lex-parser.shtml#Download
2. Create folder "stanford_parser" inside the knoex folder
3. Extract files from the .zip file into the newly created folder

### Berkeley Parser:
1. Download Berkeley Parser jar file from : https://code.google.com/p/berkeleyparser/downloads/list
2. Rename .jar file to BerkeleyParser.jar
2. Download Grammar ( eng_sm6.gr  )  for some page
3. Create folder "berkeley_parser" inside the knoex folder and put both downloaded files in it

BOTH PARSERS REQUIRE JAVA 
