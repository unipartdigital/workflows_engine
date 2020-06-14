FROM httpd:2.4

RUN apt update; \
    apt install -y python3-dev build-essential python3-pip

RUN pip3 install sphinx recommonmark

COPY . /workflows
WORKDIR /workflows/docs
RUN make html; \
    ls ./build/html/*; \
    cp -r ./build/html/* /usr/local/apache2/htdocs/

