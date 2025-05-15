import csv

CSV_FILE = "ladder_results.csv"

try:
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
        print(f"📊 현재까지 저장된 회차 수: {len(rows) - 1}")
except FileNotFoundError:
    print("❌ ladder_results.csv 파일이 존재하지 않습니다.")
except Exception as e:
    print(f"⚠️ 오류 발생: {e}")
