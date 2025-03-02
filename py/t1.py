import re

pattern = r"DELETE\s+FROM\s+(?:\$\{\w+\}|\w+(\.\w+)?)\s+"

sql_query = "DELETE FROM ${db}.table WHERE id = 1 AND name LIKE '%John%\'; -- 댓글"

match = re.search(pattern, sql_query, re.IGNORECASE | re.DOTALL)

if match:
    # owner = match.group(0)
    table_name = match.group(1)

    # print("owner Name:", owner)
    print("Table Name:", table_name)
else:
    print("No match found.")

