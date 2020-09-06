import json

import pytest
from selenium.webdriver.common.by import By

import api
import dataset

NO_TEMPLATE_XPATH = '//*[text()="No template uploaded or your template is empty..."]'


def test_no_template_installed(browser):
    browser.get(api.APP_URI)
    assert browser.title == 'Awesome Test APP'
    # No template provided
    assert browser.find_element(By.XPATH, NO_TEMPLATE_XPATH)


@pytest.mark.parametrize('yaml_template', dataset.yaml_empty_set, indirect=True)
def test_install_empty_template(yaml_template, browser):
    response = api.upload_template(yaml_template[0])
    response_json = response.json()
    message = response_json['message']
    tmpl_id = message[message.find('=') + 1:]
    api.install_template(tmpl_id)
    browser.get(api.APP_URI)
    # Template is empty
    assert browser.find_element(By.XPATH, NO_TEMPLATE_XPATH)


@pytest.mark.parametrize('yaml_template', [dataset.yaml_valid_data[1]], indirect=True)
def test_no_content_after_removing_installed_template(yaml_template, browser):
    response = api.upload_template(yaml_template[0])
    response_json = response.json()
    message = response_json['message']
    tmpl_id = message[message.find('=') + 1:]
    api.install_template(tmpl_id)
    api.remove_template(tmpl_id)
    # No template should be displayed
    assert browser.find_element(By.XPATH, NO_TEMPLATE_XPATH)


@pytest.mark.parametrize('yaml_template', dataset.yaml_valid_data, indirect=True)
def test_rendering_of_the_template(yaml_template, browser):
    tmpl_filename, tmpl_data = yaml_template
    tmpl_id = 'some-unique-id'
    api.upload_template(tmpl_filename, {'data': json.dumps({'tmpl_id': tmpl_id})})
    api.install_template(tmpl_id)
    browser.get(api.APP_URI)
    # Template with no data
    if not tmpl_data:
        assert browser.find_element(By.XPATH, NO_TEMPLATE_XPATH)
    else:
        for item in tmpl_data:
            # Check required elements
            print(f'Try to find elem with id={item["id"]}')
            page_item = browser.find_element_by_id(item['id'])
            assert page_item
            assert page_item.text == item['label']
            # Optional arguments
            if 'link' in item:
                assert page_item.get_attribute('href').startswith(item['link'])  # Trailing slash added by browser
                # Buttons on the rendered page should be clickable except case with no link provided
                assert page_item.is_enabled
            else:
                # If link is not set for element button is rendered as disabled
                assert not page_item.is_enabled
            if 'depends' in item:   # Parent element should be present in list of elements
                assert browser.find_element_by_id(item['depends'])
