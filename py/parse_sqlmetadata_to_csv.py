import csv
import os
from sql_metadata import Parser

def parse_sql_to_csv(sql_file_path, output_csv_path):
    # 파일명 추출
    file_name = os.path.basename(sql_file_path)

    # SQL 파일 읽기
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        sql_content = file.read()

    # SQL 문장 구분 (세미콜론 기준으로 구분)
    sql_statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]

    # CSV 파일 작성
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # CSV 헤더
        writer.writerow([
            "File Name", "Query Type", "Tables", "Table Type", "Table Aliases", "Columns",
            "Column Aliases", "With Clauses", "Subqueries"
        ])

        # 각 SQL 문장별로 정보 추출 및 CSV 저장
        for sql in sql_statements:
            parser = Parser(sql)
            
            # 쿼리 타입 판별
            query_type = 'SELECT' if 'SELECT' in sql.upper() else 'WRITE'

            # 테이블 정보와 유형
            tables = parser.tables if parser.tables else ['null']
            table_type = 'write' if any(keyword in sql.upper() for keyword in ['INSERT', 'UPDATE', 'DELETE']) else 'read'
            table_aliases = parser.tables_aliases if parser.tables_aliases else {'null': 'null'}

            # 컬럼 정보
            columns = parser.columns if parser.columns else ['null']
            column_aliases = parser.columns_aliases if parser.columns_aliases else {'null': 'null'}
            with_names = parser.with_names if parser.with_names else 'null'
            subqueries = parser.subqueries if parser.subqueries else 'null'

            # CSV에 저장할 행 데이터 구성
            row = [
                file_name,
                query_type,
                ', '.join(tables),
                table_type,
                ', '.join([f"{alias}: {tbl}" for tbl, alias in table_aliases.items()]) if table_aliases != 'null' else 'null',
                ', '.join(columns),
                ', '.join([f"{col}: {alias}" for col, alias in column_aliases.items()]) if column_aliases != 'null' else 'null',
                ', '.join(with_names) if with_names != 'null' else 'null',
                ', '.join(subqueries) if subqueries != 'null' else 'null',
            ]
            
            # CSV에 행 추가
            writer.writerow(row)

# 실행 예시
parse_sql_to_csv('input.sql', 'output_tera.csv')
