from playwright.sync_api import  expect, Page
from common import sqlcheck

def test_delete_computers_group(page: Page) -> None:
    print("OK")
    sqlcheck("dyngroup", "DELETE FROM Results")
    sqlcheck('dyngroup', "DELETE FROM ShareGroup")
    sqlcheck('dyngroup', "DELETE FROM Groups")
