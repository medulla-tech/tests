from playwright.sync_api import  expect, Page
from common import medulla_connect, sqlcheck

import configparser
import os
import re

project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')
login = Config.get('test_server', 'login')
password = Config.get('test_server', 'password')
machineName = Config.get('test_server', 'machinename')

def test_dashboard_createuser(page: Page) -> None:

    medulla_connect(page)

    page.click("//html/body/div/div[4]/div/div[3]/div[1]/div[2]/div[1]/ul/li/a")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=users&action=add")



def test_dashboard_creategroup(page: Page) -> None:

    medulla_connect(page)

    page.click("//html/body/div/div[4]/div/div[3]/div[1]/div[2]/div[2]/ul/li/a")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=groups&action=add")

def test_create_groupe_by_dashboard_os_system(page: Page) -> None:
    medulla_connect(page)

    page.click("#os-graphs")
    expect(page).to_have_url(re.compile(".*submod=computers&action=display*"))

    page.click("#namepresence1")
    page.click(".edit a")
    expect(page).to_have_url(re.compile(".*submod=computers&action=computersgroupedit*"))

    page.fill("//html/body/div/div[4]/div/form/table/tbody/tr[1]/td[3]/input", "Group Created by playwright By Dashboard OS System")

    page.click(".btnPrimary[type='submit']")

    result_on_server = sqlcheck("dyngroup", "SELECT count(*) from Groups WHERE name = 'Group Created by playwright By Dashboard OS System'")

    assert result_on_server == 1

    locator = page.locator(".alert")
    expect(locator).to_have_class("alert alert-success")

def test_create_groupe_by_dashboard_antivirus(page: Page) -> None:
    medulla_connect(page)

    locator = page.locator(".antivirus-graphsLabel0 a")
    expect(locator).to_have_text(re.compile("OK:*"))

    page.click(".antivirus-graphsLabel0 a")
    expect(page).to_have_url(re.compile(".*submod=computers&action=display*"))

    page.click("#namepresence1")
    page.click(".edit a")
    expect(page).to_have_url(re.compile(".*submod=computers&action=computersgroupedit*"))

    page.fill("//html/body/div/div[4]/div/form/table/tbody/tr[1]/td[3]/input", "Group Created by playwright By Dashboard Antivirus")

    page.click(".btnPrimary[type='submit']")

    result_on_server = sqlcheck("dyngroup", "SELECT count(*) from Groups WHERE name = 'Group Created by playwright By Dashboard Antivirus'")

    assert result_on_server == 1

    locator = page.locator(".alert")
    expect(locator).to_have_class("alert alert-success")

def template_create_group_by_status(page: Page, selector, group_name) -> None:
    """
    It's a template to create a group of machines online or offline depending on the status available on the dashboard
    Args:
        selector: selector on which we want to click
        group_name: name of the group you want to give
    """
    page.click(selector)
    expect(page).to_have_url(re.compile(".*submod=computers&action=display*"))

    page.click("#namepresence1")
    page.click(".edit a")
    expect(page).to_have_url(re.compile(".*submod=computers&action=computersgroupedit*"))

    page.fill("//html/body/div/div[4]/div/form/table/tbody/tr[1]/td[3]/input", "Group Created by playwright By Dashboard " + group_name)

    page.click(".btnPrimary[type='submit']")

    result_on_server = sqlcheck("dyngroup", "SELECT count(*) from Groups WHERE name = 'Group Created by playwright By Dashboard " + group_name + "'")

    assert result_on_server == 1

    locator = page.locator(".alert")
    expect(locator).to_have_class("alert alert-success")

def test_create_groupe_by_dashboard_machine_online(page: Page) -> None:
    medulla_connect(page)

    status = sqlcheck("xmppmaster", "SELECT status FROM uptime_machine WHERE hostname = '" + machineName + "' ORDER BY id DESC LIMIT 1")

    if(status == 1):
        template_create_group_by_status(page, ".computersonline-graphLabel0 a", "Machine Online")
    else:
        template_create_group_by_status(page, ".computersonline-graphLabel1 a", "Machine Offline")
