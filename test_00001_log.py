from playwright.sync_api import  expect, Page

def test_basic_login(page: Page) -> None:

    page.goto('http://dev.siveo.net')

    # We fille username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', 'siveo')
    page.click('#connect_button')

    expect(page).to_have_url("http://dev.siveo.net/mmc/main.php?module=base&submod=main&action=default")

    pass
