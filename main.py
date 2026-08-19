import json
import os
import csv

# 数据文件路径
DATA_FILE = "data.json"

# 内存里的账单列表，程序运行时数据放这里
records = []


def load_data():
    """启动时从文件读取历史记录"""
    global records

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            records = json.load(f)
        print(f"已加载 {len(records)} 条记录")
    else:
        print("暂无历史数据，从零开始")


def save_data():
    """退出时保存到文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"已保存 {len(records)} 条记录")


def add_record():
    """记一笔"""
    print("\n--- 记一笔 ---")

    # 输入类型
    t_type = input("类型（收入/支出）: ").strip()
    while t_type not in ["收入", "支出"]:
        t_type = input("请输入 收入 或 支出: ").strip()

    # 输入金额
    while True:
        try:
            amount = float(input("金额: "))
            if amount > 0:
                break
            print("金额必须大于0")
        except ValueError:
            print("请输入数字")

    # 根据类型显示不同的分类选项
    if t_type == "收入":
        print("收入分类: 工资 / 奖金 / 兼职 / 投资 / 其他")
        category = input("分类: ").strip() or "其他"
    else:
        print("支出分类: 餐饮 / 交通 / 学习 / 娱乐 / 购物 / 医疗 / 其他")
        category = input("分类: ").strip() or "其他"

    # 输入日期
    date = input("日期（如2026-08-16）: ").strip()
    if not date:
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d")

    # 输入备注
    note = input("备注: ").strip()

    # 组装成字典，加到列表里
    record = {
        "type": t_type,
        "amount": amount,
        "category": category,
        "date": date,
        "note": note
    }
    records.append(record)
    print("✅ 记录成功！")

def show_records():
    """查看记录，支持按月份筛选"""
    print("\n--- 查看记录 ---")

    # 新增：询问是否筛选月份
    month = input("输入月份筛选（如 2026-08，直接回车查全部）: ").strip()

    # 筛选逻辑
    results = records
    if month:
        results = [r for r in records if r["date"].startswith(month)]

    if not results:
        print("暂无记录")
        return

    print(f"\n共 {len(results)} 条记录：")
    print("-" * 60)
    for i, r in enumerate(results, 1):
        symbol = "+" if r["type"] == "收入" else "-"
        print(f"{i}. [{r['date']}] {symbol}¥{r['amount']:.2f} | {r['category']} | {r['note']}")
    print("-" * 60)


def show_report():
    """收支报表"""
    print("\n--- 收支报表 ---")

    if not records:
        print("暂无记录")
        return

    # 计算总收入和总支出
    income = sum(r["amount"] for r in records if r["type"] == "收入")
    expense = sum(r["amount"] for r in records if r["type"] == "支出")
    balance = income - expense

    # 支出分类统计
    expense_by_category = {}
    for r in records:
        if r["type"] == "支出":
            cat = r["category"]
            expense_by_category[cat] = expense_by_category.get(cat, 0) + r["amount"]

    # 排序：花钱最多的排前面
    sorted_categories = sorted(expense_by_category.items(), key=lambda x: x[1], reverse=True)

    # 打印报表
    print("=" * 40)
    print(f"  总收入: +¥{income:.2f}")
    print(f"  总支出: -¥{expense:.2f}")
    print(f"  结  余: {'+' if balance >= 0 else ''}¥{balance:.2f}")
    print("-" * 40)
    print("  支出分类排行:")
    for i, (cat, amt) in enumerate(sorted_categories[:3], 1):
        pct = amt / expense * 100 if expense else 0
        print(f"    {i}. {cat:6s}: ¥{amt:8.2f} ({pct:5.1f}%)")
    print("=" * 40)


def export_csv():
    """导出记录到 CSV 文件"""
    if not records:
        print("暂无记录可导出")
        return

    filename = input("文件名（默认 export.csv）: ").strip() or "export.csv"
    if not filename.endswith(".csv"):
        filename += ".csv"

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(["类型", "金额", "分类", "日期", "备注"])
        # 写入每条记录
        for r in records:
            writer.writerow([
                r["type"],
                r["amount"],
                r["category"],
                r["date"],
                r["note"]
            ])

    print(f"✅ 已导出 {len(records)} 条记录到 {filename}")


def delete_record():
    """删除记录"""
    if not records:
        print("暂无记录可删除")
        return

    show_records()  # 直接调用显示函数，让用户看到编号

    try:
        num = int(input("\n要删除第几条（输入编号，0取消）: "))
        if num == 0:
            print("已取消")
            return
        if num < 1 or num > len(records):
            print("编号不存在")
            return
    except ValueError:
        print("请输入数字")
        return

    deleted = records.pop(num - 1)
    save_data()
    print(f"✅ 已删除: {deleted['type']} ¥{deleted['amount']:.2f}")

def main():
    """程序入口"""
    load_data()

    while True:
        print("\n========== 记账本 ==========")
        print("1. 记一笔")
        print("2. 查看记录")
        print("3. 收支报表")
        print("4. 导出 CSV")
        print("5. 删除记录")  # 新增
        print("0. 退出")
        print("============================")

        choice = input("请选择: ").strip()

        if choice == "1":
            add_record()
        elif choice == "2":
            show_records()
        elif choice == "3":
            show_report()
        elif choice == "4":
            export_csv()
        elif choice == "5":  # 新增
            delete_record()  # 新增
        elif choice == "0":
            save_data()
            print("再见！")
            break

# 程序从这里开始运行
if __name__ == "__main__":
    main()