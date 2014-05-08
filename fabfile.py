from fabric.api import *
from fabric.context_managers import shell_env
from fabtools.vagrant import vagrant
from fabtools.python import virtualenv

@task
def setup():
	sudo('apt-get update')
	sudo('apt-get install -y git')
	sudo('apt-get install -y make')
	sudo('apt-get install -y g++')
	sudo('apt-get install -y python-pip')
	sudo('apt-get install -y python-dev')
	sudo('apt-get install libxml2-dev libxslt1-dev python-dev')
	sudo('pip install virtualenv')
	run('virtualenv knowext-env')
	
@task
def deploy():
	with virtualenv('knowext-env'):
		sudo('pip install -r /vagrant/requirements.txt')