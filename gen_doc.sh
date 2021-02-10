rm -r doc/source
mkdir doc/source
cp doc/index.rst doc/source/
cp doc/conf.py doc/source/
sphinx-apidoc -o doc/source src
export SOURCEDIR=doc/source
export BUILDDIR=doc/build
sphinx-build -M clean $SOURCEDIR $BUILDDIR
sphinx-build -M html $SOURCEDIR $BUILDDIR
