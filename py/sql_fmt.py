from sql_formatter.core import format_sql
import sqlglot
from sqlglot import parse_one, exp


with open("C:/py/input.sql", 'r', encoding='utf-8') as f:
    sqlcc = f.read()


example_sql = """
create or replace table mytable as -- mytable example
seLecT a.asdf, b.qwer, -- some comment here
c.asdf, -- some comment there
b.asdf2 frOm table1 as a leFt join 
table2 as b -- and here a comment
    on a.asdf = b.asdf  -- join this way
    inner join table3 as c
on a.asdf=c.asdf
whEre a.asdf= 1 -- comment this
anD b.qwer =2 and a.asdf<=1 --comment that
or b.qwer>=5
groUp by a.asdf
"""

# print all column references (a and b)
for column in parse_one("SELECT a, b + 1 AS c FROM d").find_all(exp.Column):
    print(column.alias_or_name)
print()

# find all projections in select statements (a and c)
for select in parse_one("SELECT a, b + 1 AS c FROM d").find_all(exp.Select):
    for projection in select.expressions:
        print(projection.alias_or_name)
print()

# find all tables (x, y, z)
for table in parse_one("SELECT * FROM x JOIN y JOIN z").find_all(exp.Table):
    print(table.name)
print()

print(sqlcc)
columns = sqlglot.parse_one(sqlcc)

for column in columns.find_all(exp.Column):
    print(column.alias_or_name)