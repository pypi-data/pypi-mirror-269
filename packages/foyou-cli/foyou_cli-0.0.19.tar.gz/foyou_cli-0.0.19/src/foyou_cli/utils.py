import re


def del_special_symbol(s: str) -> str:
    """删除Windows文件名中不允许的字符"""
    return re.sub(r'[\\/:*?"<>|]', '_', s)
