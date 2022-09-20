from playwright.sync_api import  expect, Page
import re

def test_create_group_based_on_name(page: Page) -> None:

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
    page.locator('.listinfos tbody tr td a >> nth=0').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.locator("//html/body/div/div[4]/div/div[3]/form/table/tbody/tr/td[4]/input[2]").click()
    page.locator("//html/body/div/div[4]/div/div[3]/table[3]/tbody/tr/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Name")
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[2]/td[3]/input").click()
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_description(page: Page) -> None:

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
    page.locator('.listinfos tbody tr td a >> nth=1').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.locator("//html/body/div/div[4]/div/div[3]/form/table/tbody/tr/td[4]/input[2]").click()
    page.locator("//html/body/div/div[4]/div/div[3]/table[3]/tbody/tr/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Description")
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[2]/td[3]/input").click()
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

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

def test_create_group_based_on_glpi_group(page: Page) -> None:

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
    page.locator('.listinfos tbody tr td a >> nth=3').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.locator("//html/body/div/div[4]/div/div[3]/form/table/tbody/tr/td[4]/input[2]").click()
    page.locator("//html/body/div/div[4]/div/div[3]/table[3]/tbody/tr/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Glpi Group")
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[2]/td[3]/input").click()
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_peripheral_name(page: Page) -> None:

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
    page.locator('.listinfos tbody tr td a >> nth=4').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.locator("//html/body/div/div[4]/div/div[3]/form/table/tbody/tr/td[4]/input[2]").click()
    page.locator("//html/body/div/div[4]/div/div[3]/table[3]/tbody/tr/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Peripheral name")
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[2]/td[3]/input").click()
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))

def test_create_group_based_on_peripheral_serial(page: Page) -> None:

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
    page.locator('.listinfos tbody tr td a >> nth=5').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.locator("//html/body/div/div[4]/div/div[3]/form/table/tbody/tr/td[4]/input[2]").click()
    page.locator("//html/body/div/div[4]/div/div[3]/table[3]/tbody/tr/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Peripheral serial")
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[2]/td[3]/input").click()
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))
    
def test_create_group_based_on_machine_type(page: Page) -> None:

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
    page.locator('.listinfos tbody tr td a >> nth=6').click()
    page.locator('//*[@id="autocomplete"]').click()
    page.locator('//*[@id="autocomplete"]').fill("*win*")
    page.locator("//html/body/div/div[4]/div/div[3]/form/table/tbody/tr/td[4]/input[2]").click()
    page.locator("//html/body/div/div[4]/div/div[3]/table[3]/tbody/tr/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").click()
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[1]/td[1]/input").fill("Group Created by playwright By Machine Type")
    page.locator("//html/body/div/div[4]/div/table[2]/tbody/tr[2]/td[3]/input").click()
    expect(page).to_have_url(re.compile(".*submod=computers&action=save_detail*"))
