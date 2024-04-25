# Spyctl API

This is a containerized version of spyctl that runs as an API server. It uses some of the code from the spyctl-cli modules
to perform some tasks that could be used by other services. For example, the spyctl api server can take http requests to
validate Spyderbat resource yaml (such as Guardian Policies).


## Python dependencies

The spyctl API runs on python 3.11 so that is a requirement

### Installing dependencies for local testing

Run `make install_test_requirements` to install the local dependencies required for unit testing without updating the requirements.txt files

### Updating requirements.txt

Edit the `requirements.in` file as needed and then run
`make update_requirements`

- This will compile two requirements files
`requirements.txt` -- this file is used by the Dockerfile to install the spyctl-cli code from this repository
`test_requirements.txt` -- this file is used for local unit testing, and is also used by github actions to run unit tests

- `requirements.txt` is a little tricky because we want the container to run with the latest local spyctl code saved to `spyctl_api/build/spyctl` but in the container the code is saved to `/spyctl`. Pip-compile builds the requirements from the `pyproject.toml` file in the local directory, then this make command changes the location that the container looks for it to be `/spyctl`. You can see this reflected in `Dockerfile`

Running `make update_requirements` will build a python virtual environment in ./spyctl_api_venv which you should set as
your interpreter if using an editor such as vscode.

