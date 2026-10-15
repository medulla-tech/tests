from playwright.sync_api import  expect, Page
from common import sqlcheck

# Only the groups created by the tests: the server may hold real groups too
TEST_GROUPS = "SELECT id FROM Groups WHERE name = 'Group_Test' OR name LIKE '%playwright%'"

def test_delete_computers_group(page: Page) -> None:
    sqlcheck("dyngroup", "DELETE FROM Results WHERE FK_groups IN (" + TEST_GROUPS + ")")
    sqlcheck('dyngroup', "DELETE FROM ShareGroup WHERE FK_groups IN (" + TEST_GROUPS + ")")
    sqlcheck('dyngroup', "DELETE FROM Groups WHERE name = 'Group_Test' OR name LIKE '%playwright%'")
