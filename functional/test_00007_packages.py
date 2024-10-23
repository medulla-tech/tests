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

project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')
ssh_server = Config.get('test_server', 'ssh')
passphrase = Config.get('test_server', 'passphrase')
private_key_path = Config.get('test_server', 'passkey_path')

mylogger = logging.getLogger()

"""
    The tests are done to test the package page of pulse.

    Test to be done:
    -> Open the package page.
    -> Create a package ( all possible modes )
    -> Modify a package
    -> Create a rule
    -> List the rules
    -> Edit a rule
"""


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
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Test_execute_package")
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
    page.fill("#workflow li:nth-child(1) .special_textarea", "hostname")
    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )


def test_remove_from_pending(page: Page) -> None:
    """
        It creates a simple package with an empty
        execute field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#pending")
    package_uuid = find_uuid_sql("Test_execute_package")

    element_id = "#p_" +  package_uuid

    mylogger.error(package_uuid)
    try:
        max_attempts = 10
        attempt = 0

        while attempt < max_attempts:
            try:
                page.wait_for_selector(element_id, timeout=10000)
                mylogger.info(f"The package is still on the pending list. Test:  {attempt + 1}")

                page.reload()
                time.sleep(3)
            except:
                mylogger.info("The package is not on the pending list")
                break

            attempt += 1
        else:
            raise AssertionError("After 10 tries, the package is still on the pending list. There is a problem.")

    except Exception as e:
        mylogger.error(f"A problem occured : {e}")

def test_watching_create_package(page: Page) -> None:
    """
        It tests if watching is working or if syncthing is not.
    """

    timeToWait = "20"
    # We need to add a small sleep to make sure the package is well synchronised  on the servers ( principal + ARs )
    mylogger.info(f"We are waiting {timeToWait} secondes. This allow the package to sync on the Relay servers")
    time.sleep(timeToWait)

    medulla_connect(page)

    uuidPackage = find_uuid_sql("Package de test execute")

    sql_request = "SELECT id FROM syncthingsync WHERE uuidpackage = '" + uuidPackage + "'LIMIT 1"
    is_watching_OK = sqlcheck("pkgs", sql_request)

    assert not is_watching_OK


def test_correctness_package_execute_json(page: Page) -> None:
    """
        It checks if the packages we just created is OK.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )


    page.locator("#param").click()
    page.locator("#param").fill("Test_execute_package")
    page.get_by_role("button", name="Search").click()


    page.click(".display > a >> nth=0")

    package_url = page.url
    package_uuid = find_uuid_web(package_url)[0]

    tempdir = tempfile.mkdtemp()

    get_package(package_uuid, tempdir)

    remove_unneeded_key(tempdir, package_uuid, "conf.json")

    with open(os.path.join(tempdir, package_uuid, "conf.json"), 'r') as conffile1, \
         open(os.path.join("packages_template", "conf-execute.json"), 'r') as conffile2:
        confjson1 = json.load(conffile1)
        confjson2 = json.load(conffile2)


    assert(confjson1 == confjson2)


    with open(os.path.join(tempdir, package_uuid, "xmppdeploy.json"), 'r') as xmppfile1, \
         open(os.path.join("packages_template", "xmppdeploy-execute.json"), 'r') as xmppfile2:
        xmppjson1 = json.load(xmppfile1)
        xmppjson2 = json.load(xmppfile2)


    assert(xmppjson1 == xmppjson2)

def test_package_view_execute_package(page: Page) -> None:

    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    package_uuid = find_uuid_sql("Test_execute_package")

    id_to_edit = "#p_" + package_uuid + " >> .display >> a"

    page.locator("#param").click()
    page.locator("#param").fill("Test_execute_package")
    page.get_by_role("button", name="Search").click()

    page.click(id_to_edit)

    # FIXME: Fix the expect part.
    url_to_edit = ".*packageUuid=" + package_uuid + "*"
    expect(page).to_have_url(re.compile(url_to_edit))

def test_package_delete_execute_package(page: Page) -> None:

    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    package_uuid = find_uuid_sql("Test_execute_package")

    page.locator("#param").click()
    page.locator("#param").fill("Test_execute_package")
    page.get_by_role("button", name="Search").click()


    id_to_remove = "#p_" +  package_uuid + " .delete a"
    page.click(id_to_remove)
    page.click(".btnPrimary[type='submit']")

    # To check if the user is created, we check if the locator is present
    locator = page.locator(".alert")
    expect(locator).to_have_class("alert alert-success")


def test_create_package_execute_script(page: Page) -> None:
    """
        It creates a simple package with an empty
        execute script field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test execute_script")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=1").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    time.sleep(1)
    page.click("#workflow >> #property >> nth=0")
    page.fill("#workflow >> #laction", "Package de test")
    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_create_package_set_environment_variables(page: Page) -> None:
    """
        It creates a simple package with an empty
        set environnement variables field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test set_environment_variables")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=2").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    time.sleep(1)
    page.click("#workflow >> #property >> nth=0")
    page.fill("//html/body/div/div[4]/div/form/span/div/div[2]/ul/li[1]/div[2]/div/table/tbody/tr[1]/th[2]/input", "Package de test")
    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_create_package_restart(page: Page) -> None:
    """
        It creates a simple package with an empty
        restart field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test restart")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=3").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    time.sleep(1)
    page.click("#workflow >> #property >> nth=0")
    page.fill("//html/body/div/div[4]/div/form/span/div/div[2]/ul/li[1]/div[2]/div/table/tbody/tr[1]/th[2]/input", "Package de test")
    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_create_package_wait_and_go_to_step(page: Page) -> None:
    """
        It creates a simple package with an empty
        wait and go to step field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test wait_and_go_to_step")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=4").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    time.sleep(1)
    page.click("#workflow >> #property >> nth=0")
    page.fill("//html/body/div/div[4]/div/form/span/div/div[2]/ul/li[1]/div[2]/div/table/tbody/tr[1]/th[2]/input", "Package de test")
    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_create_package_add_info_in_deployement_log(page: Page) -> None:
    """
        It creates a simple package with an empty
        add info in deployement log field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test add_info_in_deployement_log")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=5").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    time.sleep(1)
    page.click("#workflow >> #property >> nth=0")
    page.fill("//html/body/div/div[4]/div/form/span/div/div[2]/ul/li[1]/div[2]/div/table/tbody/tr[1]/th[2]/input", "Package de test")
    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_create_package_set_config_file_parameter(page: Page) -> None:
    """
        It creates a simple package with an empty
        set config file parameter field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test set_config_file_parameter")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=6").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    time.sleep(1)
    page.click("#workflow >> #property >> nth=0")
    page.fill("//html/body/div/div[4]/div/form/span/div/div[2]/ul/li[1]/div[2]/div/table/tbody/tr[1]/th[2]/input", "Package de test")
    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_create_package_unzip_file(page: Page) -> None:
    """
        It creates a simple package with an empty
        unzip file field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test unzip_file")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=7").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    page.fill("#workflow >> .zip_file", "c:\\progra~1\\pulse\\tests\\packages_template\\test.zip")

    time.sleep(1)
    page.click("#workflow >> #property >> nth=0")
    page.fill("#workflow >> #laction", "Package de test")
    page.click("#workflow >> #pathdirectorytounzip")
    page.fill("#workflow >> .pathdirectorytounzip","c:\\progra~1\\pulse\\tests\\packages_template")
    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_create_package_download_file(page: Page) -> None:
    """
        It creates a simple package with an empty
        download file field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test download_file")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=8").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    page.fill("#workflow >> .url_name", "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v7.8.9/npp.7.8.9.Installer.exe")

    time.sleep(1)
    page.click("#workflow >> #property >> nth=0")
    page.fill("//html/body/div/div[4]/div/form/span/div/div[2]/ul/li[1]/div[2]/div/table/tbody/tr[1]/th[2]/input", "Package de test")
    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_create_package_remove_uploaded_files(page: Page) -> None:
    """
        It creates a simple package with an empty
        remove uploaded files field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test remove_uploaded_files")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=9").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    time.sleep(1)
    page.click("#workflow >> #property >> nth=0")
    page.fill("//html/body/div/div[4]/div/form/span/div/div[2]/ul/li[1]/div[2]/div/table/tbody/tr[1]/th[2]/input", "Package de test")
    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_create_package_installation_section(page: Page) -> None:
    """
        It creates a simple package with an empty
        install section field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test installation_section")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=10").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_create_package_update_section(page: Page) -> None:
    """
        It creates a simple package with an empty
        update section field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test update_section")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=11").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )


    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_create_package_uninstall_section(page: Page) -> None:
    """
        It creates a simple package with an empty
        uninstall section field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test uninstall_section")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=12").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_create_package_kiosk_notification(page: Page) -> None:
    """
        It creates a simple package with an empty
        kiosk notification field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test kiosk_notification")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=13").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    time.sleep(1)
    page.click("#workflow >> #property >> nth=0")
    page.fill("//html/body/div/div[4]/div/form/span/div/div[2]/ul/li[1]/div[2]/div/table/tbody/tr[1]/th[2]/input", "Package de test")
    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_create_package_user_notification(page: Page) -> None:
    """
        It creates a simple package with an empty
        user notification field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test user_notification")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=14").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    time.sleep(1)
    page.click("#workflow >> #property >> nth=0")
    page.fill("//html/body/div/div[4]/div/form/span/div/div[2]/ul/li[1]/div[2]/div/table/tbody/tr[1]/th[2]/input", "Package de test")
    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_create_package_user_question(page: Page) -> None:
    """
        It creates a simple package with an empty
        user question field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test user_question")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=15").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    time.sleep(1)
    page.click("#workflow >> #property >> nth=0")
    page.fill("//html/body/div/div[4]/div/form/span/div/div[2]/ul/li[1]/div[2]/div/table/tbody/tr[1]/th[2]/input", "Package de test")
    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_create_package_user_postpone_options(page: Page) -> None:
    """
        It creates a simple package with an empty
        user postpone options field.
    """
    medulla_connect(page)

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.wait_for_selector("input[type='radio'][value='empty']:checked")
    page.fill("#label", "Package de test user_postpone_options")
    page.fill("#version", "0.0")
    page.fill("#description", "CAN BE DELETED. TEST PACKAGE")

    page.locator("#available-actions li >> nth=16").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    # As playwright does not detect correctly the new element, it drops it at the end.
    # We need a second step, after the drop, to use the correct position
    page.locator("#workflow >> .action").drag_to(
        page.locator("#current-actions li >> nth=0")
    )

    time.sleep(1)
    page.click("#workflow >> #property >> nth=0")
    page.fill("//html/body/div/div[4]/div/form/span/div/div[2]/ul/li[1]/div[2]/div/table/tbody/tr[1]/th[2]/input", "Package de test")
    page.click(".btnPrimary[type='submit']")
    page.click(".btn")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

def test_clean_test_packages() -> None:

    private_key = paramiko.RSAKey.from_private_key_file(private_key_path, password=passphrase)

    ssh_client = paramiko.SSHClient()

    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ssh_server, port="22", username="root", pkey=private_key)

    file_to_delete = '/var/lib/pulse2/packages/sharing/global/*'
    delete_command = f'rm -fr {file_to_delete}'
    stdin, stdout, stderr = ssh_client.exec_command(delete_command)


    run_script_command = 'source /var/lib/pulse2/clients/generate-agent-package'
    stdin, stdout, stderr = ssh_client.exec_command(run_script_command)

    ssh_client.close()
