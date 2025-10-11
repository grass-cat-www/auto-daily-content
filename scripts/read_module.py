
import importlib


def read_module(path: str):
    """
    根據給定的路徑字串，動態載入並返回對應的模組或函式。
    例如，給定 "scripts.send_discord.send_tip"，
    會返回 send_discord 模組中的 send_tip 函式。
    """
    module_name, func_name = path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, func_name)