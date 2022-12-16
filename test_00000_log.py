from playwright.sync_api import  expect, Page
from common import medulla_connect

import configparser
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')
login = Config.get('test_server', 'login')
password = Config.get('test_server', 'password')

def test_basic_login(page: Page) -> None:

    medulla_connect(page)

    pass
