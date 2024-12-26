from playwright.sync_api import  expect, Page
from common import medulla_connect, sqlcheck, get_an_available_update, is_update_activated, get_an_activated_update, is_update_whitelisted, get_a_greylist_update

import configparser
import os
import re
import time

project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')
login = Config.get('test_server', 'login')
password = Config.get('test_server', 'password')

"""
    The tests are done to test the update page of pulse.

    Test to be done:
    -> Open all actions of a machine
    -> Deploy specific update
    -> Enable update
    -> Disable update
"""

def test_open_update(page: Page) -> None:
    medulla_connect(page)

    page.click("#navbarupdates")

    time.sleep(1)
    locator = page.locator("#__popup_container")
    expect(locator).to_be_hidden()

    expect(page).to_have_url(test_server + "/mmc/main.php?module=updates&submod=updates&action=index")

def test_open_details_by_machines(page: Page) -> None:
    medulla_connect(page)

    page.click("#navbarupdates")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=updates&submod=updates&action=index")

    page.click(".auditbymachine a")

    time.sleep(1)
    locator = page.locator("#__popup_container")
    expect(locator).to_be_hidden()

    expect(page).to_have_url(re.compile(".*module=updates&submod=updates&action=detailsByMachines*"))

#def test_deploy_specific_update(page: Page) -> None:
#    medulla_connect(page)
#
#    page.click("#navbarupdates")
#    expect(page).to_have_url(test_server + "/mmc/main.php?module=updates&submod=updates&action=index")
#
#    page.click(".updateone a")
#    page.click(".quick a")
#
#    time.sleep(1)
#    locator = page.locator("#__popup_container")
#    expect(locator).to_be_hidden()
#
#    expect(page).to_have_url(re.compile(".*module=updates&submod=updates&action=deploySpecificUpdate*"))


def test_enable_update(page: Page) -> None:
    medulla_connect(page)

    page.click("#navbarupdates")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=updates&submod=updates&action=index")

    page.click("#updatesListWin a")

    availableUpdate = get_an_available_update()

    ActivateUpdate = "#u_" + availableUpdate + " > td.action > ul > li.enableupdate > a"
    page.click(ActivateUpdate)

    locator = (page.locator(".alert"))
    expect(locator).to_have_class("alert alert-success")

    isUpdateActivated = is_update_activated(availableUpdate)

    assert isUpdateActivated == 1


def test_disable_update(page: Page) -> None:
    medulla_connect(page)

    page.click("#navbarupdates")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=updates&submod=updates&action=index")

    page.click("#updatesListWin a")

    availableUpdate = get_an_activated_update()

    ActivateUpdate = "#u_" + availableUpdate + " > td.action > ul > li.disableupdate > a"
    page.click(ActivateUpdate)


    page.click(".btnPrimary[type='submit']")

    isUpdateActivated = is_update_activated(availableUpdate)

    assert isUpdateActivated == 0


#def test_add_whitelist_update(page: Page) -> None:
#    medulla_connect(page)
#    
#    page.click("#navbarupdates")
#    expect(page).to_have_url(test_server + "/mmc/main.php?module=updates&submod=updates&action=index")
#    
#    page.click("#updatesListWin a")
#    
#    availableUpdate = get_a_greylist_update()
#    
#    ActivateUpdate = "#u_" + availableUpdate + " > td.action > ul > li.approveupdate > a"
#    page.click(ActivateUpdate)
#    
#
#    isUpdateWhiteListed = is_update_whitelisted(availableUpdate)
#    
#    assert isUpdateWhiteListed == 0


def test_remove_whitelist_update(page: Page) -> None:
    medulla_connect(page)

    page.click("#navbarupdates")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=updates&submod=updates&action=index")

    page.click("#updatesListWin a")

    availableUpdate = get_an_available_update()

    ActivateUpdate = "#u_" + availableUpdate + " > td.action > ul > li.approveupdate > a"
    page.click(ActivateUpdate)

    page.click(".btnPrimary[type='submit']")

    isUpdateWhiteListed = is_update_whitelisted(availableUpdate)

    assert isUpdateWhiteListed == 1
