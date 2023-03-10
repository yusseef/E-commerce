import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
'''
@pytest.mark.selenium
def test_create_admin_user(create_admin_user):
    assert create_admin_user.__str__() == "admin"
'''
@pytest.mark.dbfixtures
def test_dashboard_admin_login(live_server, db_fixture_setup, firefox_browser_instance):

        i = User.objects.get(id=1)
        print(i.username)
        print(i.password)

        browser = firefox_browser_instance

        browser.get(("%s%s" % (live_server.url, "/admin/login")))
        username = browser.find_element(By.NAME, 'username')
        password = browser.find_element(By.NAME, 'password')
        submit = browser.find_element(By.XPATH, '//input[@value = "Log in"]')

        username.send_keys("admin")
        password.send_keys("admin")
        submit.send_keys(Keys.RETURN)

        assert "Site administration" in browser.page_source

