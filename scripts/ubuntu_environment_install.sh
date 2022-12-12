#!/bin/bash

set -eu -o pipefail # fail on error , debug all lines

sudo -n true
test $? -eq 0 || exit 1 "sudo privileges?"

## Update packages and Upgrade system
sudo apt-get update
sudo apt-get upgrade -y

echo '[+] Installing the environment pre-requisites'
while read -r p ; do sudo apt-get install -y $p ; done < <(cat << "EOF"
    pipenv
    pandoc
    python3-pypandoc
    cairosvg 
    python3-cairosvg
    libcairo2
    libcairo2-dev
    libpangocairo-1.0-0
    wget
EOF
)

echo '[+] Installing Eisvogel'
sleep 1

python3 -m pip install pandoc-latex-environment

if [ -d "eisvogel" ]; then
echo "Directory already exists" ;
else
`mkdir -p eisvogel`;
echo "eisvogel directory is created"
fi

cd eisvogel/
wget https://github.com/Wandmalfarbe/pandoc-latex-template/releases/download/v2.0.0/Eisvogel-2.0.0.tar.gz
tar xvfz Eisvogel-2.0.0.tar.gz
mkdir -p /home/$SUDO_USER/.pandoc/templates
cp eisvogel.latex /home/$SUDO_USER/.pandoc/templates/
