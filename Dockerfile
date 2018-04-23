FROM extranet.quva.fi:57104/python-base:master

COPY . .

RUN pip3 install -r requirements.txt
  
CMD make test