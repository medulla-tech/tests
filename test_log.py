from playwright.sync_api import Playwright, sync_playwright, expect
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to http://dev.siveo.net/mmc/
    page.goto("http://dev.siveo.net/mmc/")
    # Click input[name="username"]
    page.locator("input[name=\"username\"]").click()
    # Fill input[name="username"]
    page.locator("input[name=\"username\"]").fill("root")
    # Click input[name="password"]
    page.locator("input[name=\"password\"]").click()
    # Fill input[name="password"]
    page.locator("input[name=\"password\"]").fill("siveo")
    # Click text=Connecter
    page.locator("text=Connecter").click()
    expect(page).to_have_url("http://dev.siveo.net/mmc/main.php?module=base&submod=main&action=default")
    # ---------------------
    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)
