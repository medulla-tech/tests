from common import sqlcheck

sqlcheck("dyngroup", "DELETE FROM Results")
sqlcheck('dyngroup', "DELETE FROM ShareGroup")
sqlcheck('dyngroup', "DELETE FROM Groups")
