from playwright.sync_api import expect, Page, Request
from urllib.parse import urlparse, parse_qs
import tempfile
import logging
from subprocess import call
import os
import filecmp
import json
import configparser
import time

project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')
ssh_server = Config.get('test_server', 'ssh')
def find_uuid(package_url) -> str:
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
    page.goto(test_server + "")

    # We fill username/password and we connect into the mmc.
    page.fill("#username", "root")
    page.fill("#password", "siveo")
    page.click("#connect_button")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=base&submod=main&action=default"
    )

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click("#add")
    page.fill("#label", "Package de test")
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
    page.click(".btnPrimary[type='submit']")
    page.click("//html/body/div/div[3]/div[2]/div/div[3]/button")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )


def test_correctness_package(page: Page) -> None:
    """
        It checks if the packages we just created is OK.
    """
    # We need to add a small sleep to make sure the package is well synchronised  on the servers ( principal + ARs )
    time.sleep(5)
    page.goto(test_server)

    # We fill username/password and we connect into the mmc.
    page.fill("#username", "root")
    page.fill("#password", "siveo")
    page.click("#connect_button")

    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=base&submod=main&action=default"
    )

    page.click("#navbarpkgs")
    expect(page).to_have_url(
        test_server + "/mmc/main.php?module=pkgs&submod=pkgs&action=index"
    )

    page.click(
        "//html/body/div/div[4]/div/div[2]/form/table/tbody/tr/td[10]/ul/li[1]/a"
    )

    package_url = page.url
    package_uuid = find_uuid(package_url)[0]

    tempdir = tempfile.mkdtemp()

    get_package(package_uuid, tempdir)

    remove_unneeded_key(tempdir, package_uuid, "conf.json")

    assert (
        filecmp.cmp(
            os.path.join(tempdir, package_uuid, "conf.json"),
            os.path.join("packages_template", "conf-execute.json"),
        )
        == True
    )
    remove_unneeded_key(tempdir, package_uuid, "xmppdeploy.json")
    assert (
        filecmp.cmp(
            os.path.join(tempdir, package_uuid, "xmppdeploy.json"),
            os.path.join("packages_template", "xmppdeploy-execute.json"),
        )
        == True
    )
