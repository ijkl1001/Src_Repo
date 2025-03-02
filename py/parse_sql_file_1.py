import csv
import sql_metadata

def parse_sql_file(file_path):
    try:
        # 파일 읽기
        with open(file_path, 'r') as file:
            sql_query = file.read()

        # 파일 이름 및 경로
        file_name = file_path.split('/')[-1]

        # Parser 객체 생성
        parser = sql_metadata.Parser(sql_query)
        query_type = parser.query_type
        tables = parser.tables
        table_aliases = {alias: table for table, alias in parser.tables_aliases.items()}
        columns = parser.columns
        join_conditions = parser.columns_dict.get("join", [])
        where_conditions = parser.columns_dict.get("where", [])
        group_by_conditions = parser.columns_dict.get("group_by", [])
        having_conditions = parser.columns_dict.get("having", [])
        values_dict = parser.values_dict

        # WITH 쿼리 처리
        with_queries = parser.with_queries
        column_table_mapping = {}

        # 테이블-컬럼 매핑
        for alias, table in table_aliases.items():
            for column in parser.columns_dict.get("select", []):
                if column.startswith(alias + "."):
                    column_name = column.split(".")[1]
                    column_table_mapping[column_name] = table

        # WITH 쿼리 컬럼 매핑
        for with_name, with_query in with_queries.items():
            if isinstance(with_query, str):
                with_parser = sql_metadata.Parser(with_query)
                for column in with_parser.columns:
                    column_table_mapping[column] = with_name

        # 누락된 컬럼 처리
        for column in columns:
            if column not in column_table_mapping:
                column_table_mapping[column] = "Unknown"

        # 중복 방지 및 컬럼 분리
        processed_columns = set()

        # CSV 저장 데이터 준비
        output_rows = []

        for column in columns:
            # 테이블 알리아스와 컬럼 분리
            if "." in column:
                alias, col_name = column.split(".")
                source_table = table_aliases.get(alias, "Unknown")
            else:
                alias = ""
                col_name = column
                source_table = column_table_mapping.get(column, "Unknown")

            # 중복 컬럼은 제외
            if (alias, col_name) in processed_columns:
                continue
            processed_columns.add((alias, col_name))

            output_rows.append({
                "File Path": file_path,
                "File Name": file_name,
                "Query Type": query_type,
                "Column": col_name,
                "Source Table": source_table,
                "Column Aliases": None,  # Column Aliases 값 필요 시 추가 구현
                "Table Aliases": alias,
                "JOIN Conditions": join_conditions,
                "WHERE Conditions": where_conditions,
                "GROUP BY": ", ".join(group_by_conditions),
                "HAVING": ", ".join(having_conditions),
                "VALUES": str(values_dict)
            })

        # CSV 파일 저장
        output_file = "parsed_output.csv"
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                "File Path", "File Name", "Query Type", "Column", "Source Table",
                "Column Aliases", "Table Aliases", "JOIN Conditions",
                "WHERE Conditions", "GROUP BY", "HAVING", "VALUES"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(output_rows)

        print(f"SQL 파싱 완료! 결과가 '{output_file}'에 저장되었습니다.")

    except Exception as e:
        print(f"SQL 파싱 중 오류가 발생했습니다: {e}")


# 예제 SQL 파일 실행
parse_sql_file("input_query.sql")