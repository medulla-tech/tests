from playwright.sync_api import Playwright, sync_playwright, expect
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://dev.siveo.net/mmc/")
    page.locator("input[name=\"username\"]").click()
    page.locator("input[name=\"username\"]").fill("root")
    page.locator("input[name=\"password\"]").click()
    page.locator("input[name=\"password\"]").fill("siveo")
    page.locator("text=Connecter").click()
    expect(page).to_have_url("http://dev.siveo.net/mmc/main.php?module=base&submod=main&action=default")
    page.locator("#navbarusers").click()
    expect(page).to_have_url("http://dev.siveo.net/mmc/main.php?module=base&submod=users&action=index")
    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)

