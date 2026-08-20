"""
manager.py
业务逻辑：增删改查、报表、导出
"""

import csv
from storage import save_records


def add_record(records, t_type, amount, category, date, note):
    """记一笔"""
    record = {
        "type": t_type,
        "amount": amount,
        "category": category,
        "date": date,
        "note": note,
    }
    records.append(record)
    return record


def show_records(records, month=None):
    """查看记录"""
    result = records
    if month:
        result = []
        for r in records:
            if r["date"].startswith(month):
                result.append(r)
    return result


def delete_record(records, num):
    """删除记录"""
    if num < 1 or num > len(records):
        return None
    return records.pop(num - 1)


def edit_record(records, num, new_data):
    """修改记录"""
    if num < 1 or num > len(records):
        return None
    record = records[num - 1]
    for key, value in new_data.items():
        if value:
            record[key] = value
    return record


def show_report(records):
    """收支报表"""
    income = 0
    expense = 0
    for r in records:
        if r["type"] == "收入":
            income += r["amount"]
        else:
            expense += r["amount"]

    balance = income - expense

    # 分类统计
    cats = {}
    for r in records:
        if r["type"] == "支出":
            cat = r["category"]
            if cat in cats:
                cats[cat] += r["amount"]
            else:
                cats[cat] = r["amount"]

    # 排序
    sorted_cats = sorted(cats.items(), key=lambda x: x[1], reverse=True)

    return {
        "income": income,
        "expense": expense,
        "balance": balance,
        "categories": sorted_cats,
    }


def export_csv(records, filename):
    """导出 CSV"""
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["类型", "金额", "分类", "日期", "备注"])
        for r in records:
            writer.writerow([
                r["type"],
                r["amount"],
                r["category"],
                r["date"],
                r["note"],
            ])
    return len(records)