import re
import csv

def parse_insert_statements(file_path, output_csv):
    # 정규식 패턴: INSERT INTO 구문에서 owner와 table 추출
    pattern = r"insert\s+into\s+([\w\${}\.]+)\s"  # ${owner}.table 또는 owner.table
    
    results = []

    # 파일 읽기
    with open(file_path, 'r') as file:
        sql_content = file.read()

    # 정규식 매칭
    matches = re.finditer(pattern, sql_content, re.IGNORECASE)
    for match in matches:
        full_table = match.group(1).strip()  # ${db}.table 형식
        
        # owner와 table 분리
        if "." in full_table:
            owner, table = full_table.split(".", 1)
        else:
            owner, table = "None", full_table

        # 결과 저장
        results.append({
            "Path": file_path,
            "File Name": file_path.split("/")[-1],
            "Owner": owner,
            "Table": table,
            "Full Statement": match.group(0).strip()
        })

    # CSV 저장
    with open(output_csv, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=["Path", "File Name", "Owner", "Table", "Full Statement"]
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"Parsed results saved to {output_csv}")

# 실행
parse_insert_statements('input.sql', 'output.csv')
