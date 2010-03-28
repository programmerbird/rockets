
test: clean build/rockets.tar.gz
	virtualenv --no-site-packages env 
	env/bin/python setup.py install 

	# make local
	cp rockets/bin/rocket-test env/bin/rocket
	chmod +x env/bin/rocket
	
	# test begin!
	rm -rf tests
	mkdir tests
	cd  tests; rocket init
	
fulltest: clean build/rockets.tar.gz
	rm -rf /tmp/rockets-env 
	rm -rf /tmp/rockets-test
	virtualenv --no-site-packages /tmp/rockets-env 
	/tmp/rockets-env/bin/pip install build/rockets.tar.gz 
	mkdir -p /tmp/rockets-test
	cd /tmp/rockets-test/; /tmp/rockets-env/bin/rocket init

build/rockets.tar.gz:
	find . -name "*~" -exec rm -f {} \;
	find . -name "*.pyc" -exec rm -f {} \;
	rm -rf build/
	mkdir -p build/
	tar -cvvf build/rockets.tar rockets setup.py
	gzip build/rockets.tar 

clean:
	rm -rf build/
	
setupgit:
	cp rockets/bin/git-post-commit .git/hooks/post-commit 
	chmod +x .git/hooks/post-commit
	git remote add github "git@github.com:ssimasanti/rockets.git"
	git remote add dropbox ../../Dropbox/projects/rockets/
	echo "build/" >> .git/info/exclude 
	echo "tests/" >> .git/info/exclude 
	
