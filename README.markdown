## What this project is all about
	rocket use rackspaceserver1

	rocket install pythonweb
	rocket pythonweb add helloproject
	rocket pythonweb domain add helloproject www.helloweb.com
	
	rocket push 
	
	git push ssh://hellouser@rackspaceserver1/~/helloproject master 
	
	
## Usage
Add Cloud Provider 
	rocket provider add rackspaceaccount1 

List all servers from the providers 
	rocket node 
	
Select servers 
	rocket use rackspaceserver1

Reset root password
	rocket password reset

Setup a python web server
	rocket install pythonweb
	rocket pythonweb add helloworldproject
	rocket pythonweb domain add helloworldproject www.helloworld.com
	
Deploy changes to server
	rocket push 
	
Upload your web projects (Thanks to boatyard project)
	
	git push ssh://hellouser@rackspaceserver1/~/helloworldproject master 
	
Add public key
	rocket publickey add bird < ~/.ssh/id_rsa.pub
	rocket authorized_keys add bird to root 
	rocket authorized_keys add bird to hellouser 
	
## Installation

	pip install -r http://github.com/ssimasanti/rockets/raw/master/setup.ini

Start a working environment 
	mkdir workingenv
	cd workingenv/
	
	rocket init 

## Create your own server template
Coming soon..
