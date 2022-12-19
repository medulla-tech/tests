from playwright.sync_api import  expect, Page
from common import medulla_connect

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

    Test to be done:
    -> Create a user
    -> Delete a user
    -> Edit a user
    -> Backup a user
    -> Create a user already existing ( same name ).
    -> Modify MMC rights
"""
def test_open_users(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarusers')
    expect(page).to_have_url( test_server + "/mmc/main.php?module=base&submod=users&action=index")

def test_create_users(page: Page) -> None:

    medulla_connect(page)

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

def test_edit_users(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarusers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=users&action=index")
    page.click('.edit')

    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=users&action=edit&user=test_user")
    page.click(".btnPrimary[type='submit']")

    time.sleep(1)
    # We expect the same page as when we validate the user page we stay on it.
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=users&action=edit&user=test_user")

def test_delete_users(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarusers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=users&action=index")
    page.click('.delete > a >> nth=0')
    page.click('#delfiles')
    page.click(".btnPrimary[type='submit']")

    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=users&action=index")
