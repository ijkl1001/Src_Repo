# py pd_parse_sql_file.py "c:/py/input.sql" "c:/py/output.csv"
# py pd_parse_sql_file.py "c:/py/input_query.sql" "c:/py/output.csv"

import sql_metadata
import os
import pandas as pd

# 전체 헤더 정의
ALL_HEADERS = [
    "File Path", "File Name", "Query Type", "Column", "Column Source Table",
    "Table", "With Name", "With Query", "Where", "Value"
]

def parse_sql_file(file_path):
    try:
        # 파일 이름 및 경로 구분
        file_name = os.path.basename(file_path)
        file_directory = os.path.dirname(file_path)

        # SQL 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as file:
            query = file.read()
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return []
    except IOError:
        print(f"파일을 읽는 중 오류가 발생했습니다: {file_path}")
        return []

    try:
        # 쿼리 유형 확인
        query_type = query.split()[0].upper() if query else None
        # if query_type not in ["SELECT", "INSERT", "UPDATE", "DELETE"]:
        #     print(f"지원하지 않는 쿼리 유형: {query_type}. 기본값 'SELECT'로 설정합니다.")
        #     query_type = "SELECT"

        # sql_metadata 파서 초기화
        parser = sql_metadata.Parser(query)
        print("테이블:", parser.tables)  # 디버깅: 테이블 목록 출력
        print("컬럼:", parser.columns)  # 디버깅: 컬럼 목록 출력

        # 데이터 저장 리스트 초기화
        rows = []

        # 파일 정보
        rows.append({"Attribute": "File Path", "Value": file_directory})
        rows.append({"Attribute": "File Name", "Value": file_name})
        rows.append({"Attribute": "Query Type", "Value": query_type})

        # 컬럼-테이블 매핑 생성
        column_table_mapping = {}
        for table, alias in parser.tables_aliases.items():
            for column in parser.columns:
                if column.startswith(alias + ".") or column.startswith(table + "."):
                    column_table_mapping[column] = table

        # WITH 절 처리
        if parser.with_names and parser.with_queries:
            for with_name, with_query in parser.with_queries.items():
                rows.append({"Attribute": "With Name", "Value": with_name})
                rows.append({"Attribute": "With Query", "Value": with_query})

                # with_query가 문자열인지 확인
                if isinstance(with_query, str):
                    with_parser = sql_metadata.Parser(with_query)
                    print("1pass")

                    for column in with_parser.columns:
                        column_table_mapping[column] = with_name


        # 컬럼 정보
        for column in parser.columns:
            source_table = column_table_mapping.get(column, "Unknown")
            rows.append({"Attribute": "Column", "Value": column, "Source Table": source_table})

        # WHERE 조건 처리
        if 'where' in parser.columns_dict:
            for where_condition in parser.columns_dict['where']:
                rows.append({"Attribute": "Where", "Value": where_condition})

        # SELECT 필드 값 추가
        if 'select' in parser.columns_dict:
            for select_value in parser.columns_dict['select']:
                rows.append({"Attribute": "Value", "Value": select_value})

        # 테이블 정보
        for table in parser.tables:
            rows.append({"Attribute": "Table", "Value": table})

    except Exception as e:
        print(f"SQL 파싱 중 오류가 발생했습니다: {e}")
        print(f"문제 쿼리: {query}")
        return []

    # 파싱된 결과 확인 출력
    print("=== 파싱된 데이터 확인 ===")
    for row in rows:
        print(row)
    print("=========================")

    return rows

def save_pivoted_csv(parsed_data, output_csv_path):
    if not parsed_data:
        print("저장할 데이터가 없습니다.")
        return

    try:
        # DataFrame 생성
        df = pd.DataFrame(parsed_data)

        # 컬럼 및 테이블 정보 유지
        column_data = df[df['Attribute'] == 'Column'][["Value", "Source Table"]]
        column_data.columns = ["Column", "Column Source Table"]

        table_data = df[df['Attribute'] == 'Table'][["Value"]]
        table_data.columns = ["Table"]

        # 기타 데이터는 피벗 처리
        other_data = df[~df['Attribute'].isin(['Column', 'Table'])]

        # 누락된 헤더를 포함하여 Null로 채움
        for header in ALL_HEADERS:
            if header not in other_data['Attribute'].values:
                other_data = pd.concat(
                    [other_data, pd.DataFrame([{"Attribute": header, "Value": "Null"}])],
                    ignore_index=True
                )

        # 피벗 테이블 생성
        pivot_df = other_data.pivot_table(
            index=None, columns='Attribute', values='Value', aggfunc=lambda x: ' | '.join(x)
        )

        # 고정된 헤더 순서 유지
        pivot_df = pivot_df.reindex(columns=ALL_HEADERS)

        # 컬럼, 테이블 데이터 병합
        column_table_combined = pd.concat([column_data, table_data], ignore_index=True)
        final_df = pd.concat([pivot_df, column_table_combined], ignore_index=True)

        # CSV로 저장
        final_df.to_csv(output_csv_path, index=False, encoding='utf-8')
        print(f"피벗된 데이터가 {output_csv_path} 파일에 저장되었습니다.")
    
    except IOError as e:
        print(f"CSV 파일 저장 중 오류가 발생했습니다: {e}")

# 메인 코드
if __name__ == "__main__":
    import sys

    # 명령줄 인수로 SQL 파일 경로와 출력 CSV 경로 입력받음
    if len(sys.argv) != 3:
        print("사용법: python script.py <input_sql_file> <output_csv_file>")
        sys.exit(1)

    input_sql_file = sys.argv[1]
    output_csv_file = sys.argv[2]

    # SQL 파일 파싱
    parsed_data = parse_sql_file(input_sql_file)

    # 피벗된 데이터를 CSV 파일로 저장
    save_pivoted_csv(parsed_data, output_csv_file)
