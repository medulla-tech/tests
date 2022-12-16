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
def test_open_audit(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarxmppmaster')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=index")

def test_audit_modify_refresh(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarxmppmaster')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=index")

    page.fill('#nbs', '103')
    page.click('//*[@id="bt"]')

    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=index&refreshtime=6180000")

def test_audit_users_tasks(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarxmppmaster')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=index")
    page.click('#auditdeploy')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=auditdeploy")

def test_audit_my_team_tasks(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarxmppmaster')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=index")
    page.click('#auditteam')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=auditteam")

def test_audit_my_past_deploys(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarxmppmaster')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=index")
    page.click('#auditmypastdeploys')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=auditmypastdeploys")

def test_audit_past_deploys(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarxmppmaster')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=index")
    page.click('#auditpastdeploys')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=auditpastdeploys")

def test_audit_my_past_deploys_teams(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarxmppmaster')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=index")
    page.click('#auditmypastdeploysteam')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=auditmypastdeploysteam")
