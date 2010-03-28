
test:
	virtualenv --no-site-packages env 
	env/bin/python setup.py install 
	rm -rf tests
	mkdir tests
	cd  tests; ../env/bin/rocket init
	
setupgit:
	cp rockets/bin/git-post-commit .git/hooks/post-commit 
	chmod +x .git/hooks/post-commit
	git remote add github "git@github.com:ssimasanti/rocket.git"
	git remote add dropbox ../../Dropbox/projects/rockets/
	echo "build/" >> .git/info/exclude 
	echo "tests/" >> .git/info/exclude 
	
