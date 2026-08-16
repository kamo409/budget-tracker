import json
import os

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

    # 输入分类
    category = input("分类（如餐饮/交通）: ").strip() or "其他"

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
    """查看所有记录"""
    print("\n--- 所有记录 ---")
    if not records:
        print("暂无记录")
        return

    for i, r in enumerate(records, 1):
        symbol = "+" if r["type"] == "收入" else "-"
        print(f"{i}. [{r['date']}] {symbol}¥{r['amount']:.2f} | {r['category']} | {r['note']}")


def main():
    """程序入口"""
    load_data()

    while True:
        print("\n========== 记账本 ==========")
        print("1. 记一笔")
        print("2. 查看记录")
        print("0. 退出")
        print("============================")

        choice = input("请选择: ").strip()

        if choice == "1":
            add_record()
        elif choice == "2":
            show_records()
        elif choice == "0":
            save_data()
            print("再见！")
            break
        else:
            print("无效选择")


# 程序从这里开始运行
if __name__ == "__main__":
    main()