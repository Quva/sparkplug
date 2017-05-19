FROM extranet.quva.fi:57104/python-base:master

COPY . .

CMD make test