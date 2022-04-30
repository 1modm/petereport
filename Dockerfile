FROM ubuntu:20.04

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# no apt prompts
ARG DEBIAN_FRONTEND=noninteractive

# fetch package list
RUN apt-get -y update

# Make sure locale is set to UTF-8
RUN apt-get -y upgrade
RUN apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# install python
RUN apt-get -y install python3 python3-dev python3-pip

# install dependencies
RUN apt-get -y install texlive-latex-recommended texlive-fonts-extra texlive-latex-extra p7zip-full texlive-xetex
RUN apt-get -y install pipenv python3-pypandoc
RUN apt-get -y install wget
RUN apt-get -y install libpangocairo-1.0-0

# alias "python" to "python3"
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN apt-get -y install python3-gunicorn gunicorn
RUN python3 -m pip install pandoc-latex-environment

# https://github.com/dalibo/pandocker/blob/latest/alpine/Dockerfile
# Templates are installed in '/.pandoc'.
ARG TEMPLATES_DIR=/.pandoc/templates

RUN mkdir -p ${TEMPLATES_DIR} && \
    # Links for the root user
    ln -s /.pandoc /root/.pandoc

# eisvogel template
ARG EISVOGEL_REPO=https://raw.githubusercontent.com/Wandmalfarbe/pandoc-latex-template
ARG EISVOGEL_VERSION=2.0.0
RUN wget ${EISVOGEL_REPO}/v${EISVOGEL_VERSION}/eisvogel.tex -O ${TEMPLATES_DIR}/eisvogel.latex

WORKDIR /opt/petereport

COPY Pipfile ./
RUN pipenv install --system --deploy --ignore-pipfile