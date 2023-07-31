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

# Declaring variables for CSS selector ID for usernames 
# ex: <tr id="u_test_user">
id_code = '#u_'
test_user = 'test_user'

"""
    The tests are done to test the user page of Medulla.
    Warning: To be done correctly, it MUST be started with no users created.

    Test to be done:
    -> Create a user
    -> Delete a user
    -> Edit a user
    -> Backup a user
    -> Create a user already existing ( same name ).
    -> Modify MMC rights
"""

def test_open_users(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarusers')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=users&action=index"
    )


def test_create_users(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarusers')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=users&action=index"
    )

    page.click('#base_users_add')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=users&action=add"
    )

    page.fill('#uid', test_user)
    page.fill('#pass', password)
    page.fill('#confpass', password)
    page.fill('#sn', 'Familly Name')
    page.fill('#givenName', 'givenName')
    page.fill('#title', 'title')

    page.click(".btnPrimary[type='submit']")

    # Testing if the popup is from the alert-success class and if it has the right text
    locator = page.locator('#__popup_container .alert.alert-success')
    expect(locator).to_have_text(f'User {test_user} successfully created')

def test_edit_users_empty(page: Page) -> None:
    """
    Function used to test the user account edition without 
    changing any entries and submitting empty changes
    """
    medulla_connect(page)

    page.click('#navbarusers')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=users&action=index"
    )
    page.click(id_code + test_user + ' .edit')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=users&action=edit&user=test_user"
    )
    page.click(".btnPrimary[type='submit']")

    time.sleep(1)

    # Checking that no alert-error appears
    locator = page.locator('#__popup_container .alert.alert-error')
    expect(locator).to_be_hidden()

def test_edit_users(page: Page) -> None:
    """
    Function used to test user edition by editing an entry and
    submitting changes
    """

    medulla_connect(page)
    page.click('#navbarusers')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=users&action=index"
    )
    page.click(id_code + test_user + ' .edit')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=users&action=edit&user=test_user"
    )
    page.fill('#sn', 'Familly Name Edited')
    page.click(".btnPrimary[type='submit']")

    time.sleep(1)

    # Testing if the popup is from the alert-success class and if it has the right text
    locator = page.locator('#__popup_container .alert.alert-success')
    expect(locator).to_have_text('User attributes updated')

# Testing user creation when user name already exists
def test_duplicated_user(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarusers')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=users&action=index"
    )

    page.locator('#base_users_add').click()
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=users&action=add"
    )

    page.fill('#uid', test_user)
    page.fill('#pass', password)
    page.fill('#confpass', password)
    page.fill('#sn', 'Familly Name')
    page.fill('#givenName', 'givenName')
    page.fill('#title', 'title')
    page.click(".btnPrimary[type='submit']")
    page.click("button.btn")

    # Testing if the popup is from the alert-error class.
    # However, since there is 2 values of .alert we need to specify the entire CSS selector.
    # Then we make sure that it has the right text 
    locator = page.locator('#__popup_container > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')
    expect(locator).to_have_text('The user home directory already exists.Set the home directory in a different location or force the use of the existing directory (in expert mode).')

def test_delete_users(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarusers')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=users&action=index"
    )
    page.click(id_code + test_user + ' .delete a')
    page.click('#delfiles')
    page.click(".btnPrimary[type='submit']")

    # Testing if the popup is from the alert-success class and if it has the right text
    locator = page.locator('#__popup_container .alert.alert-success')
    expect(locator).to_have_text(f'User {test_user} has been successfully deleted')
    page.click('#__popup_container button')

    time.sleep(1)