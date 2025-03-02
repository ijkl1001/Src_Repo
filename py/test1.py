import csv
from sqlglot import parse_one, exp


with open('input.sql', 'r', encoding='utf-8') as file:
    sql_content = file.read()

# SQL 구문을 세미콜론으로 분리
queries = sql_content.split(';')

# 결과 저장
all_elements = []

for query in queries:
    query = query.strip()
    if query:
        print(query)
        elements = []
        tree = parse_one(query, read="teradata")
        query_type = tree.key.upper() if tree.key else 'N/A'

        # 쿼리 레벨 (인라인 서브쿼리인지 확인)
        def is_inline(subquery):
            return isinstance(subquery, exp.Subquery)
        
        # 테이블 정보 추출
        table_alias_map = {}
        for table in tree.find_all(exp.Table):
            table_name = table.name
            table_alias = table.args.get('alias')
            table_alias_map[table_alias or table_name] = table_name  # 테이블과 별칭 매핑
            elements.append({
                'Filename': 'filename',
                'Query Type': query_type,
                'Query Level': 'Inline' if is_inline(table) else 'Main',
                'Type': 'Table',
                'Table': table_name,
                'Table Alias': table_alias if table_alias else 'N/A',
                'Column': 'N/A',
                'Column Alias': 'N/A',
                'Column Value': 'N/A',
                'Subquery': 'N/A',
                'Join Table': 'N/A',
                'Join Column': 'N/A',
                'Where': 'N/A',
                'Values': 'N/A'
            })
        
        print(elements)