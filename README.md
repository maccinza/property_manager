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

If you go with this option you only need to assure you have virtualenv installed, all the rest is resolved by the makefile.


## Running

If you went with `Option I - Using Docker`, you may run the following commands from your shell:

```
# it will build the environment if not yet build
# and run tests
$ make docker-test
```

```
# it will build the environment if not yet build
# and run the application locally
# if you run this option you'll need to wait a little time while mysql gets up and running
$ make docker-run
```

If you went with `Option II - Using local environment`, you may run the following commands from your shell:
```
# it will build the environment if not yet build
# and run tests
$ make local-test
```

```
# it will build the environment if not yet build
# and run the application locally
$ make local-run
```

When running the application, it will be available at `http://localhost:8000/admin`
There is a pre-loaded user with superuser privileges whose credentials are:

```
username: david_farrington
password: r007admpwd
```

Alongside with the user, some other fixtures are loaded for having an initial
set of objects when interacting with the solution locally.

The api endpoints are available at `http://localhost:8000/api/`. The same credentials are needed
for accessing the api.
The available api endpoints are:

- `/api/auth/login`: for requesting JWT token authentication;
- `/api/landlords`: for management of Landlords;
- `/api/tenants`: for management of Tenants;
- `/api/properties`: for management of Properties;
- `/api/contracts`: for management of Contracts;

## Tests Coverage

By running `coverage` command as following:

```
$ docker-compose run web coverage run --source="." manage.py test
$ docker-compose run web coverage report
```

It was possible to obtain the following coverage report:

```
Name                                               Stmts   Miss  Cover
----------------------------------------------------------------------
accounts/__init__.py                                   0      0   100%
accounts/admin.py                                     14      0   100%
accounts/apps.py                                       4      4     0%
accounts/migrations/0001_initial.py                    8      0   100%
accounts/migrations/0002_auto_20171001_2011.py         5      0   100%
accounts/migrations/__init__.py                        0      0   100%
accounts/models.py                                     6      0   100%
accounts/serializers.py                               23      0   100%
accounts/tests/__init__.py                             0      0   100%
accounts/tests/factories.py                           29      0   100%
accounts/tests/test_admin.py                         116      0   100%
accounts/tests/test_api_authentication.py             35      0   100%
accounts/tests/test_api_endpoints.py                 335      0   100%
accounts/tests/test_models.py                        130      2    98%
accounts/views.py                                     55      4    93%
api/__init__.py                                        0      0   100%
api/settings/__init__.py                               0      0   100%
api/settings/base.py                                  24      0   100%
api/settings/dev.py                                    3      0   100%
api/settings/local.py                                  2      2     0%
api/urls.py                                            4      0   100%
api/wsgi.py                                            4      4     0%
contracts/__init__.py                                  0      0   100%
contracts/admin.py                                    12      0   100%
contracts/apps.py                                      4      4     0%
contracts/management/__init__.py                       0      0   100%
contracts/management/commands/__init__.py              0      0   100%
contracts/management/commands/check_contracts.py      33      0   100%
contracts/management/helpers.py                       23      0   100%
contracts/migrations/0001_initial.py                   9      0   100%
contracts/migrations/__init__.py                       0      0   100%
contracts/models.py                                   32      0   100%
contracts/serializers.py                              23      0   100%
contracts/tests/__init__.py                            0      0   100%
contracts/tests/factories.py                          13      0   100%
contracts/tests/test_admin.py                         67      0   100%
contracts/tests/test_api_endpoints.py                263      0   100%
contracts/tests/test_command.py                       36      0   100%
contracts/tests/test_helpers.py                       38      0   100%
contracts/tests/test_models.py                       159      0   100%
contracts/views.py                                    64      0   100%
core/__init__.py                                       0      0   100%
core/admin.py                                          1      0   100%
core/api.py                                           13      0   100%
core/apps.py                                           4      4     0%
core/exception_handlers.py                            29      9    69%
core/exceptions.py                                    18      0   100%
core/migrations/__init__.py                            0      0   100%
core/models.py                                        29      0   100%
core/pagination.py                                    12      0   100%
core/permissions.py                                    5      1    80%
core/tests/__init__.py                                 9      0   100%
core/tests/test_models.py                             16      0   100%
core/tests/test_validators.py                         21      0   100%
core/validators.py                                     7      0   100%
core/views.py                                          1      1     0%
manage.py                                             13      6    54%
properties/__init__.py                                 0      0   100%
properties/admin.py                                   13      0   100%
properties/apps.py                                     4      4     0%
properties/migrations/0001_initial.py                  9      0   100%
properties/migrations/__init__.py                      0      0   100%
properties/models.py                                  25      0   100%
properties/serializers.py                             14      0   100%
properties/tests/__init__.py                           0      0   100%
properties/tests/factories.py                         15      0   100%
properties/tests/test_admin.py                        83      0   100%
properties/tests/test_api_endpoints.py               286      0   100%
properties/tests/test_models.py                      140      0   100%
properties/tests/test_validators.py                   19      0   100%
properties/validators.py                               8      0   100%
properties/views.py                                   68      0   100%
----------------------------------------------------------------------
TOTAL                                               2435     45    98%
```

## Solution brief description

The solution was modeled under 4 different django apps:

- `core`: which holds common data/code;
- `accounts`: which implements Landlord and Tenant models;
- `properties`: which implements Property model;
- `contracts`: which implements Contract model;

The models were designed to hold a minimal set of information to keep the challenge solution simple.

For running the mailing report command it is suggested to use a cronjob (an example of cronjob is given)
to call the management command.

It was not in the scope of this solution to present a guide or provide the tools for deploying the application.
The project structure and its settings are organized in a way that it is easy to provide different configurations for
local development, staging, production.

The application runs with `DEBUG` set to `True` locally.


## Improvements

There are lots of things to improve in the solution if we needed to use it in a real world context:

- Improve models to hold more information (e.g.: more information about landlords and tenants);
- Add validators for zip_codes, maybe using an external api;
- Implement sorting in api endpoints;
- Adding a model `ThirdPartyActor` to group thirdparty api users and be referenced by the other models.
 By doing so it would be possible to restrict each group of users to only interact with the entities they are
 related to through their `ThirdPartyActor`;
- Maybe instead of using a cronjob for running the mailing command, we could use celery + redis with a periodic task

