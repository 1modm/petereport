FROM ubuntu:latest

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# No apt prompts
ARG DEBIAN_FRONTEND=noninteractive

# Fetch package list
RUN apt-get -y update
RUN apt-get -y upgrade

# Make sure locale is set to UTF-8
RUN apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Install python
RUN apt-get install -y software-properties-common 
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install -y \
  python3.8 \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

RUN apt-get -y update

# Install dependencies
RUN apt-get -y install texlive-latex-recommended texlive-fonts-extra texlive-latex-extra p7zip-full texlive-xetex
RUN apt-get -y install pipenv python3-pypandoc
RUN apt-get -y install wget
RUN apt-get -y install libpangocairo-1.0-0
ARG TARGETARCH
RUN wget https://github.com/jgm/pandoc/releases/download/2.19.2/pandoc-2.19.2-1-${TARGETARCH}.deb
RUN dpkg -i pandoc-2.19.2-1-${TARGETARCH}.deb
RUN apt-get -y install python3.8-distutils
RUN apt-get -y install python3-gunicorn gunicorn
RUN python3 -m pip install pandoc-latex-environment
RUN python3 -m pip install CairoSVG

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

RUN python -V

COPY Pipfile ./
RUN pipenv install --system --deploy --ignore-pipfile
