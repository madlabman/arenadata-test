import requests

APP_URI = 'http://localhost:5000'
API_BASE = 'http://localhost:5000/api/v1'


def get_templates():
    return requests.get(f'{API_BASE}/templates')


def remove_template(tmpl_id):
    return requests.delete(f'{API_BASE}/templates/{tmpl_id}')


def install_template(tmpl_id):
    return requests.post(f'{API_BASE}/templates/{tmpl_id}/install')


def upload_template(filename=None, data=None):
    files = None
    if filename:
        files = {'file': open(filename, 'rb')}
    return requests.put(f'{API_BASE}/templates', files=files, data=data)
