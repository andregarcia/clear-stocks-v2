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


def group_transactions_by_month(transactions: Transactions) -> List[MonthTransactions]:
    grouped_by_month = defaultdict(lambda: [])
    for transaction in transactions:
        year_and_month = (int(transaction.date.year), int(transaction.date.month))
        grouped_by_month[year_and_month].append(transaction)
    result = []
    last_iteration_transactions = None
    for year_and_month, transactions_in_month in sorted(grouped_by_month.items(), key=lambda x: x[0]):
        year, month = year_and_month
        month_transactions_obj = MonthTransactions(year,
                                        month,
                                        sorted(transactions_in_month, key=lambda x: (x.title, x.date)),
                                        last_iteration_transactions)
        result.append(month_transactions_obj)
        last_iteration_transactions = month_transactions_obj
    return result

