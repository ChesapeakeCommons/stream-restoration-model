# FieldDoc.io

## Getting Started

### Setup the Application

The FieldDoc platform is a Python based application. We will need to use
several non-standard Python packages. To use these packages with our application
we must install these within an application specific virtual environment.

#### Create Your Virtual Environment

```
virtualenv venv
```

#### Activiate Your Virtual Enviornment

```
source venv/bin/activate
```

#### Install FieldDoc Dependencies

```
pip install -r requirements.txt
```

### Create and Configure a Database

In order for the application to run we will need to create a PostgreSQL database.

```
CREATE DATABASE <string:databaseName>;
```

The FieldDoc platform also takes advantage of the PostgreSQL extension called
PostGIS for enhanced geospatial operations.

```
CREATE EXTENSION postgis;
```

### Starting the Application

```
python runserver.py --enviornment=[CONFIG_ENVIRONMENT]
```

#### Help starting the Application
Formatting the CONFIG_ENVIRONMENT variables is made of two parts.

1. The name of the file in the `app/config` directory you wish to use
(e.g., development.py would be development)
2. The name of the class you wish to execute against (e.g., DevelopmentConfig)

In this example our command would look like the following:

```
python runserver.py --environment="development.DevelopmentConfig"
```

## Contributor Guidelines

We welcome project contributions including functionality proposals, bug and
security fixes, and increased performance. When contributing to this project we
ask that you take a couple of things into consideration.

### Functionality Proposals

When proposing new functionality please follow the guidelines below:

1. Prior to submitting new functionality in the form of code changes or Pull
Reqeusts, please open an issue and discuss it with community. Often times you
will discover that others have similar ideas. Occasionally your new functionality
or some version of it, may already be part of our development roadmap.
2. If your new functionality does not exist please open an Issue within the
projects Github account.
3. If your new functionality is similar to other request functionality please
make sure to reference the possible similar functionality by referening the
Milestone or Issue # in your New Issue.
4. Once vetted by project contributors, a Github Milestone will be created
within the project directory.
5. At that point you may submit specific tasks via Issues to guide your
development progress and open up possible contributions from the community.
6. Please install the `pep8` Python package and execute it against your project.
https://pypi.python.org/pypi/pep8. Please ensure that the `pep8` tests pass for
your project prior to submitting a Pull Request. Failing pep8 tests will result
in additional Issues for your Milestone and a rejected Pull Request.

Our QA/QC Review Board will at minimum run the following PEP8 test against your
code, and then again prior to making a Release available to the public:

```
pep8 . --exclude=tests,venv,docs,.git -v
```

```
pep257 .
```

7. Once you feel your new functionality is ready for review by the project's
QA/QC Review Board.
8. The board may ask for additional information regarding your functionality and
in some cases further revisions. Please be prepared to submit fixes and
ammendments to your functionality in a timely fashion.

### Submitting Bug Fixes

Bug fix guidelines currently in-development

### Submitting Security and Performance Patches

Security and Perforamnce patching guidelines currently in-development
