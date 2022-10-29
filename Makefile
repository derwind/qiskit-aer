TARGET=_skbuild

.PHONY: all build install clean
all: $TARGET
$TARGET: build

build:
	sh build.sh 2> build_log.txt

install: $TARGET
	sh install_editable.sh

clean:
	@rm -rf $TARGET
