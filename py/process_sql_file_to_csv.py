import csv
# import sqlglot
from sqlglot import parse_one, exp

def extract_sql_elements(query, filename):
    elements = []
    tree = parse_one(query, read="teradata")
    query_type = tree.key.upper() if tree.key else ''

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
            'Filename': filename,
            'Query Type': query_type,
            'Query Level': 'Inline' if is_inline(table) else 'Main',
            'Type': 'Table',
            'Table': table_name,
            'Table Alias': table_alias if table_alias else '',
            'Column': '',
            'Column Alias': '',
            'Column Value': '',
            'Subquery': '',
            'Join Table': '',
            'Join Column': '',
            'Where': '',
            'Values': ''
        })
    print(table_alias_map)
    # 컬럼 정보 추출
    for select in tree.find_all(exp.Select):
        for column in select.args.get('expressions', []):
            column_name = column.name if hasattr(column, 'name') else str(column)
            column_alias = column.args.get('alias')
            column_value = column.text('this') if column.args.get('this') else ''
            # 소속 테이블 이름 추출
            table_name = table_alias_map.get(column.args.get('table'), '')
            elements.append({
                'Filename': filename,
                'Query Type': query_type,
                'Query Level': 'Inline' if is_inline(select) else 'Main',
                'Type': 'Column',
                'Table': table_name,
                'Table Alias': '',
                'Column': column_name,
                'Column Alias': column_alias if column_alias else '',
                'Column Value': column_value,
                'Subquery': '',
                'Join Table': '',
                'Join Column': '',
                'Where': '',
                'Values': ''
            })

    # 조인 정보 추출
    for join in tree.find_all(exp.Join):
        join_table = join.args.get('this').name if join.args.get('this') else ''
        join_condition = join.args.get('on')
        join_column = join_condition.text('this') if join_condition else ''
        elements.append({
            'Filename': filename,
            'Query Type': query_type,
            'Query Level': 'Inline' if is_inline(join) else 'Main',
            'Type': 'Join',
            'Table': '',
            'Table Alias': '',
            'Column': '',
            'Column Alias': '',
            'Column Value': '',
            'Subquery': '',
            'Join Table': join_table,
            'Join Column': join_column,
            'Where': '',
            'Values': ''
        })

    # WHERE 조건 추출
    where_clause = tree.args.get('where')
    if where_clause:
        elements.append({
            'Filename': filename,
            'Query Type': query_type,
            'Query Level': 'Inline' if is_inline(where_clause) else 'Main',
            'Type': 'Where',
            'Table': '',
            'Table Alias': '',
            'Column': '',
            'Column Alias': '',
            'Column Value': '',
            'Subquery': '',
            'Join Table': '',
            'Join Column': '',
            'Where': str(where_clause),
            'Values': ''
        })

    # VALUES 구문 추출
    values_clause = tree.args.get('values')
    if values_clause:
        elements.append({
            'Filename': filename,
            'Query Type': query_type,
            'Query Level': 'Inline' if is_inline(values_clause) else 'Main',
            'Type': 'Values',
            'Table': '',
            'Table Alias': '',
            'Column': '',
            'Column Alias': '',
            'Column Value': '',
            'Subquery': '',
            'Join Table': '',
            'Join Column': '',
            'Where': '',
            'Values': str(values_clause)
        })

    # 서브쿼리 추출
    for subquery in tree.find_all(exp.Subquery):
        elements.append({
            'Filename': filename,
            'Query Type': query_type,
            'Query Level': 'Inline',
            'Type': 'Subquery',
            'Table': '',
            'Table Alias': '',
            'Column': '',
            'Column Alias': '',
            'Column Value': '',
            'Subquery': str(subquery),
            'Join Table': '',
            'Join Column': '',
            'Where': '',
            'Values': ''
        })

    return elements

# SQL 파일을 읽고 CSV로 저장하는 함수
def process_sql_file_to_csv(sql_file_path, csv_file_path):
    filename = sql_file_path.split('/')[-1]

    # SQL 파일 읽기
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        sql_content = file.read()

    # SQL 구문을 세미콜론으로 분리
    queries = sql_content.split(';')

    # 결과 저장
    all_elements = []

    for query in queries:
        query = query.strip()
        if query:
            try:
                elements = extract_sql_elements(query, filename)
                all_elements.extend(elements)
            except Exception as e:
                print(f"Error parsing query: {query}\nError: {e}")

    # CSV 파일로 저장
    with open(csv_file_path, mode='w', newline='') as file:
        fieldnames = [
            'Filename', 'Query Type', 'Query Level', 'Type', 'Table', 'Table Alias',
            'Column', 'Column Alias', 'Column Value', 'Subquery', 
            'Join Table', 'Join Column', 'Where', 'Values'
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_elements)

    print("CSV 파일이 성공적으로 생성되었습니다.")

# 예시 사용법

sql_file_path = 'input.sql'  # 분석할 SQL 파일 경로
csv_file_path = 'tera.csv'  # 저장할 CSV 파일 경로

process_sql_file_to_csv(sql_file_path, csv_file_path)
