from playwright.sync_api import  expect, Page
import time

def test_open_imaging_manage_postimaging_scripts(page: Page) -> None:

    page.goto('http://dev.siveo.net')

    # We fille username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', 'siveo')
    page.click('#connect_button')
    expect(page).to_have_url("http://dev.siveo.net/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarmanage')
    expect(page).to_have_url("http://dev.siveo.net/mmc/main.php?module=imaging&submod=manage&action=index")

    page.locator("//html/body/div/div[4]/div/div[1]/ul/li[5]/a").click()
    # As the page can have issues, with wrong php include , or wrong session
    # we wait a second to be sure we have the final page.
    time.sleep(1)
    expect(page).to_have_url("http://dev.siveo.net/mmc/main.php?module=imaging&submod=manage&action=postinstall")
