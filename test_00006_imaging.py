from playwright.sync_api import  expect, Page
import time 
import configparser
import os


project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')

def test_open_imaging(page: Page) -> None:

    page.goto(test_server)

    # We fille username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', 'siveo')
    page.click('#connect_button')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarmanage')
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

def test_open_imaging_manage_masters(page: Page) -> None:

    page.goto(test_server)

    # We fille username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', 'siveo')
    page.click('#connect_button')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.locator("//html/body/div/div[4]/div/div[1]/ul/li[2]/a").click()
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=master")

def test_open_imaging_manage_bootservices(page: Page) -> None:

    page.goto(test_server)

    # We fille username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', 'siveo')
    page.click('#connect_button')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.locator("//html/body/div/div[4]/div/div[1]/ul/li[3]/a").click()
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=service")

def test_open_imaging_manage_bootmenu(page: Page) -> None:

    page.goto(test_server)

    # We fille username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', 'siveo')
    page.click('#connect_button')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.locator("//html/body/div/div[4]/div/div[1]/ul/li[4]/a").click()
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=bootmenu")

def test_open_imaging_manage_postimaging_scripts(page: Page) -> None:

    page.goto(test_server)

    # We fille username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', 'siveo')
    page.click('#connect_button')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.locator("//html/body/div/div[4]/div/div[1]/ul/li[5]/a").click()
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=postinstall")

def test_open_imaging_configuration(page: Page) -> None:

    page.goto(test_server)

    # We fille username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', 'siveo')
    page.click('#connect_button')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.locator("//html/body/div/div[4]/div/div[1]/ul/li[6]/a").click()
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=configuration")

def test_open_imaging_manage_sysprep(page: Page) -> None:

    page.goto(test_server)

    # We fille username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', 'siveo')
    page.click('#connect_button')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.locator("//html/body/div/div[4]/div/div[1]/ul/li[7]/a").click()
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=systemImageManager")

def test_open_imaging_manage_groups(page: Page) -> None:

    page.goto(test_server)

    # We fille username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', 'siveo')
    page.click('#connect_button')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.locator("//html/body/div/div[4]/div/div[1]/ul/li[8]/a").click()
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=list_profiles")

def test_open_imaging_add_groups(page: Page) -> None:

    page.goto(test_server)

    # We fille username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', 'siveo')
    page.click('#connect_button')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarmanage')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=index")

    page.locator("//html/body/div/div[4]/div/div[1]/ul/li[9]/a").click()
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=imaging&submod=manage&action=computersprofilecreator")
