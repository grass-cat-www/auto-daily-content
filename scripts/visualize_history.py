MARKDOWN_PATH = 'data/history.md'


def visualize_history(date: str, theme: str, text: str) -> None:
    """
    將每日小技巧以 Markdown 格式附加到歷史檔案中
    """
    with open(MARKDOWN_PATH, 'a', encoding='utf-8') as f:
        f.write(f"# {date}歷史紀錄\n\n")
        f.write(f"## 主題：{theme}\n")
        f.write(f"## 內文：\n")
        f.write(f"{text}\n\n")