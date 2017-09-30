# Property Manager App
> Admin interface and API for property management

Build: [ ![Codeship Status for maccinza/property_manager](https://app.codeship.com/projects/88af9b80-8145-0135-b235-1235e5a37f40/status?branch=master)](https://app.codeship.com/projects/246904)


## Dev setup

This project was developed in a linux machine within a virtualenv with Python 2.7.13.

## Option I - Using Docker

### Prerequisites

[Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/)

#### Install docker

The development environment uses [docker](https://docs.docker.com/userguide/).
All you need is a [recent installation of docker](https://docs.docker.com/installation/#installation).

#### Install docker-compose

After getting ``docker`` installed, you'll need to get ``docker-compose`` installed
on your system; ``docker-compose`` is used to run many containers together which make
up the full system. This can be installed via [pip](https://pypi.python.org/pypi/pip):

```
$ pip install docker-compose
```

#### Configure docker

Per default the docker client needs to be run as root. This requires a tiny change to be able to
run `docker-compose` as normal user. Change the docker service to also listen for commands on tcp. For this change your `/etc/default/docker`
to include

```
DOCKER_OPTS="-H tcp://127.0.0.1:4243 -H unix:///var/run/docker.sock"
```

and run

```
$ sudo service docker restart
```

to restart ``docker``.

Now you have to export a different docker host in your shell session. To achieve this
add these line to your ``.bashrc``
```
export DOCKER_HOST=tcp://127.0.0.1:4243
```

## Option II - Using local environment

If you go with this option you don't need to be concerned about anything. You may completely rely on the provided makefile.


## Running

If you went with `Option I - Using Docker`, you may run the following commands from your shell:

```
# run tests
$ make docker-test
```

```
# run application locally
$ make docker-run
```

If you went with `Option II - Using local environment`, you may run the following commands from your shell:
```
# run tests
$ make local-test
```

```
# run application locally
$ make local-run
```

When running the application, it will be available at `http://localhost:8000/admin`
There is a pre-loaded user with superuser privileges whose credentials are:

```
username: david_farrington
password: r007admpwd
```