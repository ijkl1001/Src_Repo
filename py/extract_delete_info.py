import re
import csv
import os

def extract_delete_info(file_path, content):
    # pattern = r"DELETE\s+FROM\s+(?:) (\S+)\s+WHERE\s+(.*)"
    # pattern = r"DELETE\s+FROM\s+(?:\w+\.\w+|\w+)\s+WHERE\s+(.*?)"
    pattern = r"""
DELETE\s+FROM\s+
(?:\w+\.\w+|\w+)\s+  # Capture database.table or table name
WHERE\s+(.*)          # Capture WHERE clause (greedy)
;
"""
    match = re.search(pattern, content, re.IGNORECASE)

    if match:
        table_name = match.group(1)
        where_clause = match.group(2)
        return file_path, os.path.basename(file_path), os.path.splitext(file_path)[1], "owner_info", table_name, where_clause, content
    else:
        return None

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as  f:
                content = f.read()  

                info = extract_delete_info(file_path, content)
                if info:
                    yield info

def write_to_csv(data, filename="delete_statements.csv"):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['path', 'file', 'extension', 'owner', 'table', 'where_clause', 'full_statement']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Example usage:
directory_to_scan = "c:/py/delete_in.sql"
delete_info = list(process_directory(directory_to_scan))
write_to_csv(delete_info)
