# Enasis Network Homie Automate

> :children_crossing: This project has not released its first major version.

Define desired scenes for groups using flexible conditional plugins.

[![](https://img.shields.io/github/actions/workflow/status/enasisnetwork/enhomie/build.yml?style=flat-square&label=GitHub%20actions)](https://github.com/enasisnetwork/enhomie/actions)<br>
[![codecov](https://img.shields.io/codecov/c/github/enasisnetwork/enhomie?token=7PGOXKJU0E&style=flat-square&logoColor=FFFFFF&label=Coverage)](https://codecov.io/gh/enasisnetwork/enhomie)<br>
[![](https://img.shields.io/readthedocs/enhomie?style=flat-square&label=Read%20the%20Docs)](https://enhomie.readthedocs.io)<br>
[![](https://img.shields.io/pypi/v/enhomie.svg?style=flat-square&label=PyPi%20version)](https://pypi.org/project/enhomie)<br>
[![](https://img.shields.io/pypi/dm/enhomie?style=flat-square&label=PyPi%20downloads)](https://pypi.org/project/enhomie)

## Configuration example
Some basic configuration examples. See next section for more documentation.
- [Homie Desires](enhomie/homie/test/samples/desires.yml)
- [Homie Groups](enhomie/homie/test/samples/groups.yml)
- [Homie Scenes](enhomie/homie/test/samples/scenes.yml)
- [Philips Hue Bridges](enhomie/philipshue/test/samples/bridges.yml)
- [Philips Hue Devices](enhomie/philipshue/test/samples/devices.yml)
- [Ubiquiti Routers](enhomie/ubiquiti/test/samples/routers.yml)
- [Ubiquiti Clients](enhomie/ubiquiti/test/samples/clients.yml)

## Documentation
Documentation is on [Read the Docs](https://enhomie.readthedocs.io).
Should you venture into the sections below you will be able to use the
`sphinx` recipe to build documention in the `docs/html` directory.

## Additional scripts
- [dumper.py](desired.py) is useful for setting desired scenes.
- [dumper.py](dumper.py) is useful for dumping configuration.
- [scener.py](scener.py) is useful for setting scene on groups.

## Useful and related links
- https://ubntwiki.com/products/software/unifi-controller/api

## Installing the package
Installing stable from the PyPi repository
```
pip install enhomie
```
Installing latest from GitHub repository
```
pip install git+https://github.com/enasisnetwork/enhomie
```

## Quick start for local development
Start by cloning the repository to your local machine.
```
git clone https://github.com/enasisnetwork/enhomie.git
```
Set up the Python virtual environments expected by the Makefile.
```
make -s venv-create
```

### Execute the linters and tests
The comprehensive approach is to use the `check` recipe. This will stop on
any failure that is encountered.
```
make -s check
```
However you can run the linters in a non-blocking mode.
```
make -s linters-pass
```
And finally run the various tests to validate the code and produce coverage
information found in the `htmlcov` folder in the root of the project.
```
make -s pytest
```

## Build and upload to PyPi
Build the package.
```
make -s pypackage
```
Upload to the test PyPi.
```
make -s pypi-upload-test
```
Upload to the prod PyPi.
```
make -s pypi-upload-prod
```
