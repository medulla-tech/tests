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
    -> Create a group
    -> Delete a group
    -> Edit a group -> Will need IDs
    -> Create group with an already existing name
"""
def test_open_groups(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbargroups')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=groups&action=index")


def test_create_groups(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbargroups')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=groups&action=index")

    page.click('//html/body/div/div[4]/div/div[1]/ul/li[2]/a')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=groups&action=add")

    page.fill('#groupname', 'Nom_Du_groupe_de_test')
    page.fill('#groupdesc', 'Description du groupe')
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=groups&action=index")

