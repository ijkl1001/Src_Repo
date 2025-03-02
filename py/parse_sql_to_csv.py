import csv
import re

def parse_sql_to_csv(input_file, output_csv):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    rows = []
    in_select_block = False

    for line in lines:
        line = line.strip()

        # 주석 및 빈 줄 제외
        if line.startswith('--') or line.startswith('/**') or line == '':
            continue

        # SELECT 블록 시작 및 FROM 블록 끝 인식
        if line.upper().startswith("SELECT"):
            in_select_block = True
            continue
        elif line.upper().startswith("FROM"):
            in_select_block = False
            break
        if not in_select_block:
            continue

        # 요소 정리 (쉼표로 구분, "AS STR03" 등 처리)
        # (와 )로 감싸진 쉼표는 분리하지 않고 한 문자열로 처리
        elements = re.split(r',\s*(?![^()]*\))', line)
        for element in elements:
            element = element.strip()
            
            # AS 구문 처리: AS STR03를 하나의 문자열로 병합
            as_match = re.search(r"'([^']+)' AS (\w+)", element)
            if as_match:
                element = f"{as_match.group(1)} AS {as_match.group(2)}"

            # 필드별 정보 추출
            match = re.match(
                r"^(.*?)\s*(\(FORMAT '.*?'\))?\s*(\(CHAR\(\d+\)\)|\(DATE\)|\(DECIMAL\(\d+(,?\d*)?\)\))?\s*(--.*)?$",
                element
            )
            if match:
                column = match.group(1).strip().replace("'", "").replace("“", "").replace("”", "")
                format_type = match.group(2).strip("()").replace("FORMAT", "") if match.group(2) else ""
                data_type = match.group(3).strip("()") if match.group(3) else ""
                comment = match.group(5).lstrip("--").strip() if match.group(5) else ""

                # CHAR 또는 DECIMAL의 크기 추출
                numeric_size = re.search(r"\((\d+(,?\d*)?)\)", data_type)
                size = numeric_size.group(1) if numeric_size else ""

                rows.append([column, format_type, data_type, comment, size])

    # CSV 파일로 저장
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Column', 'Format', 'Data Type', 'Comment', 'Size'])
        csv_writer.writerows(rows)

# 예제 실행
input_file = 'input.sql'  # 입력 파일명
output_csv = 'output.csv'  # 출력 CSV 파일명
parse_sql_to_csv(input_file, output_csv)
