import json
import uuid

import pytest

import api
import dataset


def test_no_templates_at_startup():
    response = api.get_templates()
    assert response.status_code == 200  # Everything should be ok
    response_json = response.json()
    assert not response_json['templates']


def test_cannot_remove_non_existent_template():
    tmpl_id = str(uuid.uuid4())[:3]  # Generate unique id
    response = api.remove_template(tmpl_id)
    assert response.status_code == 404  # Should be not found
    response_json = response.json()
    assert response_json['message'] == f'No template with tmpl_id={tmpl_id} found!'


def test_cannot_install_non_existent_template():
    tmpl_id = str(uuid.uuid4())[:3]  # Generate unique id
    response = api.install_template(tmpl_id)
    assert response.status_code == 404  # Should be not found
    response_json = response.json()
    assert response_json['message'] == f'No template with tmpl_id={tmpl_id} found!'


def test_upload_without_template():
    response = api.upload_template()
    assert response.status_code == 400  # Bad request
    response_json = response.json()
    assert response_json['message'] == 'No file part in the request'


@pytest.mark.parametrize('yaml_template', dataset.yaml_empty_set, indirect=True)
def test_upload_template_without_data(yaml_template):
    response = api.upload_template(yaml_template[0])
    assert response.status_code == 201  # Created HTTP code
    response_json = response.json()
    assert response_json['message'].startswith('Template successfully uploaded.')
    message = response_json['message']
    tmpl_id = message[message.find('=') + 1:]
    # Check list of templates
    response = api.get_templates()
    assert response.status_code == 200  # Everything should be ok
    response_json = response.json()
    assert tmpl_id in response_json['templates']


@pytest.mark.parametrize('yaml_template', dataset.yaml_empty_set, indirect=True)
def test_upload_template_with_custom_id(yaml_template):
    response = api.upload_template(yaml_template[0], {'data': json.dumps({'tmpl_id': 'my_custom_id'})})
    assert response.status_code == 201  # Created HTTP code
    response_json = response.json()
    assert response_json['message'].startswith('Template successfully uploaded.')
    message = response_json['message']
    tmpl_id = message[message.find('=') + 1:]
    assert tmpl_id == 'my_custom_id'
    # Check list of templates
    response = api.get_templates()
    assert response.status_code == 200  # Everything should be ok
    response_json = response.json()
    assert tmpl_id in response_json['templates']


@pytest.mark.parametrize('yaml_template', dataset.yaml_empty_set, indirect=True)
def test_upload_templates_with_the_same_custom_ids(yaml_template):
    response = api.upload_template(yaml_template[0], {'data': json.dumps({'tmpl_id': 'my_custom_id'})})
    assert response.status_code == 201  # Created HTTP code
    response = api.upload_template(yaml_template[0], {'data': json.dumps({'tmpl_id': 'my_custom_id'})})
    assert response.status_code == 500  # Should not be added


@pytest.mark.parametrize('yaml_template', dataset.yaml_empty_set, indirect=True)
def test_upload_template_with_id_of_previously_uploaded_template(yaml_template):
    response = api.upload_template(yaml_template[0])
    response_json = response.json()
    message = response_json['message']
    tmpl_id = message[message.find('=') + 1:]
    response = api.upload_template(yaml_template[0], {'data': json.dumps({'tmpl_id': tmpl_id})})
    assert response.status_code == 500  # Should not be added


@pytest.mark.parametrize('yaml_template', dataset.yaml_invalid_data, indirect=True)
def test_install_invalid_template(yaml_template):
    response = api.upload_template(yaml_template[0])
    assert response.status_code == 201  # Created HTTP code
    response_json = response.json()
    message = response_json['message']
    tmpl_id = message[message.find('=') + 1:]
    response = api.install_template(tmpl_id)
    assert response.status_code == 500  # Invalid template
    # response_json = response.json()
    # assert response_json
    # assert response_json['message'] == 'Invalid template format!'


@pytest.mark.parametrize('yaml_template', dataset.yaml_valid_data, indirect=True)
def test_install_valid_template(yaml_template):
    response = api.upload_template(yaml_template[0])
    assert response.status_code == 201  # Created HTTP code
    response_json = response.json()
    message = response_json['message']
    tmpl_id = message[message.find('=') + 1:]
    response = api.install_template(tmpl_id)
    assert response.status_code == 200  # Should be ok
    response_json = response.json()
    assert tmpl_id in response_json['message']
    assert response_json['message'].endswith('successfully installed!')


@pytest.mark.parametrize('yaml_template', dataset.yaml_empty_set, indirect=True)
def test_remove_uploaded_template(yaml_template):
    response = api.upload_template(yaml_template[0])
    assert response.status_code == 201  # Created HTTP code
    response_json = response.json()
    message = response_json['message']
    tmpl_id = message[message.find('=') + 1:]
    # Make sure that item exists
    response = api.get_templates()
    assert response.status_code == 200  # Everything should be ok
    response_json = response.json()
    assert tmpl_id in response_json['templates']
    # Remove template
    response = api.remove_template(tmpl_id)
    assert response.status_code == 200  # Should be ok
    # List of templates should be empty
    response = api.get_templates()
    assert response.status_code == 200  # Everything should be ok
    response_json = response.json()
    assert not response_json['templates']