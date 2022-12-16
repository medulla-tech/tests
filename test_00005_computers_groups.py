from playwright.sync_api import  expect, Page
from common import medulla_connect, sqlcheck

import re
import configparser
import os
import time

project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')

"""
    The tests are done to test the user page of pulse.

    Test to be done:
    -> Create a group
    -> Delete a group
    -> Edit a group
        -> Add a new description to an existing group
    -> Add new machines to a group

"""
def test_create_group_based_on_name(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('#Computer-name').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Name")

    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_name = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Name'")

    normal_result = "1==glpi::Computer name==*win*"

    assert normal_result != result_on_name[0]


def test_create_group_based_on_description(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('#Description').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Description")

    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_inventory_number(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('#Inventory-number').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Inventory Number")

    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_glpi_group(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('#Group').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Glpi Group")

    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_peripheral_name(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('#Peripheral-name').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Peripheral name")

    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_peripheral_serial(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('#Peripheral-serial').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Peripheral serial")

    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_machine_type(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('#System-type').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Machine Type")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))


def test_create_group_based_on_machine_manufacturer(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="System-manufacturer"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Machine Manufacturer")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_machine_model(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="System-model"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Machine Model")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_machine_owner(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="Owner-of-the-machine"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Machine Owner")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_last_logged_user(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="Last-Logged-User"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Last Logged User")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_user_location(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="User-location"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By User location")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_location(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="Location"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Location")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_state(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="State"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By State")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_entity(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="Entity"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Entity")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_operating_system(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="Operating-system"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Operating System")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_installed_software(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="Installed-software"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Installed Software")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_software_name_and_version(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()

    page.locator('//*[@id="Installed-software--specific-version-"]').click()
    page.locator("//html/body/div/div[4]/div/div[3]/form/table/tbody/tr/td[4]/input").fill("Notepad")
    page.locator("//html/body/div/div[4]/div/div[3]/form/table/tbody/tr/td[5]/input").click()
    page.locator("//html/body/div/div[4]/div/div[3]/form/table/tbody/tr/td[6]/input").fill("0.1")
    page.locator("//html/body/div/div[4]/div/div[3]/form/table/tbody/tr/td[7]/input").click()
    page.locator("//html/body/div/div[4]/div/div[3]/table[3]/tbody/tr/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Software Name and Version")
    page.click(".btnPrimary[type='submit']")

    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_os_version(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="OS-Version"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By OS Version")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_architecture(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="Architecture"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Architecture")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_register_key(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="Register-key"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Register Key")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_register_key_value(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="Register-key-value"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.click(".btnPrimary[type='button']")
    page.locator('//*[@id="autocomplete2"]').click()
    page.locator('//*[@id="autocomplete2"]').fill("*win*")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Register Key value")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_by_OU_User(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")

    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#xmppmaster').click()
    page.locator("//html/body/div/div[4]/div/div[3]/table[2]/tbody/tr[1]/td[1]/a").click()
    page.locator("//html/body/div/div[4]/div/div[3]/form/table/tbody/tr/td[4]/input[1]").fill("test OU User")
    page.locator("//html/body/div/div[4]/div/div[3]/form/table/tbody/tr/td[4]/input[2]").click()
    page.locator("//html/body/div/div[4]/div/div[3]/table[3]/tbody/tr/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By OU User")
    page.click(".btnPrimary[type='submit']")
