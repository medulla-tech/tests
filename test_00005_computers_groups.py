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
GroupTest = "Group_Test"

"""
    The tests are done to test the user page of pulse.

    Test to be done:
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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill(GroupTest)

    page.click(".btnPrimary[type='submit']")

def test_create_duplicate_group_based_on_name(page: Page) -> None:

    """
        We create a dupplicate group ( the same as the previous test.
        We only allow one group with a name.
        We expect to obtain an error pop-up
    """
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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill(GroupTest)

    page.click(".btnPrimary[type='submit']")

    locator = page.locator('#__popup_container .alert.alert-error')
    wanted_sentence = "A group already exists with name '%s'" % GroupTest
    expect(locator).to_have_text(wanted_sentence)

def test_groups_list_from_name(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#list')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=list")

    # Ajouter le nom du groupe via SQL
    page.click("#g_" + GroupTest + " a")
    expect(page).to_have_url(re.compile(".*action=display*"))

def test_groups_display_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#list')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=list")

    # Ajouter le nom du groupe via SQL
    page.click("#g_" + GroupTest +  " .display a")
    expect(page).to_have_url(re.compile(".*action=display*"))

def test_groups_edit_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#list')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=list")

    # Ajouter le nom du groupe via SQL
    page.click("#g_" + GroupTest + " .edit a")
    expect(page).to_have_url(re.compile(".*computersgroupedit*"))

def test_groups_share_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#list')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=list")

    # Ajouter le nom du groupe via SQL
    page.click("#g_" + GroupTest + " .groupshare a")
    expect(page).to_have_url(re.compile(".*edit_share*"))

def test_groups_install_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#list')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=list")

    # Ajouter le nom du groupe via SQL
    page.click("#g_" + GroupTest + " .install a")
    expect(page).to_have_url(re.compile(".*action=groupmsctabs*"))

def test_groups_delete_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#list')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=list")

    # Ajouter le nom du groupe via SQL
    page.click("#g_" + GroupTest + " .delete a")
    page.click(".btnPrimary[type='submit']")


    result_on_server = sqlcheck("dyngroup", "SELECT count(*) FROM Groups WHERE name = 'Group_Test'")

    # We use 0 here as we deleted the Group we should have any left
    assert 0 == result_on_server

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Name'")

    normal_result = "1==glpi::Computer name==*win*"

    assert normal_result != result_on_server[0]


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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Description'")

    normal_result = "1==glpi::Description==*win*"

    assert normal_result != result_on_server[0]



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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Inventory Number'")

    normal_result = "1==glpi::Inventory number==*win*"

    assert normal_result != result_on_server[0]


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
    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Glpi Group'")

    normal_result = "1==glpi::Group==*win*"

    assert normal_result != result_on_server[0]


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
    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Peripheral name'")

    normal_result = "1==glpi::Peripheral name==*win*"

    assert normal_result != result_on_server[0]


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
    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Peripheral serial'")

    normal_result = "1==glpi::Peripheral serial==*win*"

    assert normal_result != result_on_server[0]


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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Machine Type'")

    normal_result = "1==glpi::System type==*win*"

    assert normal_result != result_on_server[0]

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Machine Manufacturer'")

    normal_result = "1==glpi::System manufacturer==*win*"

    assert normal_result != result_on_server[0]

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Machine Model'")

    normal_result = "1==glpi::System model==*win*"

    assert normal_result != result_on_server[0]

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Machine Owner'")

    normal_result = "1==glpi::Owner of the machine==*win*"

    assert normal_result != result_on_server[0]

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Last Logged User'")

    normal_result = "1==glpi::Last Logged User==*win*"

    assert normal_result != result_on_server[0]

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By User location'")

    normal_result = "1==glpi::User location==*win*"

    assert normal_result != result_on_server[0]

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Location'")

    normal_result = "1==glpi::Location==*win*"

    assert normal_result != result_on_server[0]

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By State'")

    normal_result = "1==glpi::State==*win*"

    assert normal_result != result_on_server[0]

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Entity'")

    normal_result = "1==glpi::Entity==*win*"

    assert normal_result != result_on_server[0]

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Operating System'")

    normal_result = "1==glpi::Operating system==*win*"

    assert normal_result != result_on_server[0]

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Installed Software'")

    normal_result = "1==glpi::Installed software==*win*"

    assert normal_result != result_on_server[0]

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Software Name and Version'")

    normal_result = "1==glpi::Installed software (specific version)==>Notepad, 0.1<"

    assert normal_result != result_on_server[0]

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By OS Version'")

    normal_result = "1==glpi::OS Version==*win*"

    assert normal_result != result_on_server[0]

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Architecture'")

    normal_result = "1==glpi::Architecture==*win"

    assert normal_result != result_on_server[0]

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Register Key'")

    normal_result = "1==glpi::Register key==*win*"

    assert normal_result != result_on_server[0]

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

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Register Key value'")

    normal_result = "1==glpi::Register key value==>*win*, *win*<"

    assert normal_result != result_on_server[0]

def test_create_group_based_by_OU_User(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")

    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#xmppmaster').click()
    page.locator('//*[@id="OU-User"]').click()
    page.locator('//*[@id="autocomplete"]').fill("test OU User")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By OU User")
    page.click(".btnPrimary[type='submit']")

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By OU User'")

    normal_result = "1==xmppmaster::OU user==test OU User"

    assert normal_result != result_on_server[0]

def test_create_group_based_by_OU_Machine(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")

    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#xmppmaster').click()
    page.locator('//*[@id="OU-Machine"]').click()
    page.locator('//*[@id="autocomplete"]').fill("test OU Machine")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By OU Machine")
    page.click(".btnPrimary[type='submit']")

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By OU Machine'")

    normal_result = "1==xmppmaster::OU user==test OU Machine"

    assert normal_result != result_on_server[0]

def test_create_group_by_online_computers(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.click('#glpi')
    page.click('#Online-computer')
    page.click('.btnPrimary[type="submit"]')
    page.click('.btnPrimary[type="button"]')
    page.locator('//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input').fill("Group Created by playwright By Online Computers")
    page.click('.btnPrimary[type="submit"]')

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Online Computers'")

    normal_result = "1==glpi::Online computer==True"

    assert normal_result != result_on_server[0]

    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_by_offline_computers(page: Page) -> None:
    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.click('#glpi')
    page.click('#Online-computer')
    page.locator("//select[@name='value']").select_option("False")
    page.click('.btnPrimary[type="submit"]')
    page.click('.btnPrimary[type="button"]')
    page.locator('//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input').fill("Group Created by playwright By Offline Computers")
    page.click('.btnPrimary[type="submit"]')

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Offline Computers'")

    normal_result = "1==glpi::Online computer==False"

    assert normal_result != result_on_server[0]

    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_by_existing_group(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.click('#dyngroup')
    page.locator('#autocomplete').fill("Group Created by playwright By Existing Group")
    page.click('.btnPrimary[type="submit"]')
    page.click('.btnPrimary[type="button"]')
    page.locator('//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input').fill("Group Created by playwright By Existing Group")
    page.click('.btnPrimary[type="submit"]')

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Group Created by playwright By Existing Group'")

    normal_result = "1==dyngroup::groupname==Group Created by playwright By Existing Group==True"

    assert normal_result != result_on_server[0]

    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))