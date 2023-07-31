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
    The tests are done to test the service page of pulse.
"""
def test_open_services(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcontrol')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=services&submod=control&action=index"
    )


def test_open_services_others(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcontrol')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=services&submod=control&action=index"
    )
    page.click('#others')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=services&submod=control&action=others"
    )
 


def test_open_services_log(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcontrol')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=services&submod=control&action=index"
    )
    page.click('#log')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=services&submod=control&action=log"
    )



