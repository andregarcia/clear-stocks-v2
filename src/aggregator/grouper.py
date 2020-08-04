from collections import defaultdict
from typing import List

from src.model.parsed_file import ParsedFile
from src.model.transactions import Transactions, MonthTransactions


def group_operations_by_title(parsed_files: List[ParsedFile]):
    grouped_by_titulo = defaultdict(lambda: [])
    for parsed in parsed_files:
        for op in parsed.transactions:
            titulo = op.title
            grouped_by_titulo[titulo].append(op)
    for titulo in grouped_by_titulo:
        ops = grouped_by_titulo[titulo]
        grouped_by_titulo[titulo] = Transactions(sorted(ops, key=lambda x: x.date))
    return grouped_by_titulo


def group_transactions_by_month(transactions: Transactions):
    grouped_by_month = defaultdict(lambda: [])
    for transaction in transactions:
        month_str = f'{transaction.date.year}-{transaction.date.month:02}'
        grouped_by_month[month_str].append(transaction)
    for month in grouped_by_month:
        transactions_in_month = grouped_by_month[month]
        grouped_by_month[month] = MonthTransactions(sorted(transactions_in_month, key=lambda x: (x.title, x.date)))
    return grouped_by_month
