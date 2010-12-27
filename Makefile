all: fulltest

version:
	echo 'VERSION=`git describe --tags`; sed -i "s/^VERSION\=.*$$/VERSION=\"$${VERSION}\"/g" rockets/__init__.py' | sh

testenv: clean build/rockets.tar.gz
	virtualenv --no-site-packages env 
	env/bin/python setup.py install 
	readlink -f . > env/lib/python2.6/site-packages/rockets.pth

tt:
	# make local
	grep -v "egg=Rocket" rockets/bin/rocket > env/bin/rocket
	chmod +x env/bin/rocket
	
	# test begin!
	rm -rf tests
	mkdir -p tests
	cd tests; rocket init
	mkdir -p tests/.rockets/lib/python2.6/site-packages/
	readlink -f . > tests/.rockets/lib/python2.6/site-packages/rockets.pth
	
test:
	cd tests; rocket init
	
fulltest: clean build/rockets.tar.gz
	rm -rf /tmp/rockets-env 
	rm -rf /tmp/rockets-test
	virtualenv --no-site-packages /tmp/rockets-env 
	/tmp/rockets-env/bin/pip install build/rockets.tar.gz 
	mkdir -p /tmp/rockets-test
	cd /tmp/rockets-test/; /tmp/rockets-env/bin/rocket init

build/rockets.tar.gz: version
	find . -name "*~" -exec rm -f {} \;
	find . -name "*.pyc" -exec rm -f {} \;
	rm -rf build/
	mkdir -p build/
	tar -cf build/rockets.tar rockets setup.py
	gzip build/rockets.tar 

clean:
	rm -rf build/
	
setupgit:
	git remote add github "git@github.com:ssimasanti/rockets.git"
	git remote add dropbox ../../Dropbox/projects/rockets/
	echo "build/" >> .git/info/exclude 
	echo "tests/" >> .git/info/exclude

