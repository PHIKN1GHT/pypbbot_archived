rm -r docs/source
mkdir docs/source
cp docs/index.rst docs/source/
cp docs/conf.py docs/source/
sphinx-apidoc -o docs/source/ pypbbot
export SOURCEDIR=docs/source
export BUILDDIR=docs/build
sphinx-build -M clean $SOURCEDIR $BUILDDIR
sphinx-build -M html $SOURCEDIR $BUILDDIR
