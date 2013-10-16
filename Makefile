# makefile for spw-api-scripts
# uses distutils files etc
# generates changelog first
# tabs have a special meaning in makefiles
# vim: set noet :


# generate source and binary RPMs
rpms: changelog
	python setup.py bdist_rpm 

changelog:
	git log --format="%ci [%h] - %an <%aE>%n%s%n%b" --date=short --no-merges > ChangeLog

# generate tarball
tarball:
	python setup.py sdist

# clean up build files
clean:
	find -type f -name '*.pyo' -o -name '*.pyc' | xargs rm -vf
	rm -rvf build

# clean up RPMs too
distclean: clean
	rm -rvf dist
    
