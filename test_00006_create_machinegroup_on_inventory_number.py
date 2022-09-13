from playwright.sync_api import  expect, Page
import re

def test_create_group_based_on_inventory_number(page: Page) -> None:

    page.goto('http://dev.siveo.net')

    # We fill username/password and we connect into the mmc.
    page.fill('#username', 'root')
    page.fill('#password', 'siveo')
    page.click('#connect_button')

    expect(page).to_have_url("http://dev.siveo.net/mmc/main.php?module=base&submod=main&action=default")

    page.click('#navbarcomputers')
    expect(page).to_have_url("http://dev.siveo.net/mmc/main.php?module=base&submod=computers&action=machinesList")

    page.click("#computersgroupcreator")
    expect(page).to_have_url("http://dev.siveo.net/mmc/main.php?module=base&submod=computers&action=computersgroupcreator")

    page.locator('tr td a >> nth=0').click()
    page.locator('.listinfos tbody tr td a >> nth=2').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.locator("//html/body/div/div[4]/div/div[3]/form/table/tbody/tr/td[4]/input[2]").click()
    page.locator("//html/body/div/div[4]/div/div[3]/table[3]/tbody/tr/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Inventory Number")
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[2]/td[3]/input").click()
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))
