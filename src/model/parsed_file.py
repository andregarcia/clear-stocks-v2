from typing import List

from src.model.transaction import Transaction
from src.model.transactions import Transactions


class ParsedFile:

    def __init__(self, date, transactions: List[Transaction], deals_summary, financial_summary):
        self.date = date
        self.transactions = transactions if type(transactions) == Transactions else Transactions(transactions)
        self.deals_summary = deals_summary
        self.financial_summary = financial_summary

