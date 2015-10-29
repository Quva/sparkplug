
PROG := python setup.py

.PHONY : clean build test install default release

default: clean build install

release: clean build test install

clean:
	$(PROG) clean

build:
	$(PROG) build

test:
	nosetests-2.7 -v

install:
	$(PROG) install


