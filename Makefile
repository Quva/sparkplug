
PROG := python3 setup.py

.PHONY : clean build test install default release

default: clean build install

release: clean build test install

clean:
	$(PROG) clean

build:
	$(PROG) build

test:
	nosetests -v
	nosetests-3.4 -v

install:
	$(PROG) install

docker:
	docker build -t sparkplug . && docker run sparkplug nosetests -v


