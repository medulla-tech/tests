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

def test_dashboard_createuser(page: Page) -> None:

    medulla_connect(page)

    page.click("//html/body/div/div[4]/div/div[3]/div[1]/div[2]/div[1]/ul/li/a")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=users&action=add")



def test_dashboard_creategroup(page: Page) -> None:

    medulla_connect(page)

    page.click("//html/body/div/div[4]/div/div[3]/div[1]/div[2]/div[2]/ul/li/a")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=groups&action=add")


