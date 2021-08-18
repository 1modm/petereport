# Docker environment

`$ sudo apt install docker.io docker-compose`

## Deploy PeTeReport

1. Clone repository
`
$ cd /opt
$ git clone https://github.com/1modm/petereport
$ cd petereport
`

2. Customize reports and configuration in `config/petereport_config.py`

3. Build environment

`
$ docker-compose up --build
`

4. Go to [http://127.0.0.1/](http://127.0.0.1/)
5. Login with the default user created admin/P3t3r3p0rt or the user credentials configured in configuration file
6. Try harder
7. Create a report

## Add/Edit users

Go to [http://127.0.0.1/admin](http://127.0.0.1/admin)