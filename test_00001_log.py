from playwright.sync_api import  expect, Page
import configparser
import os


project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')


def test_basic_login(page: Page) -> None:

    page.goto(test_server)

    # We fill username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', 'siveo')
    page.click('#connect_button')

    expect(page).to_have_url( test_server + "/mmc/main.php?module=base&submod=main&action=default")

    pass
