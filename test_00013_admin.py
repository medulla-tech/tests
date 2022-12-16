from playwright.sync_api import  expect, Page
from common import medulla_connect

import configparser
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')
login = Config.get('test_server', 'login')
password = Config.get('test_server', 'password')

"""
    TODO: 
        Create a cluster
        Modify a cluster
        Modify rules order
"""

def test_open_admin(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbaradmin')
    expect(page).to_have_url( test_server + "/mmc/main.php?module=admin&submod=admin&action=relaysList")

def test_admin_clusterlist(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbaradmin')
    expect(page).to_have_url( test_server + "/mmc/main.php?module=admin&submod=admin&action=relaysList")

    page.click('#clustersList')
    expect(page).to_have_url( test_server + "/mmc/main.php?module=admin&submod=admin&action=clustersList")

def test_admin_newcluster(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbaradmin')
    expect(page).to_have_url( test_server + "/mmc/main.php?module=admin&submod=admin&action=relaysList")

    page.click('#newCluster')
    expect(page).to_have_url( test_server + "/mmc/main.php?module=admin&submod=admin&action=newCluster")

def test_admin_rules(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbaradmin')
    expect(page).to_have_url( test_server + "/mmc/main.php?module=admin&submod=admin&action=relaysList")

    page.click('#rules')
    expect(page).to_have_url( test_server + "/mmc/main.php?module=admin&submod=admin&action=rules")
