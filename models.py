"""
models.py
数据模型：每一笔收支都是一个 Transaction 对象
"""


class Transaction:
    """单笔收支记录"""

    def __init__(self, t_type, amount, category, date, note=""):
        self.type = t_type
        self.amount = amount
        self.category = category
        self.date = date
        self.note = note

    def to_dict(self):
        """转成字典，方便存 JSON"""
        return {
            "type": self.type,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, data):
        """从字典恢复成对象"""
        return cls(
            data["type"],
            data["amount"],
            data["category"],
            data["date"],
            data.get("note", ""),
        )

    def __str__(self):
        """打印格式"""
        symbol = "+" if self.type == "收入" else "-"
        return f"[{self.date}] {symbol}¥{self.amount:.2f} | {self.category} | {self.note}"