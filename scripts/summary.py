import os
import json

SUMMARY_PATH = 'data/summary.json'
def load_summary() -> dict[str, list]:
    """
    讀取摘要資料
    """
    if not os.path.exists(SUMMARY_PATH):
        return {"recent_themes": [], "suggestions": []}
    with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_summary(summary: dict[str, list]):
    """
    儲存摘要資料
    """
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=4)

def get_suggestion_prompt(recent_themes: list[str], title: str, default_themes: str) -> str:
    """
    根據最近的主題，生成用於請 AI 提供未來建議主題的 prompt
    """
    return f"""
以下是最近發過的主題：
{str(recent_themes)}
請以python list的格式，
建議 10~20 個「未來可以使用的{title}相關主題」，
不要與歷史主題重複，每個建議簡短易懂且具體。
分類可以包括但不限於{default_themes}，
(務必不要回答其他格式，也不要說多餘的話，僅回答python list格式)
"""