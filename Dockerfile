FROM debian:stable-slim

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

# Install dependencies
RUN apt-get -y install texlive-latex-recommended texlive-fonts-extra texlive-latex-extra p7zip-full texlive-xetex
RUN apt-get -y install python3-minimal python3-pypandoc
RUN apt-get -y install pipenv
RUN apt-get -y install wget
RUN apt-get -y install libpangocairo-1.0-0
RUN apt-get -y install python3-distutils
RUN apt -y purge python3-gunicorn gunicorn

ARG TARGETARCH
RUN wget https://github.com/jgm/pandoc/releases/download/3.1.6.2/pandoc-3.1.6.2-1-${TARGETARCH}.deb
RUN dpkg -i pandoc-3.1.6.2-1-${TARGETARCH}.deb && rm -f pandoc-3.1.6.2-1-${TARGETARCH}.deb

WORKDIR /opt/petereport

RUN python3 --version

COPY Pipfile ./
RUN pipenv install --deploy --ignore-pipfile --python 3.11

RUN apt -y clean
RUN apt -y autoremove