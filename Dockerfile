FROM buildpack-deps:stretch
MAINTAINER Igor Tolkachnikov <i.tolkachnikov@gmail.com>

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8

WORKDIR /opt/data
SHELL ["/bin/bash", "-c"]

# Using mirror - official repository was blocked for me, sorry.
RUN truncate -s 0 /etc/apt/sources.list \
    && bash -c 'echo -e "deb http://mirror.yandex.ru/debian stretch main\ndeb-src http://mirror.yandex.ru/debian stretch main" | tee /etc/apt/sources.list'

RUN apt-get update && apt-get install -y --no-install-recommends    \
        build-essential     \
        python-dev          \
        python3-dev         \
        libssl-dev          \
        zlib1g-dev          \
        libdb5.3-dev        \
        libbz2-dev          \
        libexpat1-dev       \
        liblzma-dev         \
        libncursesw5-dev    \
        libreadline-dev     \
        libsqlite3-dev      \
        libgdbm-dev         \
        libncurses5-dev     \
        libffi-dev          \
        libxml2-dev         \
        libxslt1-dev        \
		&& apt-get clean && rm -rf /var/lib/apt/lists/*

# Adding Python 3.6
RUN wget "https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz" \
	&& tar -xvf Python-3.6.5.tar.xz \
	&& cd ./Python-3.6.5 \
	&& ./configure && make && make install

# Clean up
RUN apt-get clean && rm -rf /tmp/* /var/tmp/* /opt/data/Python-3.6.5 /opt/data/Python-3.6.5.tar.xz

# Tox
RUN pip3 install --upgrade pip && pip3 install tox
CMD ["/bin/sh"]