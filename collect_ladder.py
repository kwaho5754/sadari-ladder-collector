import requests
import csv
import time
import os

FILENAME = "ladder_results.csv"
URL = "https://ntry.com/data/json/games/power_ladder/result.json"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def load_last_round():
    if not os.path.exists(FILENAME):
        return -1
    with open(FILENAME, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return int(rows[-1]["r"]) if rows else -1

def save_result(data):
    file_exists = os.path.exists(FILENAME)
    with open(FILENAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "r", "s", "l", "o"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def wait_for_next_result():
    last_round = load_last_round()
    print(f"📌 현재 저장된 마지막 회차: {last_round}")

    timeout = 60  # 최대 대기 시간 (초)
    elapsed = 0
    while elapsed < timeout:
        try:
            res = requests.get(URL, headers=HEADERS)
            data = res.json()
            if int(data["r"]) > last_round:
                save_result(data)
                print(f"✅ 새 회차 {data['r']} 저장 완료")
                return
            else:
                print(f"⏳ 새 회차 대기 중... (현재: {data['r']})")
        except Exception as e:
            print("⚠️ 오류:", e)
        time.sleep(5)
        elapsed += 5
    print("❌ 새 회차 대기 시간 초과")

def run():
    while True:
        wait_for_next_result()
        print("⏱️ 다음 5분까지 대기...\n")
        time.sleep(300)

if __name__ == "__main__":
    run()
