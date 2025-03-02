import csv
import sql_metadata


def parse_sql_file(file_path):
    try:
        # 파일 읽기
        with open(file_path, 'r') as file:
            sql_query = file.read()

        # 파일 이름 및 경로
        file_name = file_path.split('/')[-1]

        # SQL 파서 생성
        parser = sql_metadata.Parser(sql_query)
        query_type = parser.query_type
        tables = parser.tables
        table_aliases = parser.tables_aliases
        columns = parser.columns
        column_aliases = parser.columns_aliases
        with_queries = parser.with_queries

        # 테이블-컬럼 매핑
        column_table_mapping = {}
        for table, alias in table_aliases.items():
            for column in parser.columns_dict.get("select", []):
                if column.startswith(alias + "."):
                    column_name = column.split(".")[1]
                    column_table_mapping[column_name] = table

        # WITH 쿼리 컬럼 및 테이블 처리
        for with_name, with_query in with_queries.items():
            if isinstance(with_query, str):
                with_parser = sql_metadata.Parser(with_query)
                with_columns = with_parser.columns_dict.get("select", [])
                with_tables = with_parser.tables
                with_table_aliases = with_parser.tables_aliases

                for column in with_columns:
                    column_name = column.split(".")[-1]
                    # 소스 테이블 및 테이블 별칭을 구분하여 매핑
                    if "." in column:
                        table_alias = column.split(".")[0]
                        source_table = with_table_aliases.get(table_alias, with_name)
                    else:
                        source_table = with_name

                    column_table_mapping[column_name] = source_table

                    # 테이블 별칭을 정확히 매핑
                    if column_name not in column_aliases:
                        column_aliases[column_name] = with_name

        # 컬럼의 매핑이 없으면 "Unknown" 처리
        for column in columns:
            if column not in column_table_mapping:
                column_table_mapping[column] = "Unknown"

        # CSV 파일에 저장할 데이터 준비
        output_rows = []
        processed_columns = set()

        for column in columns:
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

            # 컬럼 별로 처리
            column_alias = column_aliases.get(col_name, "Unknown")
            table_alias = table_aliases.get(source_table, "Unknown")

            # JOIN Conditions, WHERE Conditions, GROUP BY 제외 처리
            join_condition_str = "None"
            where_condition_str = "None"
            group_by_str = "None"
            having_str = "None"

            output_rows.append({
                "File Path": file_path,
                "File Name": file_name,
                "Query Type": query_type,
                "Column": col_name,
                "Source Table": source_table,
                "Column Aliases": column_alias,
                "Table Aliases": table_alias,
                "JOIN Conditions": join_condition_str,
                "WHERE Conditions": where_condition_str,
                "GROUP BY": group_by_str,
                "HAVING": having_str,
                "VALUES": "None",  # INSERT 또는 VALUES 조건 처리 필요 시 구현
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
