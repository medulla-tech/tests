from playwright.sync_api import expect, Page
from common import medulla_connect, sqlcheck
from bs4 import BeautifulSoup

import logging
import configparser
import os
import re
import sys
from time import sleep

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()
project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')
login = Config.get('test_server', 'login')
password = Config.get('test_server', 'password')
machineName = Config.get('test_server', 'machinename')

"""
    The tests are done to test the computer page of pulse.

    Test to be done:
    -> Open all actions of a machine
    -> Do a search
    -> List online/offline computers.
"""

def test_open_inventory(page: Page) -> None:

    medulla_connect(page)


    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

def test_open_favouriteGroup(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#listFavourite')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=listFavourite")

def test_open_AllGroups(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#list')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=list")


def test_open_CreateGroups(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#computersgroupcreator')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")


def test_open_UninventoriedMachines(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#xmppMachinesList')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=xmppMachinesList")


def test_open_monitoringAlerts(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#alerts')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=alerts")


def test_open_customQA(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#customQA')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=customQA")

def test_open_ActionQuickGroup(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#ActionQuickGroup')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=ActionQuickGroup")

def test_open_inventory_from_name(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " a"
    page.click(machine_inventory)

    expect(page).to_have_url(re.compile(".*action=glpitabs*"))

def test_open_inventory_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .inventory a"
    page.click(machine_inventory)

    expect(page).to_have_url(re.compile(".*action=glpitabs*"))

def test_open_monitoring_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .monit a"
    page.click(machine_inventory)

    expect(page).to_have_url(re.compile(".*action=monitoringview*"))

def test_open_backup_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .urbackup"
    page.click(machine_inventory)

    # We have 2 cases to handle.
    # if the machine is in a urbackup profile, or not yet configured
    # The 2 are valid cases and can be encountered
    try:
        expect(page).to_have_url(re.compile(".*action=checkMachine*"))
    except:
        expect(page).to_have_url(re.compile(".*action=list_backups*"))

def test_open_deploy_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .install a"
    page.click(machine_inventory)

    expect(page).to_have_url(re.compile(".*action=msctabs*"))

def test_open_imaging_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .imaging a"
    page.click(machine_inventory)

    expect(page).to_have_url(re.compile(".*action=register_target*"))

def test_open_xmppconsole_tab_summary(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)


    machine_inventory = "#m_" + machine_serial + " .console a"
    page.click(machine_inventory)

    expect(page).to_have_url(re.compile(".*action=consolecomputerxmpp*"))

def test_open_config_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .config a"
    page.click(machine_inventory)

    expect(page).to_have_url(re.compile(".*action=listfichierconf*"))

def test_open_quickaction_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .quick a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_inventory_tab_hardware(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .inventory a"
    page.click(machine_inventory)

    page.click("#tab1 a")
    expect(page).to_have_url(re.compile(".*part=Hardware*"))

def test_open_inventory_tab_connections(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .inventory a"
    page.click(machine_inventory)

    page.click("#tab2 a")
    expect(page).to_have_url(re.compile(".*part=Connections*"))

def test_open_inventory_tab_storage(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .inventory a"
    page.click(machine_inventory)

    page.click("#tab3 a")
    expect(page).to_have_url(re.compile(".*part=Storage*"))

def test_open_inventory_tab_network(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .inventory a"
    page.click(machine_inventory)

    page.click("#tab4 a")
    expect(page).to_have_url(re.compile(".*part=Network"))

def test_open_inventory_tab_software(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .inventory a"
    page.click(machine_inventory)

    page.click("#tab5 a")
    expect(page).to_have_url(re.compile(".*part=Software"))

def test_open_inventory_tab_administrative(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .inventory a"
    page.click(machine_inventory)

    page.click("#tab6 a")
    expect(page).to_have_url(re.compile(".*part=Administrative"))

def test_open_inventory_tab_history(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .inventory a"
    page.click(machine_inventory)

    page.click("#tab7 a")
    expect(page).to_have_url(re.compile(".*part=History"))

def test_open_inventory_tab_antivirus(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .inventory a"
    page.click(machine_inventory)

    page.click("#tab8 a")
    expect(page).to_have_url(re.compile(".*part=Antivirus*"))

def test_open_inventory_tab_registry(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .inventory a"
    page.click(machine_inventory)

    page.click("#tab9 a")
    expect(page).to_have_url(re.compile(".*part=Registry*"))

def test_open_glpi_inventory_from_name(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesListglpi')
    sql_command = 'SELECT hostname FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " a"
    page.click(machine_inventory)


def test_open_glpi_inventory_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesListglpi')
    sql_command = 'SELECT hostname FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .inventory a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_glpi_monitoring_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesListglpi')
    sql_command = 'SELECT hostname FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .monit a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_glpi_remoteviewer_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesListglpi')
    sql_command = 'SELECT hostname FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .guaca a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_glpi_backup_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesListglpi')
    sql_command = 'SELECT hostname FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .urbackup a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_glpi_deploy_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesListglpi')
    sql_command = 'SELECT hostname FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .install a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_glpi_imaging_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesListglpi')
    sql_command = 'SELECT hostname FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .imaging a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_glpi_xmppconsole_tab_summary(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesListglpi')
    sql_command = 'SELECT hostname FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machineName + " .console a"
    page.click(machine_inventory)    
    expect(page).to_have_url(re.compile(".*action=consolecomputerxmpp*"))

def test_open_glpi_config_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesListglpi')
    sql_command = 'SELECT hostname FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .config a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_glpi_quickaction_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesListglpi')
    sql_command = 'SELECT hostname FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .quick a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_glpi_delete_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesListglpi')
    sql_command = 'SELECT hostname FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .delete a"
    page.click(machine_inventory)

    page.click('#imageWarning')
    page.click(".btnPrimary[type='submit']")

    # Custom loop to wait until the machine_inventory element is back
    timeout = 120  # Maximum time to wait in seconds
    interval = 5  # Time interval between checks in seconds
    elapsed_time = 0

    while elapsed_time < timeout:
        page.reload()  # Refresh the page to see the latest state
        sleep(interval)
        if page.is_visible(machine_inventory):
            mylogger.info("Machine inventory is back and test is completed.")
            break
        elapsed_time += interval

    if elapsed_time >= timeout:
        mylogger.error("Machine inventory did not reappear within the timeout period.")

def test_open_delete_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    while machine_serial == '':
        machine_serial = sqlcheck("xmppmaster", sql_command)
        sleep(5)

    machine_inventory = "#m_" + machine_serial + " .delete a"
    page.click(machine_inventory)

    page.click('#imageWarning')
    page.click(".btnPrimary[type='submit']")

    # Custom loop to wait until the machine_inventory element is back
    timeout = 60  # Maximum time to wait in seconds
    interval = 5  # Time interval between checks in seconds
    elapsed_time = 0

    while elapsed_time < timeout:
        page.reload()  # Refresh the page to see the latest state
        sleep(interval)
        if page.is_visible(machine_inventory):
            mylogger.info("Machine inventory is back and test is completed.")
            break
        elapsed_time += interval

    if elapsed_time >= timeout:
        mylogger.error("Machine inventory did not reappear within the timeout period.")

def test_hovering_modal_xmpp_info(page: Page) -> None:
    """
    This function tests the opening of the machine inventory from the navigation bar.

    It performs the following steps:
    1. Connects to the Medulla server.
    2. Navigates to the computers page and verifies the URL.
    3. Retrieves the IP address and machine serial from the database.
    4. Hovers over the specified machine element to retrieve the 'mydata' attribute.
    5. Parses the HTML content within the 'mydata' attribute to extract the IP address.
    6. Compares the extracted IP address with the IP address from the database.
    7. Logs the results and exits with a failure status if the IP addresses do not match.

    Args:
        page (Page): The Playwright Page object.

    Returns:
        None
    """

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    # Get IP address
    sql_command = 'SELECT ip_xmpp FROM machines WHERE hostname = "' + machineName + '"'
    ip_xmpp = sqlcheck("xmppmaster", sql_command)

    # Get serial
    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    # Retrieve the value of the 'mydata' attribute
    machine_inventory = "#m_" + machine_serial + " .infomach"
    mylogger.info(f"Hovering over the element with text {machineName}...")
    page.locator("//span[text()='qa-win-6']").hover()
    machine_inventory_locator = "#m_" + machine_serial + " .infomach"
    machine_inventory_element = page.locator(machine_inventory_locator)
    mydata_content = machine_inventory_element.get_attribute('mydata')
    mylogger.info(f"My DATA: {mydata_content}")

    # Parse the HTML content within the 'mydata' attribute
    soup = BeautifulSoup(mydata_content, 'html.parser')

    # Extract the IP value
    ip_address = soup.find('td', string='IP address').find_next('td').string.strip()

    mylogger.info(f"IP Address in the page {ip_address}")

    # Check if the IP present is in the modal
    if ip_xmpp in ip_address:
        mylogger.info(f"IP found is the same as in database {ip_xmpp} ")
    else:
        mylogger.info(f"IP {ip_address} not corresponding to {ip_xmpp} in the database.")
        sys.exit(1)
