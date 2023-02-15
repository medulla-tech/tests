from playwright.sync_api import  expect, Page
from common import medulla_connect, sqlcheck

import configparser
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')
login = Config.get('test_server', 'login')
password = Config.get('test_server', 'password')

user_rule = "user"

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

def test_admin_rules_up(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbaradmin')
    expect(page).to_have_url( test_server + "/mmc/main.php?module=admin&submod=admin&action=relaysList")

    page.click('#rules')
    expect(page).to_have_url( test_server + "/mmc/main.php?module=admin&submod=admin&action=rules")

    sql_request = "SELECT level FROM rules WHERE name='%s'" % user_rule
    level_before = sqlcheck("xmppmaster", sql_request)

    page.click("#cr_" + user_rule + " .up a")

    level_after = sqlcheck("xmppmaster", sql_request)

    assert level_after < level_before

def test_admin_rules_down(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbaradmin')
    expect(page).to_have_url( test_server + "/mmc/main.php?module=admin&submod=admin&action=relaysList")

    page.click('#rules')
    expect(page).to_have_url( test_server + "/mmc/main.php?module=admin&submod=admin&action=rules")

    sql_request = "SELECT level FROM rules WHERE name='%s'" % user_rule
    level_before = sqlcheck("xmppmaster", sql_request)

    page.click("#cr_" + user_rule + " .down a")

    level_after = sqlcheck("xmppmaster", sql_request)

    assert level_after > level_before

def test_admin_create_cluster(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbaradmin')
    expect(page).to_have_url( test_server + "/mmc/main.php?module=admin&submod=admin&action=relaysList")

    page.click('#newCluster')
    expect(page).to_have_url( test_server + "/mmc/main.php?module=admin&submod=admin&action=newCluster")

    page.fill('#cluster_name', 'Cluster Created by playwright To be deleted')
    page.fill('#cluster_description', 'Cluster Created by playwright Description')

    page.locator("#outCluster li >> nth=0").drag_to(
        page.locator("#inCluster")
    )
    page.click(".btnPrimary[type='submit']")

    # To check if the cluster is created, we check if the locator is present
    locator = page.locator(".alert")
    expect(locator).to_have_class("alert alert-success")
