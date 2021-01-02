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
from config import app_config


def wait_for_app(trials=3):
    """Wait for application to be available for requests"""

    for i in range(trials):
        # Wait for 100 ms
        time.sleep(0.100)
        try:
            response = requests.get(api.get_app_uri())
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
    try:
        client.images.get('test_app')
    except docker.errors.ImageNotFound:
        # Building an image from dockerfile
        print('Building image from dockerfile')
        client.images.build(path='test_app/', tag='test_app:latest')

    # Run container in detach state
    app_container = client.containers.run('test_app:latest',
                                          ports={app_config.container_port: None},
                                          detach=True, remove=True)
    print(f'Container <{app_container.short_id}> created')
    app_container.reload()  # Update cached attrs
    app_config.port = int(app_container.ports[app_config.container_port][0]['HostPort'])    # Find exposed port
    # Check if application is available
    if not wait_for_app():
        raise SystemExit('Unable to reach test application')

    # Yield to use as fixture
    yield app_container

    # Teardown
    app_container.kill()


@pytest.fixture
def yaml_template(request, tmp_path):
    """Fixture which dump data to the YAML file and return its full name"""

    filename = os.path.join(tmp_path, f'{uuid.uuid4()}.yaml')
    with open(filename, 'w') as stream:
        yaml.dump(request.param, stream)
    return filename, request.param


@pytest.fixture
def uploaded_template(yaml_template):
    """Prepare template and upload to the app"""

    filename, data = yaml_template
    response = api.upload_template(filename)
    message = response.json()['message']
    tmpl_id = message[message.find('=') + 1:]
    return tmpl_id, data


@pytest.fixture
def installed_template(uploaded_template):
    """Prepare template, upload and install to the app"""

    tmpl_id, data = uploaded_template
    api.install_template(tmpl_id)
    return tmpl_id, data


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
