import os
import json

HISTORY_PATH = 'data/history.json'

def load_history():
    """
    讀取歷史紀錄
    """
    if not os.path.exists(HISTORY_PATH):
        return []
    with open(HISTORY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)
