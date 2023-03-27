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

"""
    The tests are done to test the history page of pulse.
"""

def test_open_history(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarlogview')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=index"
    )

def test_history_logsinventory(page: Page) -> None:
    
    medulla_connect(page)

    page.click('#navbarlogview')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=index"
    )
    page.click('#logsinventory')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=logsinventory"
    )

def test_history_logsbackuppc(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarlogview')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=index"
    )
    page.click('#logsbackuppc')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=logsbackuppc"
    )

def test_history_logsdeployment(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarlogview')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=index"
    )
    page.click('#logsdeployment')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=logsdeployment"
    )

def test_history_logsquickaction(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarlogview')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=index"
    )
    page.click('#logsquickaction')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=logsquickaction"
    )

def test_history_logsdownload(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarlogview')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=index"
    )
    page.click('#logsdownload')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=logsdownload"
    )

def test_history_logskiosk(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarlogview')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=index"
    )
    page.click('#logskiosk')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=logskiosk"
    )

def test_history_logspackaging(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarlogview')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=index"
    )
    page.click('#logspackaging')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=logspackaging"
    )

def test_history_logsremotedesktop(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarlogview')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=index"
    )
    page.click('#logsremotedesktop')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=logsremotedesktop"
    )

def test_history_logsimaging(page: Page) -> None:

    medulla_connect(page)

    page.click('#navbarlogview')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=index"
    )
    page.click('#logsimaging')
    expect(page).to_have_url(
        f"{test_server}/mmc/main.php?module=base&submod=logview&action=logsimaging"
    )
