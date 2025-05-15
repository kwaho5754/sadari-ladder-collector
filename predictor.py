import csv
from collections import Counter

CSV_FILE = "ladder_results.csv"
BLOCK_SIZE = 3  # 블럭 크기 (최근 3줄)

def load_data():
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        return reader

def extract_block_pattern(data, idx, size):
    return [(d["s"], d["l"], d["o"]) for d in data[idx:idx+size]]

def block_to_str(block):
    return "-".join([f"{s}|{l}|{o}" for (s, l, o) in block])

def find_top_predictions(data, recent_block):
    patterns = Counter()

    for i in range(len(data) - BLOCK_SIZE - 1):
        block = extract_block_pattern(data, i, BLOCK_SIZE)
        if block == recent_block or block[::-1] == recent_block:  # 정방향 or 역방향
            next_result = data[i + BLOCK_SIZE]["s"]  # 다음 줄 방향만 예측
            patterns[next_result] += 1

    return patterns.most_common(3)

def get_prediction_list():
    data = load_data()
    if len(data) < BLOCK_SIZE + 1:
        return []

    recent_block = extract_block_pattern(data, -BLOCK_SIZE, BLOCK_SIZE)
    result = find_top_predictions(data, recent_block)
    return [(i+1, direction, count) for i, (direction, count) in enumerate(result)]

if __name__ == "__main__":
    predict()