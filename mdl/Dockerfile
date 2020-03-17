FROM mcr.microsoft.com/dotnet/core/sdk:2.1 AS build

# Nodejs
ENV NODE_VERSION 10.18.0
ENV NODE_DOWNLOAD_SHA 78a46d1e1f6db68c0732981fc9a1fe8583eabb4e232f1ed742f7dedc5bed3ddd

RUN curl -SL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.gz" --output nodejs.tar.gz \
    && echo "$NODE_DOWNLOAD_SHA nodejs.tar.gz" | sha256sum -c - \
    && tar -xzf "nodejs.tar.gz" -C /usr/local --strip-components=1 \
    && rm nodejs.tar.gz \
    && ln -s /usr/local/bin/node /usr/local/bin/nodejs

# Python3
RUN apt-get update
RUN apt-get install -y \
	git \
	wget \
	curl \
	build-essential \
	zlib1g-dev \
	libncurses5-dev \
	libgdbm-dev \
	libnss3-dev \
	libssl-dev \
	libreadline-dev \
	libffi-dev

# Set Python version
ARG PYTHON_VERSION='3.8.0'
# Set pyenv home
ARG PYENV_HOME=/root/.pyenv

# Install pyenv, then install python versions
RUN git clone --depth 1 https://github.com/pyenv/pyenv.git $PYENV_HOME && \
    rm -rfv $PYENV_HOME/.git

ENV PATH $PYENV_HOME/shims:$PYENV_HOME/bin:$PATH

RUN pyenv install $PYTHON_VERSION
RUN pyenv global $PYTHON_VERSION
RUN pip install --upgrade pip && pyenv rehash


RUN npm install --global typescript@3.1.6

WORKDIR /

COPY . .

RUN wget https://raw.githubusercontent.com/Vermont-Labor-UI/cdn_dupe_checker/master/dupechecker.py -O dupechecker.py
RUN wget https://raw.githubusercontent.com/Vermont-Labor-UI/cdn_dupe_checker/master/requirements.txt -O requirements.txt

RUN pip install -r requirements.txt

RUN npm install
RUN npm install gulp -g
