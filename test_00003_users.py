from playwright.sync_api import  expect, Page
import configparser
import os
import time

project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')
login = Config.get('test_server', 'login')
password = Config.get('test_server', 'password')
"""
    The tests are done to test the user page of pulse.
    Warning: To be done correctly, it MUST be started with no users created.
"""
def test_open_users(page: Page) -> None:

    page.goto(test_server)

    # We fill username/password and we connect into the mmc.
    page.fill('#username', login)
    page.fill('#password', password)
    page.click('#connect_button')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarusers')
    expect(page).to_have_url( test_server + "/mmc/main.php?module=base&submod=users&action=index")

def test_create_users(page: Page) -> None:

    page.goto(test_server)

    # We fill username/password and we connect into the mmc.
    page.fill('#username', login)
    page.fill('#password', password)
    page.click('#connect_button')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarusers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=users&action=index")

    page.locator('#base_users_add').click()
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=users&action=add")

    page.fill('#uid', 'test_user')
    page.fill('#pass', password)
    page.fill('#confpass', password)
    page.fill('#sn', 'Familly Name')
    page.fill('#givenName', 'givenName')
    page.fill('#title', 'title')

    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=users&action=edit&user=test_user")


def test_delete_users(page: Page) -> None:

    page.goto(test_server)

    # We fill username/password and we connect into the mmc.
    page.fill('#username', login)
    page.fill('#password', password)
    page.click('#connect_button')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarusers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=users&action=index")
    page.click('//html/body/div/div[4]/div/div[2]/form/table/tbody/tr[2]/td[5]/ul/li[3]/a')
    page.click('#delfiles')
    page.click(".btnPrimary[type='submit']")

    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=users&action=index")
