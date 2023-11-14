FROM debian:stable-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# No apt prompts
ARG DEBIAN_FRONTEND=noninteractive

# Fetch package list
RUN apt -y update
RUN apt -y upgrade

# Make sure locale is set to UTF-8
RUN apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Install dependencies
RUN apt -y install wget
RUN apt -y install texlive-latex-recommended texlive-fonts-extra texlive-latex-extra p7zip-full texlive-xetex
RUN apt -y install python3-minimal python3-pypandoc
RUN apt -y install libpangocairo-1.0-0
RUN apt -y install python3-distutils
RUN apt -y install pipenv
RUN apt -y purge python3-gunicorn gunicorn

ARG TARGETARCH
ARG PANDOC_VERSION=3.1.9
RUN wget https://github.com/jgm/pandoc/releases/download/${PANDOC_VERSION}/pandoc-${PANDOC_VERSION}-1-${TARGETARCH}.deb
RUN dpkg -i pandoc-${PANDOC_VERSION}-1-${TARGETARCH}.deb && rm -f pandoc-${PANDOC_VERSION}-1-${TARGETARCH}.deb

ENV OSFONTDIR=/usr/share/fonts
RUN fc-cache --really-force --verbose

# https://github.com/dalibo/pandocker/blob/latest/alpine/Dockerfile
# Templates are installed in '/.pandoc'.
#ARG TEMPLATES_DIR=/.pandoc/templates

#RUN mkdir -p ${TEMPLATES_DIR} && \
    # Links for the root user
#    ln -s /.pandoc /root/.pandoc

# eisvogel template
#ARG EISVOGEL=https://github.com/Wandmalfarbe/pandoc-latex-template/raw/master/eisvogel.tex
#RUN wget ${EISVOGEL} -O ${TEMPLATES_DIR}/eisvogel.latex

WORKDIR /opt/petereport

RUN python3 --version

COPY Pipfile ./
RUN pipenv install --deploy --ignore-pipfile --python 3.11

RUN apt -y purge wget

# Final Debian Update
RUN apt -y update
RUN apt -y upgrade
RUN apt -y clean
RUN apt -y autoremove