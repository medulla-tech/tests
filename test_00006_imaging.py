from playwright.sync_api import  expect, Page
from common import medulla_connect

import time 
import configparser
import os


project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')
login = Config.get('test_server', 'login')
password = Config.get('test_server', 'password')

def test_open_imaging(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarmanage')
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

def test_open_imaging_manage_masters(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.click('#master')
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=master")

def test_open_imaging_manage_bootservices(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.click('#service')
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=service")

def test_open_imaging_manage_bootmenu(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.click('#bootmenu')
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=bootmenu")

def test_open_imaging_manage_postimaging_scripts(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.click('#postinstall')
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=postinstall")

def test_open_imaging_configuration(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.click('#configuration')
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=configuration")

def test_open_imaging_manage_sysprep(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.click('#systemImageManager')
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=systemImageManager")

def test_open_imaging_manage_sysprep_list(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.click('#systemImageManager')
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=systemImageManager")


    page.click('#sysprepList a')

def test_open_imaging_manage_groups(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.click('#list_profiles')
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=list_profiles")

def test_open_imaging_add_groups(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.click('#computersprofilecreator')
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=computersprofilecreator")
