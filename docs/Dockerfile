FROM httpd:2.4

RUN apt update; \
    apt install -y python3-dev build-essential python3-pip

RUN pip3 install sphinx recommonmark pytest

COPY . /workflows

WORKDIR /workflows/
RUN pip3 install . --user

WORKDIR /workflows/docs
RUN make doctest && \
    make html; \
    ls ./build/html/*; \
    cp -r ./build/html/* /usr/local/apache2/htdocs/

