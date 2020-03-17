FROM mcr.microsoft.com/dotnet/core/sdk:2.1 AS build

# Nodejs
ENV NODE_VERSION 12.13.0
ENV NODE_DOWNLOAD_SHA c69671c89d0faa47b64bd5f37079e4480852857a9a9366ee86cdd8bc9670074a

RUN curl -SL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.gz" --output nodejs.tar.gz \
    && echo "$NODE_DOWNLOAD_SHA nodejs.tar.gz" | sha256sum -c - \
    && tar -xzf "nodejs.tar.gz" -C /usr/local --strip-components=1 \
    && rm nodejs.tar.gz \
    && ln -s /usr/local/bin/node /usr/local/bin/nodejs

RUN echo $("help")

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


COPY ./bannedversions.json /data/
COPY ./versionchecker.py /data/
COPY ./requirements.txt /data/
COPY ./post_restore.py /data

RUN pip install -r /data/requirements.txt
