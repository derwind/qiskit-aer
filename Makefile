TARGET=_skbuild

.PHONY: all build install clean lint
all: $TARGET
$TARGET: build

build:
	sh build.sh 2> build_log.txt

install: $TARGET
	sh install_editable.sh

clean:
	@rm -rf $TARGET

lint:
	pycodestyle --ignore=E402,W504 --max-line-length=100 qiskit_aer
	pylint -j 2 -rn qiskit_aer
