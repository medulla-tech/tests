from playwright.sync_api import  expect, Page

import configparser
import os
import MySQLdb
import sys


project_dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
# MEDULLA_CONFIG selects another file, e.g. one per server (config.preprod.ini)
Config.read(os.environ.get('MEDULLA_CONFIG') or os.path.join(project_dir, "config.ini"))

# Environment variables override the config file, so the CI can pass secrets
# without writing them to disk.
env_overrides = {
    'name': 'MEDULLA_URL',
    'login': 'MEDULLA_USER',
    'password': 'MEDULLA_PASSWORD',
    'ssh': 'MEDULLA_HOST',
    'port': 'MYSQL_PORT',
    'mysqluser': 'MYSQL_USER',
    'mysqlpass': 'MYSQL_PASSWORD',
    'machinename': 'MEDULLA_MACHINE',
    'passkey_path': 'SSH_KEY_PATH',
    'passphrase': 'SSH_KEY_PASSPHRASE',
}
for option, variable in env_overrides.items():
    if os.environ.get(variable):
        # Escape % so ConfigParser interpolation leaves the value untouched
        Config.set('test_server', option, os.environ[variable].replace('%', '%%'))

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
    page.fill('#username', user)
    page.fill('#password', password)
    page.click('#connect_button')

    # Recent Medulla versions removed this toggle: expert mode is always on
    expert_mode = page.locator("#expertmode")
    if expert_mode.count():
        expert_mode.click()
    expect(page).to_have_url(test_server + "/mmc/main.php?module=base&submod=main&action=default")



def sqlcheck(base, sql_request) -> None:
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
                            db=base,
                            connect_timeout=10)

        cursor = db.cursor()
        cursor.execute(sql_request)

        db.commit()

        for row in cursor.fetchone() or cursor:
            return row

        return None

    except Exception as e:
        # Fail the test with the reason instead of exiting silently
        raise AssertionError(f"MySQL request on {base}@{hostname} failed: {e}") from e


def sqlfetchall(base, sql_request) -> list:
    """
        Used to run a SQL request returning several rows
        Args:
            base: The database where we will do the request.
            sql_request: The SQL Request that will be played
    """
    try:
        db = MySQLdb.connect(host=hostname,
                            user=mysqluser,
                            passwd=mysqlpass,
                            port=int(port),
                            db=base,
                            connect_timeout=10)
        cursor = db.cursor()
        cursor.execute(sql_request)
        return list(cursor.fetchall())

    except Exception as e:
        raise AssertionError(f"MySQL request on {base}@{hostname} failed: {e}") from e


def get_an_available_update() -> str:
    """
        Get an update from the Grey List but not yet validated/activated
    """

    sql_command = 'SELECT updateid FROM up_gray_list WHERE valided="0" LIMIT 1'
    return sqlcheck("xmppmaster", sql_command)


def get_an_activated_update() -> str:
    """
        Get an update from the Grey List but not yet validated/activated
    """

    sql_command = 'SELECT updateid FROM up_gray_list WHERE valided="1" LIMIT 1'
    return sqlcheck("xmppmaster", sql_command)

def get_a_greylist_update() -> str:
    """
        Get an update from the Grey List but not yet validated/activated
    """

    sql_command = 'SELECT updateid FROM up_gray_list LIMIT 1'
    return sqlcheck("xmppmaster", sql_command)

def is_update_activated(updateid) -> str:
    """
        Tell if an update is validated or not.

        Returns:
            1 if the update is validated. 0 otherwise
    """

    sql_command = f'SELECT valided FROM up_gray_list WHERE updateid="{updateid}"'
    return sqlcheck("xmppmaster", sql_command)


def is_update_whitelisted(updateid) -> str:
    """
        Tell if an update is validated or not.

        Returns:
            1 if the update is validated. 0 otherwise
    """

    sql_command = f'SELECT valided FROM up_white_list WHERE updateid="{updateid}"'
    return sqlcheck("xmppmaster", sql_command)

def is_update_blacklisted(updateid) -> str:
    """
        Tell if an update is validated or not.

        Returns:
            1 if the update is validated. 0 otherwise
    """

    sql_command = f'SELECT enable_rule FROM up_black_list WHERE updateid_or_kb="{updateid}"'
    return sqlcheck("xmppmaster", sql_command)
