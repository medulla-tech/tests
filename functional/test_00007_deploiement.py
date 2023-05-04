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

LOGGER = logging.getLogger(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')
login = Config.get('test_server', 'login')
password = Config.get('test_server', 'password')
machineName = Config.get('test_server', 'machinename')


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

    page.click(".install > a >> nth=0")
    time.sleep(1)

    page.click('.start')
    time.sleep(1)

    template_deploy(page)

def test_deploy_delayed_command(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesList')
    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m" + machine_serial + " .install a"
    page.click(machine_inventory)

    page.click("//html/body/div/div[4]/div/div[3]/div/form/table/tbody/tr/td[5]/ul/li[1]/a")


    now = datetime.now()

    start_hour = now + timedelta(minutes=5)
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

    page.click(".btnPrimary[type='submit']")
    template_deploy(page)

def test_deploy_interval_input(page: Page):
    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesList')
    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " > td.action > ul > li.install > a"
    page.click(machine_inventory)

    page.click("//html/body/div/div[4]/div/div[3]/div/form/table/tbody/tr[9]/td[5]/ul/li[1]/a")

    value_ok = ["", "1-3", "1-3,5-7"]
    value_nok = ["0,1,2", "1-2-3", "-1-3", "1-25", "a", "a-1", "1-b", "a-b", "a-b-c", "a,b,c"]
    # We definie the input field
    input_field = page.locator("//html/body/div[1]/div[4]/div/div[3]/form/table/tbody/tr[4]/td[2]/span/input")

    # We define the button to check if it's disabled or not
    button = page.locator("//html/body/div[1]/div[4]/div/div[3]/form/input[1]")

    # We Verify that the button is enabled with valid values
    for value in value_ok:
        input_field.fill(value)
        input_field.click()

        assert not button.is_disabled()

    # We Verify that the button is disabled with invalid values
    for value in value_nok:
        input_field.fill(value)
        input_field.click()

        assert button.is_disabled()

def test_deploy_interval_calendar(page: Page):

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesList')
    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " > td.action > ul > li.install > a"
    page.click(machine_inventory)

    page.click("//html/body/div/div[4]/div/div[3]/div/form/table/tbody/tr[9]/td[5]/ul/li[1]/a")

    # We open the first input of the calendar
    page.click("//html/body/div[1]/div[4]/div/div[3]/form/table/tbody/tr[2]/td[2]/input[2]")
    start_date = page.locator("//html/body/div[2]/table/tbody/tr[5]/td[1]/a")
    start_date.click()

    # Push enter to close the calendar
    page.keyboard.press("Enter")

    # We open the second input of the calendar
    page.click("//html/body/div[1]/div[4]/div/div[3]/form/table/tbody/tr[3]/td[2]/input[2]")
    end_date = page.locator("//html/body/div[2]/table/tbody/tr[2]/td[1]/a")
    end_date.click()

    button = page.locator("//html/body/div[1]/div[4]/div/div[3]/form/input[1]")
    assert button.is_disabled()