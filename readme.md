# Test automation with pytest and selenium 

## Run tests

Clone this repo

```shell script
git clone --recursive https://github.com/madlabman/arenadata-test
```

Install python requirements
```shell script
pip install -r requirements.txt
```

Run scripts
```shell script
pytest
```

Note that the docker image for the application will be build at the first run.

## Troubleshooting

Make sure you have:
* `chromedriver`is available in the `PATH` environment variable
* `docker` is installed in your system and you are able to connect to the socket as normal user
* the proper timeout value is set in `conftest.py::wait_for_app` function (default `100 ms` for `3` times)
* content is presented in the git submodule `test_app`