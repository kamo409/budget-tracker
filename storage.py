"""
storage.py
文件操作：读取和保存数据
"""

import json
import os


def load_records(filename):
    """从文件读取记录"""
    if not os.path.exists(filename):
        return []

    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_records(filename, records):
    """保存记录到文件"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)