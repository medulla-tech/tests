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
    The tests are done to test the computer page of pulse.

    Test to be done:
    -> Open the computer page.
    -> Open all left pages
    -> Open inventory of a machine
    -> Open all actions of a machine
    -> Do a search
    -> List online/offline computers.
"""


def test_open_inventory(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")


def test_open_favouriteGroup(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#listFavourite')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=listFavourite")

def test_open_AllGroups(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#list')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=list")


def test_open_CreateGroups(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#computersgroupcreator')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")


def test_open_UninventoriedMachines(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#xmppMachinesList')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=xmppMachinesList")


def test_open_monitoringAlerts(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#alerts')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=alerts")


def test_open_customQA(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#customQA')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=customQA")

def test_open_ActionQuickGroup(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#ActionQuickGroup')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=ActionQuickGroup")


def test_open_filesmanagers(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#filesmanagers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=filesmanagers")
