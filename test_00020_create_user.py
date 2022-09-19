from playwright.sync_api import  expect, Page

def test_create_users(page: Page) -> None:

    page.goto('http://wva.siveo.net')

    # We fille username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', 'siveo')
    page.click('#connect_button')
    expect(page).to_have_url("http://wva.siveo.net/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarusers')
    expect(page).to_have_url("http://wva.siveo.net/mmc/main.php?module=base&submod=users&action=index")

    page.locator('#base_users_add').click()
    expect(page).to_have_url("http://wva.siveo.net/mmc/main.php?module=base&submod=users&action=add")

    page.fill('#uid', 'test_user')
    page.fill('#pass', 'siveo')
    page.fill('#confpass', 'siveo')
    page.fill('#sn', 'Familly Name')
    page.fill('#givenName', 'givenName')
    page.fill('#title', 'title')

    page.click(".btnPrimary[type='submit']")
    expect(page).to_have_url("http://wva.siveo.net/mmc/main.php?module=base&submod=users&action=edit&user=test_user")
