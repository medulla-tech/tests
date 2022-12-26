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
TestGroup_Name = "Nom_Du_groupe_de_test"

def test_open_groups(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbargroups')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=groups&action=index")


def test_create_groups(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbargroups')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=groups&action=index")

    page.click('#add')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=groups&action=add")

    page.fill('#groupname', TestGroup_Name)
    page.fill('#groupdesc', 'Description du groupe')
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=groups&action=index")

def test_display_groups(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbargroups')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=groups&action=index")

    machine_inventory = "#g_" + TestGroup_Name + " .display a"
    page.click(machine_inventory)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=groups&action=members&group=" + TestGroup_Name)


def test_edit_groups(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbargroups')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=groups&action=index")

    machine_inventory = "#g_" + TestGroup_Name + " .edit a"
    page.click(machine_inventory)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=groups&action=edit&group=" + TestGroup_Name)

def test_delete_groups(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbargroups')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=groups&action=index")

    machine_inventory = "#g_" + TestGroup_Name + " .delete a"
    page.click(machine_inventory)
    page.click(".btnPrimary[type='submit']")

    locator = page.locator(".alert")
    expect(locator).to_have_class("alert alert-success")
