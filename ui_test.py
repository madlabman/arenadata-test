import pytest
from selenium.webdriver.common.by import By

import api
import dataset

NO_TEMPLATE_XPATH = '//*[text()="No template uploaded or your template is empty..."]'


def test_no_template_installed(browser):
    browser.get(api.get_app_uri())
    assert browser.title == 'Awesome Test APP'
    # No template provided
    assert browser.find_element(By.XPATH, NO_TEMPLATE_XPATH)


@pytest.mark.parametrize('yaml_template', dataset.yaml_empty_template, indirect=True)
def test_install_empty_template(uploaded_template, browser):
    tmpl_id, _ = uploaded_template
    api.install_template(tmpl_id)
    browser.get(api.get_app_uri())
    # Template is empty
    assert browser.find_element(By.XPATH, NO_TEMPLATE_XPATH)


@pytest.mark.parametrize('yaml_template', [dataset.yaml_valid_data[1]], indirect=True)
def test_no_content_after_removing_installed_template(installed_template, browser):
    tmpl_id, _ = installed_template
    api.remove_template(tmpl_id)
    # No template should be displayed
    assert browser.find_element(By.XPATH, NO_TEMPLATE_XPATH)


@pytest.mark.parametrize('yaml_template', dataset.yaml_valid_data, indirect=True)
def test_required_elements_have_to_be_presented(installed_template, browser):
    tmpl_id, tmpl_data = installed_template
    browser.get(api.get_app_uri())
    # Template with no data
    for item in tmpl_data:
        # Check required elements
        page_item = browser.find_element_by_id(item['id'])
        assert page_item
        assert page_item.text == item['label']


@pytest.mark.parametrize('yaml_template', [dataset.yaml_valid_data[1]], indirect=True)
def test_href_if_link_provided(installed_template, browser):
    tmpl_id, tmpl_data = installed_template
    browser.get(api.get_app_uri())
    for item in tmpl_data:
        page_item = browser.find_element_by_id(item['id'])
        assert page_item.get_attribute('href').startswith(item['link'])  # Trailing slash added by browser
        # Buttons on the rendered page should be clickable except case with no link provided
        assert page_item.is_enabled


@pytest.mark.parametrize('yaml_template', [dataset.yaml_valid_data[0]], indirect=True)
def test_button_without_link_has_to_be_disabled(installed_template, browser):
    tmpl_id, tmpl_data = installed_template
    browser.get(api.get_app_uri())
    for item in tmpl_data:
        page_item = browser.find_element_by_id(item['id'])
        # If link is not set for element button is rendered as disabled
        assert not page_item.is_enabled


@pytest.mark.parametrize('yaml_template', [dataset.yaml_valid_data[0]], indirect=True)
def test_item_parent_item_is_presented(installed_template, browser):
    tmpl_id, tmpl_data = installed_template
    browser.get(api.get_app_uri())
    for item in tmpl_data:
        # Parent element should be present in list of elements
        if 'depends' in tmpl_data:
            assert browser.find_element_by_id(item['depends'])
