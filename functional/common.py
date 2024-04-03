from playwright.sync_api import  expect, Page

import configparser
import os
import MySQLdb
import sys


project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(project_dir, "config.ini"))

test_server = Config.get('test_server', 'name')

hostname = Config.get('test_server', 'ssh')
user = Config.get('test_server', 'login')
password = Config.get('test_server', 'password')
port = Config.get('test_server', 'port')
mysqluser = Config.get('test_server', 'mysqluser')
mysqlpass = Config.get('test_server', 'mysqlpass')

def medulla_connect(page: Page) -> None:

    page.goto(test_server)

    # Changing the language to English
    locator = page.locator('#lang')
    locator.select_option('C')

    # We fill username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', password)
    page.click('#connect_button')

    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=main&action=default")



def sqlcheck(base, sql_request):
    """
        Used to run SQL requests
        Args:
            db: The database where we will do the requests.
            sql_request: The SQL Request that  will be played
    """
    try:
        db = MySQLdb.connect(host=hostname,
                            user=mysqluser,
                            passwd=mysqlpass,
                            port=int(port),
                            db=base)

        cursor = db.cursor()
        cursor.execute(sql_request)

        for row in cursor.fetchone() or cursor:
            return row

        return None

    except Exception as e:
        sys.exit(1)
