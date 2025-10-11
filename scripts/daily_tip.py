import yaml
import json
import random
from datetime import datetime
from read_module import read_module

# ===== 0. 初始化 =====

# --- 讀 config.json ---
with open("config.json", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
DEFAULT_THEMES = config["theme"]["default_themes"]
PROMPT_TEMPLATE = config["theme"]["prompt_template"]
HISTORY_RESERVE_DAYS = config["theme"]["history_reserve_days"]
TITLE = config["theme"]["title"]
DESCRIPTION = config["theme"]["description"]
# --- 設置輸出結果的函式 ---
send_tip = read_module(config["functions"]["send_tip"])  # e.g. "send_discord.send_tip"


# --- 設置生成使用的函式 ---
generate_text = read_module(config["functions"]["generate_text"])  # e.g. "ai_generate_gemini.generate_text"



# --- 設置歷史讀取//寫入的函式 ---
load_history = read_module(config["functions"]["history"]["load"])  # e.g. "history.load_history"
save_history = read_module(config["functions"]["history"]["save"])  # e.g. "history.save_history"
visualize_history = read_module(config["functions"]["history"]["visualize_history"])  # e.g. "history.visualize_history"

# --- 設置概要讀取//寫入//建議地prompt的函式 ---
load_summary = read_module(config["functions"]["summary"]["load"])  # e.g. "summary.load_summary"
save_summary = read_module(config["functions"]["summary"]["save"])  # e.g. "summary.save_summary"
get_suggestion_prompt = read_module(config["functions"]["summary"]["get_suggestion_prompt"])  # e.g. "summary.get_suggestion_prompt"


# ===== 1. 讀取歷史紀錄和概要 並 挑選主題 =====
history = load_history()
summary_data = load_summary()

possible_themes = [s for s in summary_data.get("suggestions", []) 
                   if s not in summary_data.get("recent_themes", [])]
if not possible_themes:
    # 若建議走向全部用過，則使用預設主題
    possible_themes = DEFAULT_THEMES

# 隨機選一個主題
today_theme = random.choice(possible_themes)


# === 2. 生成短文 Prompt ===

prompt = f"這次的主題是：{today_theme}\n" + PROMPT_TEMPLATE
tip_text = generate_text(prompt)

# === 3. 更新歷史 JSON ===
today_entry = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "theme": today_theme,
    "text": tip_text
}
history.append(today_entry)
save_history(history)

# === 4. 自動生成未來建議走向 ===
recent_themes = [h["theme"] for h in history][-365:]

response_suggest = generate_text(get_suggestion_prompt(recent_themes), TITLE, str(DEFAULT_THEMES))
summary_data["recent_themes"] = recent_themes
summary_data["suggestions"] = json.loads(response_suggest)
save_summary(summary_data)


# === 5. 生成 Markdown 可視化歷史 ===
visualize_history(
    date=today_entry["date"],
    theme=today_entry["theme"],
    text=today_entry["text"]
)

# === 6. 發送指定位置 ===

send_tip(tip_text)