import json
import requests
from config import app_config


def get_app_uri():
    return f'{app_config.host}:{app_config.port}'


def get_api_uri():
    return f'{get_app_uri()}{app_config.api_base}'


def get_templates():
    return requests.get(f'{get_api_uri()}/templates')


def remove_template(tmpl_id):
    return requests.delete(f'{get_api_uri()}/templates/{tmpl_id}')


def install_template(tmpl_id):
    return requests.post(f'{get_api_uri()}/templates/{tmpl_id}/install')


def upload_template(filename=None, data=None):
    files = None
    if filename:
        files = {'file': open(filename, 'rb')}
    return requests.put(f'{get_api_uri()}/templates', files=files, data=data)


def custom_id_data(tmpl_id):
    """Returns object to send as api request data"""

    return {'data': json.dumps({'tmpl_id': tmpl_id})}