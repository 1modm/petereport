
# Django installation

## Environment

**Easiest way in Linux (ubuntu):** `sudo bash doc/ubuntu_environment_install.sh`

### Pipenv

**Linux:** `$ sudo apt-get install pipenv`

**pip:** `$ python3 -m pip install pipenv`

**MAC:** `$ brew install pipenv`

### Latex

**Linux:**
`$ sudo apt-get install texlive-full`

**Mac:**
`$ brew remove basictex`

`$ brew cask install mactex`

### Pandoc

https://pandoc.org/installing.html

**Linux:**
`$ sudo apt-get install pandoc`

`$ sudo apt-get install python3-pypandoc`

**Mac:**
`$ brew install pandoc`

`$ brew install pandoc-citeproc`

### Eisvogel

`$ python3 -m pip install pandoc-latex-environment`

https://github.com/Wandmalfarbe/pandoc-latex-template

1. Download the latest version of the Eisvogel template from the release page.
2. Extract the downloaded ZIP archive and open the folder.
3. Move the template eisvogel.tex to your pandoc templates folder and rename the file to eisvogel.latex. The location of the templates folder depends on your operating system: `/Users/$USER/.pandoc/templates/eisvogel.latex` or `/home/$USER/.pandoc/templates`


# PeTeReport 

**Python 3.8 Required**

1. Clone the project and cd into PeTeReport: `cd petereport/`
2. Create a new virtual environment and installing dependencies: `pipenv install`
3. Run the virtual environment: `pipenv shell`
4. Go to Django PeTeReport: `cd django/`
5. Create the database: `python manage.py migrate`
6. Make the latest database changes: `python manage.py makemigrations`
7. Super user admin/P3t3r3p0rt will be created, but you can create a new super user: `python manage.py createsuperuser`
8. Populate the CWE data `python manage.py loaddata config/cwe-list.json`


## Start the server

1. Run the virtual environment: `pipenv shell`
2. Go to Django PeTeReport: `cd django/`
3. Start the django server: `python manage.py runserver` or `python manage.py runserver 0.0.0.0:8000`
4. Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
5. Login with the default user created admin/P3t3r3p0rt or the user credentials configured in the configuration file
6. Try harder
7. Create a report
8. Close up and stop the server: `Ctrl + C`


## Upgrade PeTeReport 

1. Stop the server if it's running: `Ctrl + C`
2. Pull the latest code base via git: `git pull` or download the source and replace the files.
3. Setup any additional dependencies: `pipenv install`
4. Run the virtual environment: `pipenv shell`
5. Make the latest database changes: `python manage.py makemigrations`
6. Make the latest database changes: `python manage.py migrate`
7. Start the server: `python manage.py runserver`
8. Try harder again


## Clean PeTeReport

1. Stop the server if it's running: `Ctrl + C`
2. Run the virtual environment: `pipenv shell`
3. Go to Django PeTeReport: `cd django/`
4. Run cleaner: `python clean.py`
5. Make the latest database changes: `python manage.py makemigrations`
6. Make the latest database changes: `python manage.py migrate`
7. Start the server: `python manage.py runserver`
8. Try harder again


## Configuration

1. Stop the server if it's running: `Ctrl + C`
2. Customize reports and configuration in `config/petereport_config.py`
3. Start the django server: `python manage.py runserver` or `python manage.py runserver 0.0.0.0:8000`

