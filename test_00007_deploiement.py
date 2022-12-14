from playwright.sync_api import expect, Page, Request
from urllib.parse import urlparse, parse_qs
from common import medulla_connect

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
