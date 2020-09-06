import os
import time
import uuid

import docker
import docker.errors
import pytest
import requests
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import api


def wait_for_app(trials=3):
    """Wait for application to be available for requests"""

    for i in range(0, trials):
        # Wait for 100 ms
        time.sleep(0.100)
        try:
            response = requests.get(api.APP_URI)
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            # It is expected, ignore
            pass
    return False


@pytest.fixture(scope='function', autouse=True)
def docker_container():
    """Fixture which run docker container with test application"""

    # Print new line for readability
    print()

    # Connecting to the docker client
    client = docker.from_env()

    # If an image with name test_app is not presented
    if not client.images.list(name='test_app'):
        # Building an image from dockerfile
        print('Building image from dockerfile')
        client.images.build(path='test_app/', tag='test_app:latest')

    # Run container in detach state
    app_container = client.containers.run('test_app:latest', ports={'5000/tcp': 5000}, detach=True)
    print(f'Container <{app_container.short_id}> created')

    # Check if application is available
    if not wait_for_app():
        raise SystemExit('Unable to reach test application')

    # Yield to use as fixture
    yield app_container

    # Teardown
    app_container.kill()
    client.containers.prune()


@pytest.fixture
def yaml_template(request, tmp_path):
    """Fixture which dump data to the YAML file and return its full name"""

    filename = f'{tmp_path}{os.sep}{uuid.uuid4()}.yaml'
    stream = open(filename, 'w')
    yaml.dump(request.param, stream)
    return filename, request.param


@pytest.fixture
def browser():
    """Fixture for selenium support"""

    chrome_opt = Options()
    chrome_opt.headless = True
    # Note: make sure you have chromedriver in the PATH environment variable
    driver = webdriver.Chrome(options=chrome_opt)
    driver.maximize_window()
    yield driver
    # Teardown
    driver.quit()
