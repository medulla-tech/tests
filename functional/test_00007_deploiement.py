from playwright.sync_api import expect, Page, Request
from urllib.parse import urlparse, parse_qs
from common import medulla_connect, sqlcheck

import tempfile
import logging
from subprocess import call
import os
import filecmp
import json
import configparser
import time
import unittest
from datetime import datetime, timedelta

LOGGER = logging.getLogger(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')
login = Config.get('test_server', 'login')
password = Config.get('test_server', 'password')
machineName = Config.get('test_server', 'machinename')

def find_uuid_web(package_url) -> str:
    """
    It uses the URL of the package to exact the uuid.
    The uuid is used on the filesystem to store the package

    Args:
        package_url: The URL of the package

    Returns:
        Returns a string with the uuid of the packge
    """

    package_uuid = ""
    parsed_url = urlparse(package_url).query
    package_uuid = parse_qs(parsed_url).get("packageUuid", "")
    return package_uuid

def find_uuid_sql(label) -> str:


    # If we replay the test job, only take one
    sql_request = "SELECT uuid FROM packages WHERE label = '" + label + "'LIMIT 1"
    package_uuid = sqlcheck("pkgs", sql_request)

    return package_uuid

def template_deploy(page: Page) -> None:
    result_depl = True

    def check_deploy_success():
        order_sent = page.locator("text=Deployment successful")

        try:
            order_sent.wait_for(timeout=1000)
            return True
        except:
            return False

    def check_deploy_error():
        order_error = page.locator("text=Deployment aborted")

        try:
            order_error.wait_for(timeout=1000)
            LOGGER.info("ca marche")
            return True
        except:
            LOGGER.info("Oooops")
            return False

    while check_deploy_success() == False:
        page.reload()
        time.sleep(3)

        if check_deploy_error() == True:
            LOGGER.info("Deployment error")
            result_depl = False
            break


    assert result_depl == True

def test_deploy_package_execute_command(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesList')
    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)


    machine_inventory = "#m_" + machine_serial + " .install a"
    page.click(machine_inventory)

    package_uuid = find_uuid_sql("Notepad++")

    package_to_deploy = "#p_" + package_uuid + " >> .start >> a"
    page.click(package_to_deploy)

    time.sleep(1)

    template_deploy(page)

def test_deploy_delayed_command(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesList')
    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .install a"
    page.click(machine_inventory)

    page.click("//html/body/div/div[4]/div/div[3]/div/form/table/tbody/tr[4]/td[5]/ul/li[2]/a")

    now = datetime.now()

    start_hour = now + timedelta(minutes=1)
    start_hour_str = start_hour.strftime('%Y-%m-%d %H:%M:%S')

    end_hour = start_hour + timedelta(hours=1)
    end_hour_str = end_hour.strftime('%Y-%m-%d %H:%M:%S')

    end_date = page.locator("#end_date")
    end_date.evaluate("node => node.removeAttribute('readonly')");

    end_date.evaluate("node => node.setAttribute('value', '%s')" % end_hour_str);
    end_date.evaluate("node => node.setAttribute('readonly', 1)");


    start_date = page.locator("#start_date")
    start_date.evaluate("node => node.removeAttribute('readonly')");

    start_date.evaluate("node => node.setAttribute('value', '%s')" % start_hour_str);
    start_date.evaluate("node => node.setAttribute('readonly', 1)");

    page.click(".btnPrimary[type='submit']", timeout=600000)
    template_deploy(page)

def test_deploy_planned_command(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesList')
    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .install a"
    page.click(machine_inventory)

    package = 'hostname'

    sql_command_p = 'SELECT uuid FROM packages WHERE label = "' + package + '"'
    package_to_deploy = sqlcheck("pkgs", sql_command_p)

    machine_options = "#p_" + package_to_deploy + " .advanced a"


    now = datetime.now()

    start_hour = now + timedelta(minutes=1)
    start_hour_str = start_hour.strftime('%Y-%m-%d %H:%M:%S')

    end_hour = start_hour + timedelta(minutes=1)
    end_hour_str = end_hour.strftime('%Y-%m-%d %H:%M:%S')

    end_date = page.locator("#exec_date")
    end_date.evaluate("node => node.removeAttribute('readonly')");

    end_date.evaluate("node => node.setAttribute('value', '%s')" % end_hour_str);
    end_date.evaluate("node => node.setAttribute('readonly', 1)");

    page.check('xpath=//*[@id="Delay_install"]')

    page.click(".btnPrimary[type='submit']", timeout=600000)
    template_deploy(page)
