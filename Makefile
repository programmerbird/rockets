all: fulltest

version:
	echo 'VERSION=`git describe --tags`; sed -i "s/^VERSION\=.*$$/VERSION=\"$${VERSION}\"/g" rockets/__init__.py' | sh
	
test:
	# make local
	mkdir -p tests
	virtualenv --no-site-packages tests/.rockets
	grep -v "egg=Rocket" rockets/bin/rocket2 > env/bin/rocket2
	chmod +x env/bin/rocket2

	readlink -f . > env/lib/python2.7/site-packages/rockets.pth
	readlink -f . > tests/.rockets/lib/python2.7/site-packages/rockets.pth
	cd tests; rocket2 init
	
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
	

