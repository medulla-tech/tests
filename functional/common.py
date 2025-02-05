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
csv_file_path = os.path.join(project_dir, "packages_template/csv_grp.csv")

def medulla_connect(page: Page) -> None:

    page.goto(test_server)

    # Changing the language to English
    locator = page.locator('#lang')
    locator.select_option('C')

    # We fill username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', password)
    page.click('#connect_button')

    page.click("#expertmode")
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
                            db=base)

        cursor = db.cursor()
        cursor.execute(sql_request)

        db.commit()

        for row in cursor.fetchone() or cursor:
            return row

        return None

    except Exception as e:
        sys.exit(1)


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

def generate_csv_import():
    """
    Generate a CSV file with the gpe_machines
    """
    with open(csv_file_path, "w") as f:
        pass
    gpe_machines = Config.get("test_server", "gpe_machine").split(",")
    with open(csv_file_path, "w") as f:
        for machine in gpe_machines:
            machine = machine.strip()
            f.write(f"{machine}\n")