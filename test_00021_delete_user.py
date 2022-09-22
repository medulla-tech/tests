from playwright.sync_api import  expect, Page
import time

login = Config.get('test_server', 'login')
password = Config.get('test_server', 'password')


def test_delete_users(page: Page) -> None:

    page.goto('http://wva.siveo.net')

    # We fill username/password and we connect into the mmc.
    page.fill('#username', login)
    page.fill('#password', password)
    #page.click('#connect_button')
    expect(page).to_have_url("http://wva.siveo.net/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarusers')
    expect(page).to_have_url("http://wva.siveo.net/mmc/main.php?module=base&submod=users&action=index")
    page.click('//html/body/div/div[4]/div/div[2]/form/table/tbody/tr[2]/td[5]/ul/li[3]/a')
    page.click('#delfiles')
    page.click(".btnPrimary[type='submit']")

    page.click(".btnPrimary[type='submit']")
    time.sleep(1)
    expect(pagei).to_have_url("http://wva.siveo.net/mmc/main.php?module=base&submod=users&action=index")

