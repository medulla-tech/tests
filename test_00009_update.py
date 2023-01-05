from playwright.sync_api import  expect, Page
from common import medulla_connect, sqlcheck

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

def test_open_details_by_updates(page: Page) -> None:
    medulla_connect(page)

    page.click("#navbarupdates")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=updates&submod=updates&action=index")

    page.click(".auditbyupdate a")

    time.sleep(1)
    locator = page.locator("#__popup_container")
    expect(locator).to_be_hidden()

    expect(page).to_have_url(re.compile(".*module=updates&submod=updates&action=detailsByUpdates*"))

def test_open_details_by_updateall(page: Page) -> None:
    medulla_connect(page)

    page.click("#navbarupdates")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=updates&submod=updates&action=index")

    page.click(".updateall a")

    time.sleep(1)
    locator = page.locator("#__popup_container")
    expect(locator).to_be_hidden()

    expect(page).to_have_url(re.compile(".*module=updates&submod=updates&action=deployAllUpdates*"))

def test_deploy_specific_update(page: Page) -> None:
    medulla_connect(page)

    page.click("#navbarupdates")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=updates&submod=updates&action=index")

    page.click(".updateone a")
    page.click(".quick a")

    time.sleep(1)
    locator = page.locator("#__popup_container")
    expect(locator).to_be_hidden()

    expect(page).to_have_url(re.compile(".*module=updates&submod=updates&action=deploySpecificUpdate*"))

def test_enable_update(page: Page) -> None:
    medulla_connect(page)

    page.click("#navbarupdates")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=updates&submod=updates&action=index")

    page.click("#updatesListWin a")

    time.sleep(1)
    updateid = page.locator(".listinfos .alternate >> nth=0").get_attribute("id")

    def check_enable_update(page: Page, selctor, updateid):
        """
            It's a function to check if the update is enabled or not.
        Args:
            page (Page): The page to check
            selector : Css selector of the update to check to know statut of the update
            updateid : The id of the update to check
        """
        if(page.locator(selctor).get_attribute("class") == "enableupdateg"):
            page.click("#" + updateid + " a")
            updateid = updateid[2:]

            result_on_server = sqlcheck("xmppmaster", "SELECT valided FROM up_gray_list WHERE updateid = '" + updateid + "'")

            assert result_on_server == 1

            expect(page).to_have_url(re.compile(".*module=updates&submod=updates&action=updatesListWin*"))

        else:
            page.click("#" + updateid + " a")
            updateid = updateid[2:]

            result_on_server = sqlcheck("xmppmaster", "SELECT valided FROM up_gray_list WHERE updateid = '" + updateid + "'")

            locator = (page.locator(".alert"))
            expect(locator).to_have_class("alert alert-success")
            assert result_on_server == 1

            expect(page).to_have_url(re.compile(".*module=updates&submod=updates&action=updatesListWin*"))

    check_enable_update(page, "//html/body/div/div[4]/div/div[2]/form/table/tbody/tr[1]/td[4]/ul/li[1]", updateid)
