import pytest

from selenium import webdriver
from selenium.webdriver.firefox.options import Options



@pytest.fixture(scope = 'module')
def firefox_browser_instance(request):
    options = Options()
    options.headless = False
    browser= webdriver.Firefox(options = options)
    yield browser
    browser.close()
