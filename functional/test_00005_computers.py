from playwright.sync_api import  expect, Page
from common import medulla_connect, sqlcheck

import configparser
import os
import re
from time import sleep

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


def test_open_filesmanagers(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#filesmanagers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=filesmanagers")

def test_open_topology(page: Page) -> None:

    medulla_connect(page)
    
    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")
    
    page.click('#topology')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=xmppmaster&submod=xmppmaster&action=topology")

def test_open_inventory_from_name(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_inventory_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .inventory a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_monitoring_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .monit a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_remoteviewer_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .guaca a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_backup_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .urbackup a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_deploy_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .install a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_imaging_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .imaging a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_xmppconsole_tab_summary(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .console a"
    page.click(machine_inventory)

    page.click("#tab0")
    expect(page).to_have_url(re.compile(".*part=Summary*"))

def test_open_fileviewer_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sleep(5)
    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .fileviewer a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

def test_open_config_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .config a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

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

def test_open_delete_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .delete a"
    page.click(machine_inventory)

    page.click('#imageWarning')
    page.click(".btnPrimary[type='submit']")

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

    page.click("#tab1")
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

    page.click("#tab2")
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

    page.click("#tab3")
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

    page.click("#tab4")
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

    page.click("#tab5")
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

    page.click("#tab6")
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

    page.click("#tab7")
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

    page.click("#tab8")
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

    page.click("#tab9")
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

    machine_inventory = "#m_" + machine_serial + " .console a"
    page.click(machine_inventory)

    page.click("#tab0")
    expect(page).to_have_url(re.compile(".*part=Summary*"))

def test_open_glpi_fileviewer_from_bar(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    sleep(5)
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesListglpi')
    sql_command = 'SELECT hostname FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .fileviewer a"
    page.click(machine_inventory)

    #TODO: Add expect for the URL.

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

    #TODO: Add expect for the URL.
