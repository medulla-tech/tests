from playwright.sync_api import  expect, Page
from common import medulla_connect, sqlcheck

import logging
import re
import configparser
import os
import time

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()
project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')
GroupTest = "Group_Test"
machineName = Config.get('test_server', 'machinename')

"""
    The tests are done to test the user page of pulse.

    Test to be done:
    -> Edit a group
        -> Add a new description to an existing group
    -> Add new machines to a group

"""
def test_remove_all_groups(page: Page) -> None:
    try:
        sqlcheck("dyngroup", "DELETE FROM ShareGroup WHERE FK_groups IN (SELECT id FROM Groups WHERE name LIKE '%playwright%');")
        sqlcheck('dyngroup', "DELETE FROM Results WHERE FK_groups IN (SELECT id FROM Groups WHERE name LIKE '%playwright%');")
        sqlcheck('dyngroup', "DELETE FROM Groups WHERE name LIKE '%playwright%';")
        mylogger.debug("Groups and related data successfully removed.")
    except Exception as e:
        mylogger.debug(f"Error occurred while removing groups: {e}")


def test_create_group_Default(page: Page) -> None:

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

# Run this manually for the moment, it works on the machine but not on Jenkins
#
#def test_create_duplicate_group_based_on_name(page: Page) -> None:
#
#    """
#        We create a dupplicate group ( the same as the previous test.
#        We only allow one group with a name.
#        We expect to obtain an error pop-up
#    """
#    medulla_connect(page)
#
#    page.click('#navbarcomputers')
#    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")
#
#    page.click("#computersgroupcreator")
#    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")
#
#    page.locator('#glpi').click()
#    page.locator('#Computer-name').click()
#    page.locator('//*[@id="autocomplete"]').click()
#    page.locator('//*[@id="autocomplete"]').fill("*win*")
#    page.click(".btnPrimary[type='submit']")
#    page.click(".btnPrimary[type='button']")
#
#    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill(GroupTest)
#
#    page.click(".btnPrimary[type='submit']")
#    popup_locator = page.locator('#__popup_container .alert.alert-error')
#    popup_locator.wait_for(timeout=100000)
#
#    wanted_sentence = "A group already exists with name '%s'" % GroupTest
#
#    expect(popup_locator).to_have_text(wanted_sentence)

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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Name")

    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Name'")

    normal_result = "1==glpi::Computer name==*win*"

    assert normal_result == result_on_server


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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Description")

    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Description'")

    normal_result = "1==glpi::Description==*win*"

    assert normal_result == result_on_server


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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Inventory Number")

    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Inventory Number'")

    normal_result = "1==glpi::Inventory number==*win*"

    assert normal_result == result_on_server


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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Glpi Group")

    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))
    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Glpi Group'")

    normal_result = "1==glpi::Group==*win*"

    assert normal_result == result_on_server


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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Peripheral name")

    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))
    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Peripheral name'")

    normal_result = "1==glpi::Peripheral name==*win*"

    assert normal_result == result_on_server


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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Peripheral serial")

    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))
    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Peripheral serial'")

    normal_result = "1==glpi::Peripheral serial==*win*"

    assert normal_result == result_on_server


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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Machine Type")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Machine Type'")

    normal_result = "1==glpi::System type==*win*"

    assert normal_result == result_on_server

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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Machine Manufacturer")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Machine Manufacturer'")

    normal_result = "1==glpi::System manufacturer==*win*"

    assert normal_result == result_on_server

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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Machine Model")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Machine Model'")

    normal_result = "1==glpi::System model==*win*"

    assert normal_result == result_on_server

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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Machine Owner")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Machine Owner'")

    normal_result = "1==glpi::Owner of the machine==*win*"

    assert normal_result == result_on_server

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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Last Logged User")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Last Logged User'")

    normal_result = "1==glpi::Last Logged User==*win*"

    assert normal_result == result_on_server

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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By User location")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By User location'")

    normal_result = "1==glpi::User location==*win*"

    assert normal_result == result_on_server

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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Location")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Location'")

    normal_result = "1==glpi::Location==*win*"

    assert normal_result == result_on_server

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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By State")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By State'")

    normal_result = "1==glpi::State==*win*"

    assert normal_result == result_on_server

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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Entity")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Entity'")

    normal_result = "1==glpi::Entity==*win*"

    assert normal_result == result_on_server

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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Operating System")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Operating System'")

    normal_result = "1==glpi::Operating system==*win*"

    assert normal_result == result_on_server

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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Installed Software")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Installed Software'")

    normal_result = "1==glpi::Installed software==*win*"

    assert normal_result == result_on_server

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
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Software Name and Version")
    page.click(".btnPrimary[type='submit']")

    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Software Name and Version'")

    normal_result = "1==glpi::Installed software (specific version)==>Notepad, 0.1<"

    assert normal_result == result_on_server

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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By OS Version")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By OS Version'")

    normal_result = "1==glpi::OS Version==*win*"

    assert normal_result == result_on_server

def test_create_group_based_on_architecture(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="Architecture"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("64-bit")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Architecture")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Architecture'")

    normal_result = "1==glpi::Architecture==64-bit"

    assert normal_result == result_on_server

def test_create_group_based_on_register_key(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#glpi').click()
    page.locator('//*[@id="Register-key"]').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("Register-key")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Register Key")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Register Key'")

    normal_result = "1==glpi::Register key==Register-key"

    assert normal_result == result_on_server

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

    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By Register Key value")
    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Register Key value'")

    normal_result = "1==glpi::Register key value==>*win*, *win*<"

    assert normal_result == result_on_server

def test_create_group_based_by_OU_User(page: Page) -> None:

    medulla_connect(page)

    sql_command = 'UPDATE machines SET ad_ou_user="ou_user" WHERE hostname = "' + machineName + '"'
    sqlcheck("xmppmaster", sql_command)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")

    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#xmppmaster').click()
    page.locator("//a[@id='OU-user']").click()
    page.locator('//*[@id="autocomplete"]').fill("ou_user")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By OU User")
    page.click(".btnPrimary[type='submit']")

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By OU User'")

    normal_result = "1==xmppmaster::OU user==ou_user"

    assert normal_result == result_on_server

def test_create_group_based_by_OU_Machine(page: Page) -> None:

    medulla_connect(page)

    sql_command = 'UPDATE machines SET ad_ou_machine="ou_machine" WHERE hostname = "' + machineName + '"'
    sqlcheck("xmppmaster", sql_command)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")

    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('#xmppmaster').click()
    page.locator('//*[@id="OU-Machine"]').click()
    page.locator('//*[@id="autocomplete"]').fill("ou_machine")
    page.click(".btnPrimary[type='submit']")
    page.click(".btnPrimary[type='button']")
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Created by playwright By OU Machine")
    page.click(".btnPrimary[type='submit']")

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By OU Machine'")

    normal_result = "1==xmppmaster::OU Machine==ou_machine"

    assert normal_result == result_on_server

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
    page.locator('//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input').fill("Created by playwright By Online Computers")
    page.click('.btnPrimary[type="submit"]')

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Online Computers'")

    normal_result = "1==glpi::Online computer==True"

    assert normal_result == result_on_server

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
    page.locator('//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input').fill("Created by playwright By Offline Computers")
    page.click('.btnPrimary[type="submit"]')

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Offline Computers'")

    normal_result = "1==glpi::Online computer==False"

    assert normal_result == result_on_server

    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_by_existing_group(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.click('#dyngroup')
    page.locator('#autocomplete').fill("Created by playwright By Existing Group")
    page.click('.btnPrimary[type="submit"]')
    page.click('.btnPrimary[type="button"]')
    page.locator('//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input').fill("Created by playwright By Existing Group")
    page.click('.btnPrimary[type="submit"]')

    result_on_server = sqlcheck("dyngroup", "SELECT query FROM Groups WHERE name = 'Created by playwright By Existing Group'")

    normal_result = "1==dyngroup::groupname==Created by playwright By Existing Group"

    assert normal_result == result_on_server

    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_static(page: Page) -> None:
    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.click("#tabsta a")

    page.fill(".tabdiv input[name='name']", "Created by playwright Static")

    page.locator("input[name=\"bfiltmachine\"]").click()
    page.click(".list option >> nth=0")
    page.click("#grouplist input[name='baddmachine']")
    page.click(".btnPrimary[type='submit']")

    result_on_server = sqlcheck("dyngroup", "SELECT count(*) from Groups WHERE name = 'Created by playwright Static'")

    assert result_on_server == 1

    locator = page.locator(".alert")
    expect(locator).to_have_class("alert alert-success")

def test_create_group_by_import_csv(page: Page) -> None:
    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.click("#tabfromfile a")
    page.fill("#groupname", "Created by playwright By Import CSV")

    with page.expect_file_chooser() as fc_info:
        page.locator("#importfile").click()
        file_chooser = fc_info.value
        file_chooser.set_files("packages_template/csv_grp.csv")

    page.click(".btnPrimary[type='submit']")

    idfromGroup = sqlcheck("dyngroup", "select id from Groups where name = 'Created by playwright By Import CSV'")

    isCSVGroup = sqlcheck("dyngroup", f"select count(*) from Results where FK_groups='{idfromGroup}'")

    assert result_on_server == 0

def test_share_group(page: Page) -> None:
    
    group_name = "aGroup_Created_by_playwright_For_Sharing"
    id_grp = "#g_"

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.click("#tabsta a")

    page.fill(".tabdiv input[name='name']", group_name)
    page.locator("input[name=\"bfiltmachine\"]").click()
    page.click(".list option >> nth=0")
    page.click("#grouplist input[name='baddmachine']")
    page.click(".btnPrimary[type='submit']")

    locator = page.locator('#__popup_container .alert.alert-success')
    expect(locator).to_have_text('Group successfully created')
    page.click('#__popup_container button')

    page.click("#list")
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=list")

    page.click(id_grp + group_name +" .groupshare a")

    id_sql = str(sqlcheck('dyngroup', "SELECT id FROM Groups WHERE name='"+group_name+"'"))
    expect(page).to_have_url(test_server + '/mmc/main.php?module=base&submod=computers&action=edit_share&id=' + id_sql + '&gid=' + id_sql + '&groupname=' + group_name + '&type=0&mod=')

    page.click('//html/body/div/div[4]/div/form/div/table/tbody/tr/td[1]/div/select/option[1]')
    page.click('//html/body/div/div[4]/div/form/div/table/tbody/tr/td[2]/div/input[1]')
    page.click('.btnPrimary')
    
    locator = page.locator('#__popup_container .alert.alert-success')
    expect(locator).to_have_text('Group successfully shared')
    page.click('#__popup_container button')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=list")


#def test_create_group_use_booleans(page: Page) -> None:
#
#    medulla_connect(page)
#
#    page.click('#navbarcomputers')
#    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")
#
#    page.click("#computersgroupcreator")
#    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")
#
#
#    # Creation of the first condition
#    page.locator('#glpi').click()
#    page.locator('#Computer-name').click()
#    page.locator('//*[@id="autocomplete"]').click()
#    page.locator('//*[@id="autocomplete"]').fill("*win*")
#    page.click(".btnPrimary[type='submit']")
#
#    # Creation of the second condition
#    page.locator('#glpi').click()
#    page.locator('#Description').click()
#    page.locator('//*[@id="autocomplete"]').click()
#    page.locator('//*[@id="autocomplete"]').fill("*For the test*")
#    page.click(".btnPrimary[type='submit']")
#    page.click(".btnPrimary[type='button']")
#
#    # Creation of the boolean
#    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[2]/td[1]/input[1]").fill("AND(1,2)")
#    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill(GroupTest)
#
#    page.click(".btnPrimary[type='submit']")
#    page.click(".btnPrimary[type='button']")
#
#    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill(GroupTest)
#
#    page.click(".btnPrimary[type='submit']")
#
#
#    expect(page).to_have_url(re.compile(".*action=save_detail*"))
