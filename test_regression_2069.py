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
import re
from datetime import datetime, timedelta

project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')
ssh_server = Config.get('test_server', 'ssh')
machineName = Config.get('test_server', 'machinename')

def find_uuid_sql(label) -> str:


    # If we replay the test job, only take one
    sql_request = "SELECT uuid FROM packages WHERE label = '" + label + "'LIMIT 1"
    package_uuid = sqlcheck("pkgs", sql_request)

    return package_uuid


def get_package(package_uuid, tempdir) -> None:
    """
    We retrieve the created package on the test server
    Args:
        package_uuid: The uuid of the package to test
        tempdir: The directory where we will copy the test package
    """
    package_path = os.path.join("/", "var", "lib", "pulse2", "packages", package_uuid)
    cmd = "scp -r root@" + ssh_server + ":%s %s" % (package_path, tempdir)
    call(cmd.split(" "))

def remove_unneeded_key(tempdir, uuid, jsonfile) -> None:
    """
        Used to remove some keys from the json file.
        As the id and creation_date are specific to
        every package we can't use them to compare.

        Args:
            tempdir: The temp dir where the downloaded
                     json is stored
            uuid: The uuid of the package we will test
            jsonfile: The jsonfile we will test (conf.json
                     or xmppdeploy.json)

        We modify the json we downloaded without the
        removed keys.
    """
    def rem_keys_in_dict(keys, mydict):
        """
            It parses the json file to remove
            the unwanted keys.
        """
        for key in keys:
            if key in mydict:
                mydict.pop(key)

    filename = os.path.join(tempdir, uuid, jsonfile)
    content = ""

    with open(filename, "r") as conffile:
        content = conffile.read()
        conffile.close()

    conf = json.loads(content)

    excluded = ["creation_date", "id"]
    if jsonfile == "conf.json":
        rem_keys_in_dict(excluded, conf)
    else:
        rem_keys_in_dict(excluded, conf["info"])

    with open(filename, 'w') as conffile: 
        json.dump(conf, conffile) 
        conffile.close()

def test_create_package_execute(page: Page) -> None:
    """
        It creates a simple package with an empty
        execute field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.fill("#label", "Notepad++")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=0").drag_to(
        page.locator("#current-actions")
    )
    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#current-actions li >> nth=2").drag_to(
        page.locator("#current-actions li >> nth=0")
    )
    # page.click('//*[@id="Form"]/input[3]')
    page.click("#workflow li:nth-child(1) input[type='button'][value='Options']")
    page.fill("#workflow li:nth-child(1) input[name='actionlabel']", "Package de test")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")
    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

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
            return True
        except:
            return False

    while check_deploy_success() == False:
        page.reload()
        time.sleep(3)

        if check_deploy_error() == True:
            LOGGER.info("Deployment error")
            result_depl = False
            break


    assert result_depl == True

def test_deploy_delayed_command(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarcomputers')
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click('#machinesList')
    sql_command = 'SELECT uuid_serial_machine FROM machines WHERE hostname = "' + machineName + '"'
    machine_serial = sqlcheck("xmppmaster", sql_command)

    machine_inventory = "#m_" + machine_serial + " .install a"
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
    start_date.evaluate("node => node.setAttribute('readonly', 1)")

    page.click(".btnPrimary[type='submit']")
    template_deploy(page)

